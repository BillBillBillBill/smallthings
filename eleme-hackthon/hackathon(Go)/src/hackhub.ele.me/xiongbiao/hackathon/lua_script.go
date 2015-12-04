package main

import (
	"github.com/garyburd/redigo/redis"
)

var (
	del_food_lua_script = `
local cart = redis.call("LRANGE",KEYS[3],0,3)
local cart_size = #cart
if cart_size == 0 then
    return 3
end
if not (KEYS[4] == cart[1]) then
    return 1
end
if (cart_size + KEYS[2]) > 4 then
    return 2
end

local new_cart = {}
local food_count = KEYS[2]
local new_cart_size = 0

if food_count == 0 then
    return 0
end

for i=2, cart_size do
    if KEYS[1] == tonumber(cart[i]) and food_count < 0 then
        food_count = food_count + 1
    else
        new_cart_size = new_cart_size + 1
        new_cart[new_cart_size] = cart[i]
    end
end

if new_cart_size ~= 0 then
    redis.call("LTRIM",KEYS[3],0,0)
    for i=1, new_cart_size do
        redis.call("RPUSH", KEYS[3], new_cart[i])
    end
else
    redis.call("LTRIM",KEYS[3],0,0)
end
return 0
`
	add_food_lua_script = `
local cart = redis.call("LRANGE",KEYS[3],0,3)
local cart_size = #cart
if cart_size == 0 then
    return 3
end
if not (KEYS[4] == cart[1]) then
    return 1
end
if (cart_size + KEYS[2]) > 4 then
    return 2
end
for i=1, KEYS[2] do
    redis.call("RPUSH", KEYS[3], KEYS[1])
end
return 0
`
	create_order_lua_script = `
local cart = redis.call("LRANGE",KEYS[1],0,3)
local cart_size = #cart
if cart_size == 0 then
    return 2
end
if not (KEYS[2] == cart[1]) then
    return 1
end
if redis.call("SISMEMBER", "ordered_user", KEYS[2]) == 1 then
    return 3
end
for i=2, cart_size do
    if redis.call("DECR", cart[i]) < 0 then
        return 4
    end
end
local total_price = 0
for i=2, cart_size do
    total_price = total_price + redis.call("GET", cart[i] .. ":price")
end

local order_dict = {}
order_dict["id"] = KEYS[3]
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

redis.call("SADD","ordered_user", KEYS[2])
redis.call("SET",KEYS[2] .. ':order', order_dict_str)
return 0
`
	lua_del_food = redis.NewScript(4, del_food_lua_script)
	lua_add_food = redis.NewScript(4, add_food_lua_script)
	lua_create_order = redis.NewScript(3, create_order_lua_script)
)