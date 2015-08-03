# Grind is the assembly pre-processor for Drip, featuring an interactive mode for command line setup of the Drip system
import json


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
        if self.subs:
            for s in self.subs:
                index = 0
                max = len(self.file)
                result = open(s + '.bean')
                result = [line for line in result]
                while index < max - 1:
                    if '%' + s + '%' in self.file[index]:
                        self.file = self.file[:index + 1] + result + self.file[index + 1:]
                        max += len(result)
                    index += 1

    def out(self):
        return self.file
