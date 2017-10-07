package main

import (
	"os"
	"strconv"

	"github.com/labstack/echo"
	"github.com/labstack/echo/middleware"
)

var HTTP_PORT = Getenv("HTTP_PORT", "80").(string)
var PUBLIC_DIR = Getenv("PUBLIC_DIR", "public").(string)

func main() {
	e := echo.New()

	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	// reserve / for public frontend directories
	e.Static("/", PUBLIC_DIR)

	// turn on the http server
	e.Logger.Fatal(e.Start(":" + HTTP_PORT))
}

func Getenv(key string, fallback interface{}) interface{} {
	value := os.Getenv(key)
	if len(value) == 0 {
		return fallback
	}

	switch fallback.(type) {
	case string:
		var nw string
		nw = value
		return nw
	case uint:
		var nw uint64
		nw, _ = strconv.ParseUint(value, 10, 32)
		return uint(nw)
	case bool:
		var nw bool
		nw, _ = strconv.ParseBool(value)
		return nw
	case int:
		var nw int64
		nw, _ = strconv.ParseInt(value, 10, 32)
		return int(nw)
	default:
		panic("unrecognized escape character")
		return value
	}
}
