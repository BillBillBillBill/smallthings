#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import ujson as json  # 比json快
from Cache import load_users, load_foods
import uuid
import redis
import base64
from lua_script import lua_add_food, lua_del_food, lua_create_order
import bjoern
# from meinheld import server
# from gevent import monkey
# monkey.patch_all()
# from gevent.wsgi import WSGIServer
# from meinheld import patch
# patch.patch_all()

host = os.getenv("APP_HOST", "localhost")
port = int(os.getenv("APP_PORT", "8080"))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "eleme")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "toor")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

pool0 = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
r = redis.Redis(connection_pool=pool0)

#用户
# pool1 = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=1)
# r1 = redis.Redis(connection_pool=pool1)

#食物
# pool2 = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=2)
# r2 = redis.Redis(connection_pool=pool2)

USER_LIST = load_users()
FOOD_LIST = load_foods()


def login(environ):
    username = environ['data'].get('username', "")
    password = environ['data'].get('password', "")
    user = USER_LIST.get(username)
    if user and user['password'] == password:
        return '200 OK', ('{"user_id": %s,"username": "%s","access_token": "%s"}' % (user['user_id'], username, base64.standard_b64encode(str(user['user_id'])).replace("=", "$"))).encode('utf-8')
    else:
        return '403 Forbidden', '{"code": "USER_AUTH_FAIL","message": "用户名或密码错误"}'

#######################用户登录部分#######################

#@chronic.time
def get_foods(environ):
    ret = []
    food_ids = FOOD_LIST.keys()
    pipe = r.pipeline()
    for food_id in food_ids:
        pipe.get(food_id)
        ret.append({'id': int(food_id), 'price': FOOD_LIST[food_id]})
    res = pipe.execute()
    #print res
    for i in range(len(res)):
        ret[i]['stock'] = int(res[i])
    return '200 OK', json.dumps(ret)


# 篮子为redis中列表 首项为user id 其余项为food id
#@chronic.time
def create_cart(environ):
    # 生成id
    # m = md5()
    # m.update(str(random.random()))
    # cart_id = m.hexdigest()
    cart_id = uuid.uuid4().hex
    # 存入redis中
    user_id = environ['uid']
    r.rpush(cart_id, user_id)
    #USER_CART_MAP[str(user_id)+"cart"] = [user_id]
    #a_rpush(cart_id, user_id)
    return '200 OK', '{"cart_id": "%s"}' % cart_id


#@chronic.time
def add_food(environ):
    food_id = environ['data'].get('food_id')
    food_count = int(environ['data'].get('count'))
    cart_id = environ["PATH_INFO"].split('/')[2]
    user_id = environ['uid']

    if str(food_id) not in FOOD_LIST.keys():
        return '404 Forbidden', '{"code": "FOOD_NOT_FOUND","message": "食物不存在"}'

    # Lua 优化版：
    if food_count <= 0:
        #ret = lua_del_food(args=[int(food_id), food_count, cart_id, user_id])
        ret = r.evalsha(lua_del_food, 0, int(food_id), food_count, cart_id, user_id)
    else:
        #ret = lua_add_food(args=[int(food_id), food_count, cart_id, user_id])
        ret = r.evalsha(lua_add_food, 0, int(food_id), food_count, cart_id, user_id)
    # 判断篮子是否存在
    if ret == 3:
        return '404 Not Found', '{"code": "CART_NOT_FOUND","message": "篮子不存在"}'
    # 判断篮子是否属于当前用户(取出列表第一项)
    elif ret == 1:
        return '401 Unauthorized', '{"code": "NOT_AUTHORIZED_TO_ACCESS_CART","message": "无权限访问指定的篮子"}'
    # 判断食物数量是否超过篮子最大限制
    elif ret == 2:
        return '403 Forbidden', '{"code": "FOOD_OUT_OF_LIMIT","message": "篮子中食物数量超过了三个"}'
    return '204 No content', ''


#@chronic.time
def get_order(environ):
    user_id = str(environ['uid'])
    order_list = r.get(user_id+':order')
    if not order_list:
        return '200 OK', '[]'
    else:
        return '200 OK', order_list


