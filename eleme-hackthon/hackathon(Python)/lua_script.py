#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

pool0 = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
r = redis.Redis(connection_pool=pool0)

"""
ARGV[1] int        food_id
ARGV[2] int        food_count
ARGV[3] str        cart_id
ARGV[4] int        user_id

ret:
0           204
1           401
2           403
3           404
"""

del_food_lua_script = """
local cart = redis.call("LRANGE",ARGV[3],0,3)
local cart_size = #cart
if cart_size == 0 then
    return 3
end
if not (ARGV[4] == cart[1]) then
    return 1
end
if (cart_size + ARGV[2]) > 4 then
    return 2
end

local new_cart = {}
local food_count = ARGV[2]
local new_cart_size = 0

if food_count == 0 then
    return 0
end

for i=2, cart_size do
    if ARGV[1] == tonumber(cart[i]) and food_count < 0 then
        food_count = food_count + 1
    else
        new_cart_size = new_cart_size + 1
        new_cart[new_cart_size] = cart[i]
    end
end

if new_cart_size ~= 0 then
    redis.call("LTRIM",ARGV[3],0,0)
    for i=1, new_cart_size do
        redis.call("RPUSH", ARGV[3], new_cart[i])
    end
else
    redis.call("LTRIM",ARGV[3],0,0)
end

return 0
"""

#lua_del_food = r.register_script(del_food_lua_script)
lua_del_food = r.script_load(del_food_lua_script)

"""
ARGV[1] int        food_id
ARGV[2] int        food_count
ARGV[3] str        cart_id
ARGV[4] int        user_id

ret:
0           204
1           401
2           403
3           404
"""

add_food_lua_script = """
local cart = redis.call("LRANGE",ARGV[3],0,3)
local cart_size = #cart
if cart_size == 0 then
    return 3
end
if not (ARGV[4] == cart[1]) then
    return 1
end
if (cart_size + ARGV[2]) > 4 then
    return 2
end
for i=1, ARGV[2] do
    redis.call("RPUSH", ARGV[3], ARGV[1])
end
return 0
"""

#lua_add_food = r.register_script(add_food_lua_script)
lua_add_food = r.script_load(add_food_lua_script)

"""
ARGV[1] str        cart_id
ARGV[2] int        user_id
ARGV[3] str        order_id

ret:
0           200
1           401
2           404 篮子不存在
3           403 每个用户只能下一单
4           403 食物库存不足
"""

create_order_lua_script = """
local cart = redis.call("LRANGE",ARGV[1],0,3)
local cart_size = #cart
if cart_size == 0 then
    return {2}
end
if not (ARGV[2] == cart[1]) then
    return {1}
end
if redis.call("SISMEMBER", "ordered_user", ARGV[2]) == 1 then
    return {3}
end
for i=2, cart_size do
    if redis.call("DECR", cart[i]) < 0 then
        return {4}
    end
end
local total_price = 0
for i=2, cart_size do
    total_price = total_price + redis.call("GET", cart[i] .. ":price")
end

local order_dict = {}
order_dict["id"] = ARGV[3]
order_dict["total"] = total_price
local inside_item = {}

if cart_size == 2 then
    inside_item[1] = {}
    inside_item[1]["food_id"] = tonumber(cart[2])
    inside_item[1]["count"] = 1
elseif cart_size == 3 then
    if cart[2] == cart[3] then
        inside_item[1] = {}
        inside_item[1]["food_id"] = tonumber(cart[2])
        inside_item[1]["count"] = 2
    else
        inside_item[1] = {}
        inside_item[1]["food_id"] = tonumber(cart[2])
        inside_item[1]["count"] = 1
        inside_item[2] = {}
        inside_item[2]["food_id"] = tonumber(cart[3])
        inside_item[2]["count"] = 1
    end
elseif cart_size == 4 then
    if cart[2] == cart[3] and cart[2] == cart[4] then
        inside_item[1] = {}
        inside_item[1]["food_id"] = tonumber(cart[2])
        inside_item[1]["count"] = 3
    elseif cart[2] == cart[3] then
        inside_item[1] = {}
        inside_item[1]["food_id"] = tonumber(cart[2])
        inside_item[1]["count"] = 2
        inside_item[2] = {}
        inside_item[2]["food_id"] = tonumber(cart[4])
        inside_item[2]["count"] = 1
    elseif cart[2] == cart[4] then
        inside_item[1] = {}
        inside_item[1]["food_id"] = tonumber(cart[2])
        inside_item[1]["count"] = 2
        inside_item[2] = {}
        inside_item[2]["food_id"] = tonumber(cart[3])
        inside_item[2]["count"] = 1
    elseif cart[3] == cart[4] then
        inside_item[1] = {}
        inside_item[1]["food_id"] = tonumber(cart[2])
        inside_item[1]["count"] = 1
        inside_item[2] = {}
        inside_item[2]["food_id"] = tonumber(cart[3])
        inside_item[2]["count"] = 2
    else
        inside_item[1] = {}
        inside_item[1]["food_id"] = tonumber(cart[2])
        inside_item[1]["count"] = 1
        inside_item[2] = {}
        inside_item[2]["food_id"] = tonumber(cart[3])
        inside_item[2]["count"] = 1
        inside_item[3] = {}
        inside_item[3]["food_id"] = tonumber(cart[4])
        inside_item[3]["count"] = 1
    end
end
order_dict["items"] = inside_item
local out_order_dict = {}
out_order_dict[1] = order_dict
local order_dict_str = cjson.encode(out_order_dict)

redis.call("SADD","ordered_user", ARGV[2])
redis.call("SET",ARGV[2] .. ':order', order_dict_str)
return {0, order_dict_str}
"""

#lua_create_order = r.register_script(create_order_lua_script)
lua_create_order = r.script_load(create_order_lua_script)
