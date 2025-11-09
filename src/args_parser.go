package main

type ArgsParserInfo struct {
	description string
	value       string
}

type ArgsParser struct {
	ArgsMap map[string]ArgsParserInfo
}

type ArgsParserInterface interface {
	AddArgument(string, string, string)
	Parse([]string)
	Get(string) string
	isExist(string) bool
}

func GetArgsParser() *ArgsParser {
	return &ArgsParser{
		ArgsMap: make(map[string]ArgsParserInfo),
	}
}

func (a ArgsParser) AddArgument(arg string, default_val string, desc string) {
	a.ArgsMap[arg] = ArgsParserInfo{desc, default_val}
}

func (a ArgsParser) Parse(args []string) {
	for i := 0; i < len(args); i++ {

		if i+1 >= len(args) {
			continue
		}

		v := args[i]
		arg_info, ok := a.ArgsMap[v]
		if ok {
			arg_info.value = args[i+1]
			a.ArgsMap[v] = arg_info
			i++
		}
	}
}

func (a ArgsParser) Get(key string) ArgsParserInfo {
	return a.ArgsMap[key]
}

func (a ArgsParser) isExist(key string) bool {
	_, ok := a.ArgsMap[key]
	return ok
}
