package main

import (
	_"log"
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)

var (
	// 预先给 make 函数一一个合理元素数量参数,有助于提升性能。因为事先申请一一大大块内存,可避免后续操作时频繁扩张。
	USER = make(map[string]struct {
		id string
		password string
	}, 10000)
	// 对应价格
	FOOD = make(map[string]string, 100)
)

func load_users() {
	db, err  := sql.Open("mysql", mySQLServer)
	defer db.Close()
	// 将用户存入cache中
	users, err := db.Query("SELECT * FROM user")
	columns, err := users.Columns()
	values := make([]sql.RawBytes, len(columns))
	scanArgs := make([]interface{}, len(values))
	for i := range values {
		scanArgs[i] = &values[i]
	}
	for users.Next() {
		err = users.Scan(scanArgs...)
		if err != nil {
			panic(err.Error())
		}
		//当 map 因扩张而而重新哈希时,各键值项存储位置都会发生生改变。 因此,map
		// 被设计成 not addressable。 类似 m[1].name 这种期望透过原 value
		// 指针修改成员的行行为自自然会被禁止止。
		// 所以要用这种写法。。。。
		u := USER[string(values[1])]
		u.id = string(values[0])
		u.password = string(values[2])
		USER[string(values[1])] = u
		//log.Printf(USER[string(values[1])].id)
	}
}

func load_foods() {
	db, err  := sql.Open("mysql", mySQLServer)
	defer db.Close()
	// 将食物存入cache中
	foods, err := db.Query("SELECT id, price FROM food")
	var id string
	var price string
	for foods.Next() {
		err = foods.Scan(&id, &price)
		if err != nil {
			panic(err.Error())
		}
		//当 map 因扩张而而重新哈希时,各键值项存储位置都会发生生改变。 因此,map
		// 被设计成 not addressable。 类似 m[1].name 这种期望透过原 value
		// 指针修改成员的行行为自自然会被禁止止。
		// 所以要用这种写法。。。。
		f := FOOD[id]
		f = price
		FOOD[id] = f
		//log.Printf(string(FOOD[id]))
	}
}
