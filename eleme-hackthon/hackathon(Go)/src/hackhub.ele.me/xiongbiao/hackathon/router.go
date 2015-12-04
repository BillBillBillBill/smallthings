package main

import (
	"bytes"
	_"io/ioutil"
	"encoding/json"
	"strconv"
	_"log"
	"github.com/gin-gonic/gin"
	"github.com/garyburd/redigo/redis"
	"github.com/nu7hatch/gouuid"
	"encoding/base64"
	_ "html"
	_ "io"
	_ "strings"
	_ "time"
	"fmt"
)

//const (
//    base64Table = "c29tZSBkYXRhIHdpdGggACBhbmQg77u/"
//)

var (
	pool *redis.Pool = poolInit()
	//coder = base64.NewEncoding(base64Table)
//	redisServer string = "localhost:6379"
//	mySQLServer string = "root@tcp(localhost:3306)/eleme"
)

func base64Encode(src []byte) string {
    return base64.StdEncoding.EncodeToString(src)
}

// 处理登录的部分
type User struct {
	Username string
	Password string
}

func login(c *gin.Context) {
	 //对于需要参数的 检查请求体是否为空
	if (c.Request.Method == "POST" || c.Request.Method == "PATCH") && c.Request.URL.Path != "/carts" {
//		//log.Println(c.Request.Method)
//		//log.Println(c.Request.ContentLength)
		if c.Request.ContentLength == 0 {
			//log.Println("请求体为空")
			c.JSON(400, gin.H{
				"code":    "EMPTY_REQUEST",
				"message": "请求体为空",
			})
			c.Abort()
			return
		}
	}
	// 读取用户名密码
	data := &User{}
	c.Bind(data)
//	//log.Println(data.Username)
//	//log.Println(data.Password)
	if data.Username == "" && data.Password == "" {
		c.JSON(400, gin.H{
			"code":    "MALFORMED_JSON",
			"message": "格式错误",
		})
		return
	}
	// 判断是否有效
	if USER[data.Username].password == data.Password {
		// 有效，　生成token
		uid, _ := strconv.Atoi(USER[data.Username].id)
		token := base64.StdEncoding.EncodeToString([]byte(USER[data.Username].id))
		c.JSON(200, gin.H{
			"user_id":    uid,
			"username": data.Username,
			"access_token": token,
		})
	} else {
		c.JSON(403, gin.H{
			"code":    "USER_AUTH_FAIL",
			"message": "用户名或密码错误",
		})
	}
}

//创建篮子部分
func create_cart(c *gin.Context) {

		// 检查是否有access_token， access_token 无效或者为空会直接返回401异常
		// 从query获取token
		token := c.Query("access_token")
		//log.Printf("Token:%q", token)
		if len(token) == 0 {
			// 从header获取token
			token = c.Request.Header.Get("Access-Token")
			////log.Printf("%q", string(username))
		}
		if len(token) == 0 {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
		}
		// 检查token有效性 设置用户ID
		uid, err := base64.StdEncoding.DecodeString(token)
		if err != nil {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
		}

	 //对于需要参数的 检查请求体是否为空
	if (c.Request.Method == "POST" || c.Request.Method == "PATCH") && c.Request.URL.Path != "/carts" {
//		//log.Println(c.Request.Method)
//		//log.Println(c.Request.ContentLength)
		if c.Request.ContentLength == 0 {
			//log.Println("请求体为空")
			c.JSON(400, gin.H{
				"code":    "EMPTY_REQUEST",
				"message": "请求体为空",
			})
			c.Abort()
			return
		}
	}
	//生成"38a2571f-afc7-45ec-5d1c-efd38d094333"这样的cart_id
	cart_id, _ := uuid.NewV4()
	////log.Printf("%q", token)
	// 存入redis
	conn := pool.Get()
	defer conn.Close()
	defer conn.Do("RPUSH", cart_id.String(), uid)
	c.JSON(200, gin.H{
		"cart_id":    cart_id.String(),
	})
}

// 必须大写
type Food struct{
	Id int	`json:"id"`
	Stock int	`json:"stock"`
	Price int		`json:"price"`
}

