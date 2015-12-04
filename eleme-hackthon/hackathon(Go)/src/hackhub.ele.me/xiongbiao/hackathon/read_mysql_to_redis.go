package main

import (
	"log"
	_ "log"
	_"time"
	"database/sql"
	"os"
	"github.com/garyburd/redigo/redis"
	_ "github.com/go-sql-driver/mysql"
)

var (
	redisServer string = ""
	mySQLServer string = ""
)

//var pool1 *redis.Pool
//var pool2 *redis.Pool

// 参数为数据库号
func poolInit() (*redis.Pool) {
	if redisServer == "" {
		REDIS_HOST := os.Getenv("REDIS_HOST")
		REDIS_PORT := os.Getenv("REDIS_PORT")
		if REDIS_HOST == "" {
		REDIS_HOST = "localhost"
		}
		if REDIS_PORT == "" {
			REDIS_PORT = "6379"
		}
		redisServer = REDIS_HOST + ":" + REDIS_PORT
		log.Printf(redisServer)
	}
	//redis pool
	return &redis.Pool{
		MaxIdle: 10000,
		MaxActive: 10000,
		//IdleTimeout: 240 * time.Second,
		Dial: func () (redis.Conn, error) {
			c, err := redis.Dial("tcp", redisServer)
			if err != nil {
				return nil, err
			}
			return c, err
		},
	}
}

func read_mysql_to_redis() {
	if mySQLServer == "" {
		DB_HOST := os.Getenv("DB_HOST")
		DB_PORT := os.Getenv("DB_PORT")
		DB_NAME := os.Getenv("DB_NAME")
		DB_USER := os.Getenv("DB_USER")
		DB_PASS := os.Getenv("DB_PASS")
	
		if DB_HOST == "" {
			DB_HOST = "localhost"
		}
		if DB_PORT == "" {
			DB_PORT = "3306"
		}
		if DB_NAME == "" {
			DB_NAME = "eleme"
		}
		if DB_USER == "" {
			DB_USER = "root"
		}
		if DB_PASS == "" {
			DB_PASS = "toor"
		}
		mySQLServer = DB_USER + ":" + DB_PASS + "@tcp(" + DB_HOST + ":" + DB_PORT + ")/" + DB_NAME
		log.Printf(mySQLServer)
	}
	db, err  := sql.Open("mysql", mySQLServer)
	c0 := pool.Get()
	// 1放用户
	//pool1 = poolInit(1)
	// 2放食物
	//pool2 = poolInit(2)
	//c1 := pool1.Get()
	//c2 := pool2.Get()
	// 结束后关闭
	//defer c1.Close()
	//defer c2.Close()
	defer c0.Close()
	defer db.Close()
	//c1.Do("SET", "type", "user'")
	//c0.Do("SET", "type", "food'")
	// 将食物存入redis中
	c0.Do("FLUSHALL")
	c0.Do("CONFIG", "loglevel","save", "warning")
	c0.Do("CONFIG", "SET","save", "")
	c0.Do("CONFIG", "SET","appendfsync", "no")
	c0.Do("CONFIG", "SET","slowlog-log-slower-than", "1000000")
	c0.Do("CONFIG", "SET","maxclients", "1000000")
	foods, err := db.Query("SELECT * FROM food")
	columns, err := foods.Columns()
	values := make([]sql.RawBytes, len(columns))
	scanArgs := make([]interface{}, len(values))
	for i := range values {
		scanArgs[i] = &values[i]
	}
	for foods.Next() {
		err = foods.Scan(scanArgs...)
		if err != nil {
			panic(err.Error())
		}
		c0.Do("SET", string(values[0]) + ":price", string(values[2]))
		c0.Do("SET", string(values[0]), string(values[1]))
		//c0.Do("HSET", string(values[0]) + ":info", "id", string(values[0]) )
//		log.Printf(string(values[0]))
//		log.Printf(string(values[1]))
//		log.Printf(string(values[2]))
	
//		var value string
//		for i, col := range values {
//			if col == nil {
//				value = "NULL"
//			} else {
//				value = string(col)
//			}
//			log.Printf(columns[i])
//			log.Printf(value)
//		}
	}
	
	// 将用户存入redis中
//	users, err := db.Query("SELECT * FROM user")
//	columns, err = users.Columns()
//	values = make([]sql.RawBytes, len(columns))
//	scanArgs = make([]interface{}, len(values))
//	for i := range values {
//		scanArgs[i] = &values[i]
//	}
//	for users.Next() {
//		err = users.Scan(scanArgs...)
//		if err != nil {
//			panic(err.Error())
//		}
//		c1.Do("HSET", string(values[1]), "user_id", string(values[0]))
//		c1.Do("HSET", string(values[1]), "password", string(values[2]))
////		log.Printf(string(values[0]))
////		log.Printf(string(values[1]))
////		log.Printf(string(values[2]))
//	}
//    n, err := c.Do("SET", "xx", "呵呵")
//    n, err = c.Do("GET", "xx")
//    if err != nil {
//        log.Fatal(err)
//    }
//    log.Printf("return:%s", n)
//	//pipeline
//	//c.Send("MULTI")
//	c.Send("SET", "test", 234)
//	c.Send("SET", "test2", "20")
//	c.Send("GET", "XX")
//	c.Send("GET", "XX")
////	a, err := c.Do("EXEC")
////	if err != nil {
////		log.Printf("%s", err)
////	}
//	// 或者：
//	c.Flush()
//	a, err := redis.String(c.Receive()) 
//	b, err := redis.String(c.Receive()) 
//	if err != nil {
//		log.Printf("%s", err)
//	}
	
//	log.Printf("ret:%q", a)
//	log.Printf("ret:%q", b)
}