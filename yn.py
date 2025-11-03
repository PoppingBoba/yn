#!/usr/bin/python3

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#                       YAML to Ninja Generator Demo
#         Author : Henry Shin <henry.shin@thundersoft.com>
#                  Nakada Tokumei <nakada_tokumei@protonmail.com>
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import yaml
import argparse
import os

class YamlParser:
    def __init__(self, file_name: str, loader = yaml.Loader):
        self.loader = loader
        self.stream = open(file_name, 'r')
        self.out = ''
        self.source = ''
        self.cflags = ''

        # Tools
        self.cc = 'gcc'
        self.cxx = 'g++'
        self.linker = 'gcc'
        pass

    def load_tools(self, obj):
        if 'cc' in obj:
            self.cc = obj['cc']
        if 'cxx' in obj:
            self.cxx = obj['cxx']
        if 'linker' in obj:
            self.linker = obj['linker']
        
    def load_app(self, obj):
        self.out = obj['out']
        self.source = obj['source']
        self.cflags = obj['cflags']

    def load(self):
        # print(yaml.load(self.stream, self.loader))
        yaml_obj = yaml.load(self.stream, self.loader)
        print(yaml_obj)
        if 'tools' in yaml_obj:
            self.load_tools(yaml_obj['tools'])
            pass

        self.load_app(yaml_obj['app'])

class NinjaRuleBase:
    def __init__(self):
        self.rulename = None
        self.description = None
        self.command = None
        pass
    
    def pack(self, stream):
        print(f"rule {self.rulename}", file=stream)
        print(f"    command = {self.command}", file=stream)
        print(f"    description = {self.description}", file=stream)
        print(f"", file=stream)
        pass

class NinjaCCRule(NinjaRuleBase):
    def __init__(self, tools='gcc'):
        super().__init__()
        self.rulename = 'cc'
        self.description = 'CC $out'
        self.command = tools + ' -c $in -o $out $cflags $includes'
        pass

class NinjaCXXRule(NinjaRuleBase):
    def __init__(self, tools='g++'):
        super().__init__()
        self.rulename = 'cxx'
        self.description = 'CXX $out'
        self.command = tools + ' -c $in -o $out $cflags $includes'
        pass

class NinjaLDRule(NinjaRuleBase):
    def __init__(self, tools='gcc'):
        super().__init__()
        self.rulename = 'linker'
        self.description = 'LINK $out'
        self.command = tools + ' $in -o $out $ldflags'
        pass

class NinjaCleanRule(NinjaRuleBase):
    def __init__(self):
        super().__init__()
        self.rulename = 'clean'
        self.description = 'CLEAN $in'
        self.command = 'rm -rf $in'
        pass

class NinjaBuildApp():
    def __init__(self, yaml_parser : YamlParser):
        self.out = yaml_parser.out
        self.sources = yaml_parser.source
        self.cflags = yaml_parser.cflags
        self.objs = []
        pass

    def write_obj_build_rules(self, stream):
        rules_list = {
            'cpp' : 'cxx',
            'cc' : 'cxx',
            'c' : 'cc'
        }
        for source in self.sources:
            source_format = source.split(".")[-1]
            self.objs.append(source + '.o')
            print(f"build {source}.o: {rules_list[source_format]} {source}", file=stream)
            if self.cflags != None:
                print(f"    cflags = {self.cflags}", file=stream)
            print(f"", file=stream)
            pass
        pass

    def write_build_apps(self, stream):
        print(f"build {self.out}: linker {' '.join(self.objs)}", file=stream)
        print(f"build clean : clean {self.out} {' '.join(self.objs)}", file=stream)
        print(f"default {self.out}", file=stream)
        pass

def yn_main(args):
    if args.b[-1] != '/':
        args.b += '/'
    yaml_file_path = args.b + args.f
    
    if not os.path.exists(yaml_file_path):
        print(f'{yaml_file_path} is not exist...')
        return     
    
    parser = YamlParser(yaml_file_path)
    parser.load()

    print("out: " + str(parser.out))
    print("source: " + str(parser.source))
    print("cflags: " + str(parser.cflags))

    ninja_out = open(args.b + '/build.ninja', 'w')
    rules = [
        NinjaCCRule(parser.cc),
        NinjaCXXRule(parser.cxx),
        NinjaLDRule(parser.linker),
        NinjaCleanRule(),
    ]

    for rule in rules:
        rule.pack(ninja_out)

    build_app = NinjaBuildApp(parser)
    build_app.write_obj_build_rules(ninja_out)
    build_app.write_build_apps(ninja_out)

argparser = argparse.ArgumentParser()
argparser.add_argument('-b', help=' : Set Build Path', default='./')
argparser.add_argument('-f', help=' : Set yn file', default='yn.yaml')
args = argparser.parse_args()

if __name__ == '__main__':
    yn_main(args=args)
    pass