//查询库存部分
func get_foods(c *gin.Context) {

		// 检查是否有access_token， access_token 无效或者为空会直接返回401异常
		// 从query获取token
		token := c.Query("access_token")
		//log.Printf("Token:%q", token)
		if len(token) == 0 {
			// 从header获取token
			token = c.Request.Header.Get("Access-Token")
			////log.Printf("%q", string(username))
		}
		if len(token) == 0 {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
		}
		// 检查token有效性 设置用户ID
		_, err := base64.StdEncoding.DecodeString(token)
		if err != nil {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
		}
	 //对于需要参数的 检查请求体是否为空
	if (c.Request.Method == "POST" || c.Request.Method == "PATCH") && c.Request.URL.Path != "/carts" {
//		//log.Println(c.Request.Method)
//		//log.Println(c.Request.ContentLength)
		if c.Request.ContentLength == 0 {
			//log.Println("请求体为空")
			c.JSON(400, gin.H{
				"code":    "EMPTY_REQUEST",
				"message": "请求体为空",
			})
			c.Abort()
			return
		}
	}
	var buff bytes.Buffer
	fmt.Fprint(&buff, "[")
	FOOD_SIZE := len(FOOD)
	foods := make([]Food, FOOD_SIZE+1)
	newFood := Food{}
	conn := pool.Get()
	// 结束后关闭
	defer conn.Close()
	//pipeline 记得写multi
	conn.Send("MULTI")
	//iterOrder := make([]int, len(FOOD)+1)
	//count := 0
	
	for key, value := range FOOD {
		newFood.Id,_ = strconv.Atoi(key)
		newFood.Price,_ = strconv.Atoi(value)
		foods[newFood.Id] = newFood
		////log.Printf(key)
		//iterOrder[count],_ = strconv.Atoi(key)
		//count++
		conn.Send("GET", key)
	}

	//c2.Send("GET", "2")
	var r = make([]string, len(FOOD))
	r, _ = redis.Strings(conn.Do("EXEC"))
	////log.Printf("%q",r)
	for i := 1 ; i < FOOD_SIZE+1 ; i++ {
		fuck,_ := strconv.Atoi(r[i-1])
		if i == FOOD_SIZE {
			fmt.Fprintf(&buff,`{"id":%d,"stock":%d,"price":%d}`,foods[i].Id,fuck,foods[i].Price)
		} else {
			fmt.Fprintf(&buff,`{"id":%d,"stock":%d,"price":%d},`,foods[i].Id,fuck,foods[i].Price)
		}
		
		//foods[iterOrder[i]].Stock,_ = strconv.Atoi(r[i])
	}
	// 从1开始 第0个为0
//	for i := 1 ; i < count+1 ; i++ {
//		//log.Printf(strconv.Itoa(foods[i].Id), strconv.Itoa(foods[i].Stock), strconv.Itoa(foods[i].Price))
//	}
	fmt.Fprint(&buff, "]")
	c.Header("Content-Type", "application/json")
	buff.WriteTo(c.Writer)
	//c.JSON(200, foods[1:])
}

// 添加的食物
type Food_item struct {
	Food_id int	`json:"food_id"`
	Count int	`json:"count"`
}

type RET struct {
	R int
}