#@chronic.time
def create_order(environ):
    #dec_stock([(5),(5),(4)])
    cart_id = environ['data'].get('cart_id')
    user_id = environ['uid']
    order_id = uuid.uuid4().hex

    # lua版:
    #ret = lua_create_order(args=[cart_id, user_id, order_id])
    ret = r.evalsha(lua_create_order, 0, cart_id, user_id, order_id)
    if len(ret) == 1:
        # 判断篮子是否属于当前用户(取出列表第一项)
        if ret[0] == 1:
            return '401 Forbidden', '{"code":"NOT_AUTHORIZED_TO_ACCESS_CART","message":"无权限访问指定的篮子"}'
        # 判断篮子是否存在(若不存在返回的是[[]])
        elif ret[0] == 2:
            return '404 Forbidden', '{"code":"CART_NOT_FOUND","message":"篮子不存在"}'
        # 判断用户是否下过单
        elif ret[0] == 3:
            return '403 Forbidden', '{"code":"ORDER_OUT_OF_LIMIT","message":"每个用户只能下一单"}'
        elif ret[0] == 4:
            return '403 Forbidden', '{"code": "FOOD_OUT_OF_STOCK","message": "食物库存不足"}'
        elif ret[0] == 0:
            return '200 OK', '{"id":"%s"}' % order_id
    else:
        return '200 OK', '{"id":"%s"}' % order_id

#@chronic.time
def admin_get_order(environ):
    order_user_list = list(r.smembers('ordered_user'))
    pipe = r.pipeline()
    for order_user in order_user_list:
        pipe.get(order_user+':order')
    order_list = [json.loads(item)[0] for item in pipe.execute()]
    #print order_list
    #print order_user_list
    for i, order in enumerate(order_list):
        order['user_id'] = int(order_user_list[i])
    #print 'order_list', json.dumps(order_list)
    return '200 OK', json.dumps(order_list)


# 格式：url: 允许的方法
API = {
    "login": {
        "POST": login
        },
    "foods": {
        "GET": get_foods
        },
    "carts": {
        "POST": create_cart,
        "PATCH": add_food
        },
    "orders": {
        "GET": get_order,
        "POST": create_order
        },
    "admin": {
        "GET": admin_get_order
        }
}

def application(environ, start_response):
    ##print environ
    status = '200 OK'
    body = ''
    headers = [
        ('Content-Type', 'application/json')
    ]
    # print environ
    request_method = environ["REQUEST_METHOD"]
    route = environ["PATH_INFO"].split('/')
    resource = route[1]
    # 获取query_string 除登录接口外，其他接口需要传入登录接口得到的access_token，access_token无效或者为空会直接返回401异常
    query_string = environ.get("QUERY_STRING", "")
    #print "request_method:", request_method
    #print "route", route
    ##print query_string

    # 获取token(如有)
    qs_list = query_string.split('=')
    if len(qs_list) == 2 and qs_list[0] == 'access_token':
        # 检查token正确性
        token = qs_list[1]
        ret = base64.decodestring(token.replace("$", "=").replace("%24", "="))
        # #print "Token:", token, len(t), r.get(uid)
        if ret:
            environ['token'] = token
            environ['uid'] = int(ret)

    # access-token 放header里的情况
    if not environ.get('token') and environ.get('HTTP_ACCESS_TOKEN'):
        token = environ.get('HTTP_ACCESS_TOKEN')
        ret = base64.decodestring(token.replace("$", "=").replace("%24", "="))
        if ret:
            environ['token'] = token
            environ['uid'] = int(ret)

    # 如果请求为POST 获取数据 放在environ['data']中
    if (request_method == "POST" or request_method == "PATCH") and not (request_method == "POST" and route[1] == 'carts'):
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        if request_body_size == 0:
            status, body = '400 Bad Request', '{"code": "EMPTY_REQUEST","message": "请求体为空"}'
            start_response(status, headers)
            return [body]
        else:
            request_body = environ['wsgi.input'].read(request_body_size)
            try:
                # 创建篮子post数据为空
                if not(route[1] == 'carts' and request_method == "POST"):
                    environ['data'] = json.loads(request_body)
            except:
                # 读取json失败
                status, body = '400 Bad Request', '{"code": "MALFORMED_JSON","message": "格式错误"}'
                start_response(status, headers)
                return [body]

    if not environ.get('token') and resource != 'login':
        status, body = '401 Unauthorized', '{"code": "INVALID_ACCESS_TOKEN","message": "无效的令牌"}'
    else:
        status, body = API[resource][request_method](environ)
        # if resource != 'admin' or (len(route) == 3 and (route[2] == 'orders' or route[1] == 'carts')):
        #     status, body = API[resource][request_method](environ)
        # else:
        #     status = '404 Not Found'

    start_response(status, headers)
    return [body]

if __name__ == '__main__':
    bjoern.run(application, host, port, True)
    #WSGIServer((host, port), application).serve_forever()
