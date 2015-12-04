import pymysql
import os
import redis

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "eleme")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "toor")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# conn = pymysql.connect(
#     host=DB_HOST,
#     port=DB_PORT,
#     passwd=DB_PASS,
#     user=DB_USER,
#     db=DB_NAME,
#     )
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
r = redis.Redis(connection_pool=pool)