//添加食物部分
func add_food(c *gin.Context) {

		// 检查是否有access_token， access_token 无效或者为空会直接返回401异常
		// 从query获取token
		token := c.Query("access_token")
		//log.Printf("Token:%q", token)
		if len(token) == 0 {
			// 从header获取token
			token = c.Request.Header.Get("Access-Token")
			////log.Printf("%q", string(username))
		}
		if len(token) == 0 {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
		}
		// 检查token有效性 设置用户ID
		uid, err := base64.StdEncoding.DecodeString(token)
		if err != nil {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
		}
	 //对于需要参数的 检查请求体是否为空
	if (c.Request.Method == "POST" || c.Request.Method == "PATCH") && c.Request.URL.Path != "/carts" {
//		//log.Println(c.Request.Method)
//		//log.Println(c.Request.ContentLength)
		if c.Request.ContentLength == 0 {
			//log.Println("请求体为空")
			c.JSON(400, gin.H{
				"code":    "EMPTY_REQUEST",
				"message": "请求体为空",
			})
			c.Abort()
			return
		}
	}

	// 获取购物车id
	cart_id := c.Param("cart_id")
	// 读取添加的食物id和数量
	data := &Food_item{}
	c.Bind(data)
	//log.Println(strconv.Itoa(data.Food_id))
	//log.Println(strconv.Itoa(data.Count))
	if strconv.Itoa(data.Food_id) == "" || strconv.Itoa(data.Count) == "" {
		c.JSON(400, gin.H{
			"code":    "MALFORMED_JSON",
			"message": "格式错误",
		})
		return
	}
	food_id := data.Food_id
	food_count := data.Count
	_, food_exist := FOOD[strconv.Itoa(data.Food_id)]
	if !food_exist {
		c.JSON(404, gin.H{
			"code":    "FOOD_NOT_FOUND",
			"message": "食物不存在",
		})
		return
	}
	conn := pool.Get()
	defer conn.Close()
	var r int
	if food_count <= 0 {
		r,_ = redis.Int(lua_del_food.Do(conn, food_id, food_count, cart_id, uid))
	} else {
		r,_ = redis.Int(lua_add_food.Do(conn, food_id, food_count, cart_id, uid))
	}
	if r == 3 {
		c.JSON(404, gin.H{
			"code":    "CART_NOT_FOUND",
			"message": "篮子不存在",
		})
		return
	} else if r == 1 {
		c.JSON(401, gin.H{
			"code":    "NOT_AUTHORIZED_TO_ACCESS_CART",
			"message": "无权限访问指定的篮子",
		})
		return
	} else if r == 2 {
		c.JSON(403, gin.H{
			"code":    "FOOD_OUT_OF_LIMIT",
			"message": "篮子中食物数量超过了三个",
		})
		return
	}
	c.AbortWithStatus(204)
}

type order struct {
	Cart_id string
}

type Order struct{
	Id string		`json:"id"`
	Items []Food_item	`json:"items"`
	Total int		`json:"total"`
}

type Create_order_ret struct {
	Cart_id string	`json:"id"`
}

// 创建订单部分
func create_order(c *gin.Context) {
	
		// 检查是否有access_token， access_token 无效或者为空会直接返回401异常
		// 从query获取token
		token := c.Query("access_token")
		//log.Printf("Token:%q", token)
		if len(token) == 0 {
			// 从header获取token
			token = c.Request.Header.Get("Access-Token")
			////log.Printf("%q", string(username))
		}
		if len(token) == 0 {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
		}
		// 检查token有效性 设置用户ID
		uid, err := base64.StdEncoding.DecodeString(token)
		if err != nil {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
		}
	 //对于需要参数的 检查请求体是否为空
	if (c.Request.Method == "POST" || c.Request.Method == "PATCH") && c.Request.URL.Path != "/carts" {
//		//log.Println(c.Request.Method)
//		//log.Println(c.Request.ContentLength)
		if c.Request.ContentLength == 0 {
			//log.Println("请求体为空")
			c.JSON(400, gin.H{
				"code":    "EMPTY_REQUEST",
				"message": "请求体为空",
			})
			c.Abort()
			return
		}
	}

	// 获取购物车id
	data := &order{}
	c.Bind(data)
	//log.Println(data.Cart_id)
	if len(data.Cart_id) == 0 {
		c.JSON(400, gin.H{
			"code":    "MALFORMED_JSON",
			"message": "格式错误",
		})
		return
	}
	cart_id := data.Cart_id
	//log.Println("card_id:", cart_id)
	// 生成order_id
	order_id, _ := uuid.NewV4()
	//查询数据库获取：篮子状态
	conn := pool.Get()
	defer conn.Close()
	r,_ := redis.Int(lua_create_order.Do(conn, cart_id, uid, order_id))
	// 判断篮子是否属于当前用户(取出列表第一项)
	if r == 1 {
		c.JSON(401, gin.H{
			"code":    "NOT_AUTHORIZED_TO_ACCESS_CART",
			"message": "无权限访问指定的篮子",
		})
		return
	} else if r == 2 {
		c.JSON(404, gin.H{
			"code":    "CART_NOT_FOUND",
			"message": "篮子不存在",
		})
		return
	} else if r == 3 {
		//log.Printf("用户已经下过单")
		c.JSON(403, gin.H{
			"code":    "ORDER_OUT_OF_LIMIT",
			"message": "每个用户只能下一单",
		})
		return
	} else if r == 4 {
		c.JSON(403, gin.H{
		"code":    "FOOD_OUT_OF_STOCK",
		"message": "食物库存不足",
		})
		return
	} else {
		retJSON := Create_order_ret{order_id.String()}
		c.JSON(200, retJSON)
	}
}

