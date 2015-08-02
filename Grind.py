# Grind is the assembly pre-processor for Drip, featuring an interactive mode for command line setup of the Drip system
import json
import re


def verify_dict(check, args, default=None):
    for arg in args:
        if arg not in check:
            check[arg] = default
    return check


def parse_dict(kwargs, arg_list, default=None):
    args = verify_dict(kwargs, arg_list, default)
    return (args[x] for x in arg_list)


class Grind:
    def __init__(self, **args):
        self.file, self.config = parse_dict(args, ['file', 'config'], '')
        self.file = open(self.file)
        self.file = [line for line in self.file]
        config = open(self.config)
        self.switches, self.subs = parse_dict(json.load(config), ['switches', 'subs'], dict())

    def sub(self):
        if self.subs['files']:
            for s in self.subs['files']:
                match, result = s.split('->')
                regex = re.compile(match)
                for line in self.file:
                    regex.sub(result, line)
                for line in self.file:
                    print(line)
