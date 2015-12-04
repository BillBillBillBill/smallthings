from celery import Celery, platforms
from conn import r
import os


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
app = Celery('tasks', broker='redis://%s:%s/1' % (REDIS_HOST, REDIS_PORT))
platforms.C_FORCE_ROOT = True
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    )


@app.task
def a_set(k, v):
    r.set(k, v)


@app.task
def a_rpush(k, *v):
    r.rpush(k, *v)


@app.task
def a_sadd(k, v):
    r.sadd(k, v)


@app.task
def a_hmset(k, v):
    r.hmset(k, v)


@app.task
def a_ltrim(k, s, e):
    r.ltrim(k, s, e)


@app.task
def a_creat_order(order_id, order_dict, user_id):
    pipe = r.pipeline()
    pipe.hmset('order:'+str(order_id), order_dict).sadd('user:'+str(user_id), order_id).sadd('order_id_list', order_id).sadd('ordered_user', user_id).execute()
