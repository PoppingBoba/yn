#!/usr/bin/python3

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#                       YAML to Ninja Generator Demo
#         Author : Henry Shin <henry.shin@thundersoft.com>
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import yaml

class YamlParser:
    def __init__(self, file_name: str, loader = yaml.Loader):
        self.loader = loader
        self.stream = open(file_name, 'r')
        self.out = ''
        self.source = ''
        self.cflags = ''
        pass

    def load(self):
        yaml_obj = yaml.load(self.stream, self.loader)['app']
        self.out = yaml_obj['out']
        self.source = yaml_obj['source']
        self.cflags = yaml_obj['cflags']

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
    def __init__(self):
        super().__init__()
        self.rulename = 'cc'
        self.description = 'CC $out'
        self.command = 'gcc -c $in -o $out $cflags $includes'
        pass

class NinjaCXXRule(NinjaRuleBase):
    def __init__(self):
        super().__init__()
        self.rulename = 'cxx'
        self.description = 'CXX $out'
        self.command = 'g++ -c $in -o $out $cflags $includes'
        pass

class NinjaLDRule(NinjaRuleBase):
    def __init__(self):
        super().__init__()
        self.rulename = 'linker'
        self.description = 'LINK $out'
        self.command = 'gcc $in -o $out $ldflags'
        pass

class NinjaBuildApp():
    def __init__(self, yaml_parser : YamlParser):
        self.out = yaml_parser.out
        self.sources = yaml_parser.source
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
            pass
        pass

    def write_build_apps(self, stream):
        print(f"build {self.out}: linker {' '.join(self.objs)}", file=stream)
        print(f"default {self.out}", file=stream)
        pass

parser = YamlParser('test/helloworld/yn.yaml')
parser.load()
print("out: " + str(parser.out))
print("source: " + str(parser.source))
print("cflags: " + str(parser.cflags))

ninja_out = open('test/helloworld/build.ninja', 'w')
rules = [
    NinjaCCRule(),
    NinjaCXXRule(),
    NinjaLDRule()
]

for rule in rules:
    rule.pack(ninja_out)

build_app = NinjaBuildApp(parser)
build_app.write_obj_build_rules(ninja_out)
build_app.write_build_apps(ninja_out)


