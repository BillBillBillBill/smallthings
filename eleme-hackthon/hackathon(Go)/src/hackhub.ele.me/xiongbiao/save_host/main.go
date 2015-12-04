package main

import (
    //"fmt"
    "os"
    "github.com/garyburd/redigo/redis"
    "time"
    "log"
)

var (
    redisServer = ""
)

// 参数为数据库号
func poolInit(dbNumber int) (*redis.Pool) {
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
        MaxIdle: 100000,
        IdleTimeout: 240 * time.Second,
        Dial: func () (redis.Conn, error) {
            c, err := redis.Dial("tcp", redisServer)
            if err != nil {
                return nil, err
            }
            if _, err := c.Do("SELECT", dbNumber); err != nil {
                 c.Close()
                 return nil, err
            }
            return c, err
        },
        TestOnBorrow: func(c redis.Conn, t time.Time) error {
            _, err := c.Do("PING")
            return err
        },
    }
}


var (
    pool *redis.Pool = poolInit(0)
)


func main() {
    host := os.Getenv("APP_HOST")
    port := os.Getenv("APP_PORT")
    if host == "" {
        host = "localhost"
    }
    if port == "" {
        port = "8080"
    }
    c0 := pool.Get()
    defer c0.Close()
    c0.Do("SADD", "host_url", host + ":" + port)
    time.Sleep(10 * time.Second)
}