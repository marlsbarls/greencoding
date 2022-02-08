package main

import (
	"fmt"
	"math/big"
)

func fib(a int) int {
	if a < 2 {
		return a
	}
	return fib(a-1) + fib(a-2)
}

func fibIter(n uint64) *big.Int {
	if n < 2 {
		return big.NewInt(int64(n))
	}
	a, b := big.NewInt(0), big.NewInt(1)
	for n--; n > 0; n-- {
		a.Add(a, b)
		a, b = b, a
	}
	return b
}

func main() {
	fmt.Println(fib(46))
	fmt.Println(fibIter(46))
}
