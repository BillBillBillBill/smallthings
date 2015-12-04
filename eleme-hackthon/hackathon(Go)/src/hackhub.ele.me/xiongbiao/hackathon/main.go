package main

import (
	_"fmt"
	"github.com/gin-gonic/gin"
	"runtime"
	"os"
)

func main() {
	read_mysql_to_redis()
	load_users()
	load_foods()
	ConfigRuntime()
	StartGin()
}

func ConfigRuntime() {
	//nuCPU := runtime.NumCPU()
	runtime.GOMAXPROCS(10)
}

func StartGin() {
	host := os.Getenv("APP_HOST")
	port := os.Getenv("APP_PORT")
	if host == "" {
		host = "localhost"
	}
	if port == "" {
		port = "8080"
	}
	gin.SetMode(gin.ReleaseMode)
	router := gin.New()
	router.PATCH("/carts/:cart_id", add_food)
	router.POST("/login", login)
	router.POST("/orders", create_order)
	router.GET("/orders", get_order)
	router.GET("/foods", get_foods)
	router.POST("/carts", create_cart)
	router.GET("/admin/orders", admin_get_order)
	router.Run(host+":"+port)
}