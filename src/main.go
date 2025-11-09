package main

import (
	"fmt"
	"os"

	"github.com/PoppingBoba/ninjago"
)

func test_ninjago() {
	var cxx_rule = ninjago.MakeNinjaGoRule("cxx", "g++ -c $in -o $out $cflags $includes", "CXX $out")

	fmt.Println("========== Check CXX Rule ==========")
	fmt.Println(cxx_rule.String())
}

func main() {
	fmt.Print("Hello yn\n")

	var arg_parser = GetArgsParser()

	arg_parser.AddArgument("-b", "./", "Set Build Path")
	arg_parser.AddArgument("-f", "yn.yaml", "Set yn File")

	arg_parser.Parse(os.Args)

	fmt.Println("Check Argument Test [-b] : ", arg_parser.Get("-b").value)
	fmt.Println("Check Argument Test [-f] : ", arg_parser.Get("-f").value)

	test_ninjago()
}