func get_order(c *gin.Context) {

		// 检查是否有access_token， access_token 无效或者为空会直接返回401异常
		// 从query获取token
		token := c.Query("access_token")
		//log.Printf("Token:%q", token)
		if len(token) == 0 {
			// 从header获取token
			token = c.Request.Header.Get("Access-Token")
			////log.Printf("%q", string(username))
		}
		if len(token) == 0 {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
		}
		// 检查token有效性 设置用户ID
		uid, err := base64.StdEncoding.DecodeString(token)
		if err != nil {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
		}
	 //对于需要参数的 检查请求体是否为空
	if (c.Request.Method == "POST" || c.Request.Method == "PATCH") && c.Request.URL.Path != "/carts" {
//		//log.Println(c.Request.Method)
//		//log.Println(c.Request.ContentLength)
		if c.Request.ContentLength == 0 {
			//log.Println("请求体为空")
			c.JSON(400, gin.H{
				"code":    "EMPTY_REQUEST",
				"message": "请求体为空",
			})
			c.Abort()
			return
		}
	}
	//查询订单
	conn := pool.Get()
	defer conn.Close()
	d,err := redis.String(conn.Do("GET", string(uid)+":order"))
	//log.Printf("Order:", d)
	//log.Printf(strconv.Itoa(len(d)))
	return_order := make([]Order, 0)
	if err != nil {
		//log.Printf("空订单")
		return_order = make([]Order, 0)
	} else {
		return_order = make([]Order, 1)
	}
	json.Unmarshal([]byte(d), &return_order)
	c.JSON(200, return_order)
}

type AdminOrder struct {
	Id string		`json:"id"`
	Items []Food_item	`json:"items"`
	Total int		`json:"total"`
	User_id int	`json:"user_id"`
}

func admin_get_order(c *gin.Context) {

	// 检查是否有access_token， access_token 无效或者为空会直接返回401异常
	// 从query获取token
	token := c.Query("access_token")
	//log.Printf("Token:%q", token)
	if len(token) == 0 {
			// 从header获取token
			token = c.Request.Header.Get("Access-Token")
			////log.Printf("%q", string(username))
	}
	if len(token) == 0 {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
	}
		// 检查token有效性 设置用户ID
		_, err := base64.StdEncoding.DecodeString(token)
		if err != nil {
			c.JSON(401, gin.H{
			"code":    "INVALID_ACCESS_TOKEN",
			"message": "无效的令牌",
			})
			c.Abort()
			return
		}
	 //对于需要参数的 检查请求体是否为空
	if (c.Request.Method == "POST" || c.Request.Method == "PATCH") && c.Request.URL.Path != "/carts" {
//		//log.Println(c.Request.Method)
//		//log.Println(c.Request.ContentLength)
		if c.Request.ContentLength == 0 {
			//log.Println("请求体为空")
			c.JSON(400, gin.H{
				"code":    "EMPTY_REQUEST",
				"message": "请求体为空",
			})
			c.Abort()
			return
		}
	}
	conn := pool.Get()
	defer conn.Close()
	user_list,_ := redis.Strings(conn.Do("SMEMBERS", "ordered_user"))
//	for _,user := range user_list {
//		//log.Printf(user)
//	}
	// 查询全部订单
	conn.Send("MULTI")
	for _,user := range user_list {
		conn.Send("GET",user+":order")
	}
	ret,_ := redis.Strings(conn.Do("EXEC"))
	return_order := make([]AdminOrder, len(ret))
	for i, rr := range ret {
		var oneOrder Order
		var adminOrder AdminOrder
		//log.Printf("%s",rr)
		json.Unmarshal([]byte(rr[1:len(rr)-1]), &oneOrder)
		//log.Printf(oneOrder.Id,oneOrder.Total)
		adminOrder.Id = oneOrder.Id
		adminOrder.Items = oneOrder.Items
		adminOrder.Total = oneOrder.Total
		adminOrder.User_id,_ = strconv.Atoi(user_list[i])
		return_order[i] = adminOrder
	}
	//log.Printf(return_order[0].Id,return_order[0].Total)
	c.JSON(200, return_order)
}