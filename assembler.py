import ram

jumps = {'JMP': 'C0',
         'JZ': 'C1',
         'JNZ': 'C2',
         'JS': 'C3',
         'JNS': 'C4',
         'JO': 'C5',
         'JNO': 'C6'}
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
    'MOV': ['D0', 'D1', 'D2', 'D3', 'D4'],
    'CMP': ['DC', 'DA', 'DB'],
    'PUSH': 'E0',
    'POP': 'E1'
}
registers = {'AL': '00', 'BL': '01', 'CL': '02', 'DL': '03'}


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
        print('Input assembly code: ', op, *args)
        yield op, args


def mov(args):
    if args[0] in registers:
        if args[1][1:-1]:
            if args[1][1:-1] in registers:
                return 'D3', [registers[args[0]], registers[args[1][1:-1]]]
            else:
                return 'D1', [registers[args[0]], args[1][1:-1]]
        else:
            return 'D0', [registers[args[0]], args[1]]
    else:
        if args[0][1:-1] in registers:
            return 'D4', [registers[args[0][1:-1]], registers[args[1]]]
        else:
            return 'D2', [args[0][1:-1], registers[args[1]]]


def parse(lines):
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
                op, args = mov(op, args)
        print('Generated machine code: ', op, *args)
        yield op, args


def flatten(foo):
    for x in foo:
        if hasattr(x, '__iter__') and not isinstance(x, str):
            for y in flatten(x):
                yield y
        else:
            yield x


def tohex(val):
    return str(hex(val & 0xFF))[2:]


def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if(val & (1 << (bits - 1)) != 0):
        val -= (1 << bits)
    return val


def find_jumps(program):
    matches = {}
    l = program[:]
    for item in l:
        if item.endswith(':'):
            matches[item[:-1]] = l.index(item)
            l.remove(item)
    for i in range(len(l)):
        if l[i] in jumps.values():
            if l[i + 1] in matches.keys():
                print('Jump to', l[i + 1], end='')
                l[i + 1] = tohex(matches[l[i + 1]] - i)
                print(' =', twos_comp(int(l[i + 1], 16), 8))
    return l


def load(program):
    memory = ram.RAM()
    program = find_jumps(list(flatten(parse(tokenize(program)))))
    print('DB '+' DB '.join(program))
    for i in range(len(program)):
        memory.put(hex(i), program[i])
    return memory

if __name__ == '__main__':
    with open('BUBBLE2.asm ') as file:
        load(file).show()
