# -*- coding: utf-8 -*-
import ram

jumps = {'JMP': 'C0',
         'JZ': 'C1',
         'JNZ': 'C2',
         'JS': 'C3',
         'JNS': 'C4',
         'JO': 'C5',
         'JNO': 'C6'}


def tokenize(lines):
    for line in lines:
        line = line.split(';')[0].strip('\t')
        if ':' in line:
            yield line, []
            continue
        elif 'END' in line:
            break
        line = line.split()
        op, args = line[0], line[1].split(',')
        yield op, args


def parse(lines):
    table = {
        'arithmetic': {
            'ADD': ['A0', 'B0'],
            'SUB': ['A1', 'B1'],
            'MUL': ['A2', 'B2'],
            'DIV': ['A3', 'B3'],
            'MOD': ['A6', 'B6']},
        'INC': 'A4',
        'DEC': 'A5',
        'jumps': jumps,
        'MOV': 'D0',
        'CMP': ['DC', 'DA', 'DB'],
        'PUSH': 'E0',
        'POP': 'E1'
    }
    registers = {'AL': '00', 'BL': '01', 'CL': '02', 'DL': '03'}
    for line in lines:
        op, args = line
        if args:
            if op == 'CMP':
                if args[1][0] == '[' and args[1][-1] == ']':
                    op = table[op][0]
                    args[0] = registers[args[0]]
                    args[1] = args[1][1:-1]
                elif args[1] in registers:
                    op = table[op][1]
                    args = [registers[arg] for arg in args]
                else:
                    op = table[op][2]
                    args[0] = registers[args[0]]
            elif op in table['arithmetic']:
                if args[1] in registers:
                    op = table['arithmetic'][op][0]
                    args = [registers[arg] for arg in args]
                else:
                    op = table['arithmetic'][op][1]
                    args[0] = registers[args[0]]
            elif op in table['jumps']:
                op = table['jumps'][op]
            elif len(args) == 1 and op in table:
                op = table[op]
                args = [registers[args[0]]]
            elif op == 'MOV':
                op = table[op]
                if args[1][0] == '[' and args[1][-1] == ']':
                    args[0] = registers[args[0]]
                    args[1] = args[1][1:-1]
                elif args[0][0] == '[' and args[0][-1] == ']':
                    print(args)
                    args[1] = registers[args[1]]
                    args[0] = args[0][1:-1]
                else:
                    args[0] = registers[args[0]]
        yield op, args


def flatten(foo):
    for x in foo:
        if hasattr(x, '__iter__') and not isinstance(x, str):
            for y in flatten(x):
                yield y
        else:
            yield x


def tohex(val):
    return str(hex((val) & 0xFF))[2:]


def find_jumps(program):
    matches = {}
    l = program[:]
    for item in l:
        if item.endswith(':'):
            matches[item[:-1]] = l.index(item)
            l.remove(item)
    return l, matches


def load(program):
    memory = ram.RAM()
    program = list(flatten(parse(tokenize(program))))
    program, jump_values = find_jumps(program)
    for i in range(len(program)):
        if program[i] in jumps.values():
            if program[i + 1] in jump_values.keys():
                program[i + 1] = tohex(jump_values[program[i + 1]] - i)
    for i in range(len(program)):
        memory.put(hex(i), program[i])
    return memory

if __name__ == '__main__':
    with open('C:/Users/yazdmich230/Desktop/SMS Simulator v50/BUBBLE2.asm') as file:
        load(file).show()
