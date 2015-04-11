import ram

jumps = {'JMP': '00C0',
         'JZ': '00C1',
         'JNZ': '00C2',
         'JS': '00C3',
         'JNS': '00C4',
         'JO': '00C5',
         'JNO': '00C6'}
table = {
    'arithmetic': {
        'ADD': ['00A0', '00B0'],
        'SUB': ['00A1', '00B1'],
        'MUL': ['00A2', '00B2'],
        'DIV': ['00A3', '00B3'],
        'MOD': ['00A6', '00B6']},
    'INC': '00A4',
    'DEC': '00A5',
    'jumps': jumps,
    'MOV': ['00D0', '00D1', '00D2', '00D3', '00D4'],
    'CMP': ['00DC', '00DA', '00DB', '00DD'],
    'PUSH': '00E0',
    'POP': '00E1',
    'OUT': ['00F0', '00F1', '00F2']
}


registers = {'AH': '0010',
             'AL': '0001',
             'AX': '0100',
             'BH': '0020',
             'BL': '0002',
             'BX': '0200',
             'CH': '0030',
             'CL': '0003',
             'CX': '0300',
             'DH': '0040',
             'DL': '0004',
             'DX': '0400'}


def tokenize(lines):
    for line in lines:
        line = line.split(';')[0].strip('\t')
        if ':' in line:
            yield line.strip('\t').strip(' '), []
            continue
        if 'END' in line:
            yield 'END', []
            continue
        line = line.split()
        op, args = line[0], line[1].split(',')
        print('Input assembly code: ', op, *args)
        yield op, args


def mov(args):
    if args[0] in registers:
        if len(args[1]) == 4 and args[1][1:-1] in registers:
            return '00D3', [registers[args[0]], registers[args[1][1:-1]]]
        elif len(args[1]) == 6:
            return '00D1', [registers[args[0]], args[1][1:-1]]
        else:
            return '00D0', [registers[args[0]], args[1]]
    else:
        if args[0][1:-1] in registers:
            return '00D4', [registers[args[0][1:-1]], registers[args[1]]]
        else:
            return '00D2', [args[0][1:-1], registers[args[1]]]


def parse(lines):
    for line in lines:
        op, args = line
        print(op, args)
        if args:
            if op == 'DB':
                if len(args[0]) == 4:
                    op, args = args, []
                else:
                    args = [tohex(ord(n)) for n in args[0][1:-1]]
                    op, args = args[0], args[1:]
            elif op == 'CMP':
                if args[1][0] == '[' and args[1][-1] == ']':
                    op = table[op][0]
                    args[0] = registers[args[0]]
                    args[1] = args[1][1:-1]
                elif args[1] in registers:
                    op = table[op][1]
                    args = [registers[arg] for arg in args]
                elif args[0][0] == '[' and args[0][-1] == ']':
                    op = table[op][3]
                    args[0] = registers[args[0][1:-1]]
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
                if op == 'OUT':
                    # a = input('before ^')
                    if args[0][0] == '[' and args[0][-1] == ']':
                        op = table[op][2]
                        args[0] = registers[args[0][1:-1]]
                    elif args[0] in registers:
                        op = table[op][1]
                        args[0] = registers[args[0]]
                    else:
                        op = table[op][0]
                    print(op, args)
                else:
                    op = table[op]
                    args = [registers[args[0]]]
            elif op == 'MOV':
                op, args = mov(args)
        elif op == 'OUT':
            if args[0][0] == '[' and args[0][-1] == ']':
                op = table[op][2]
                args[0] = args[0][1:-1]
            elif args[0] in registers:
                op = table[op][1]
                args[0] = registers[args[0]]
            else:
                op = table[op][0]
        elif op == 'END':
            op, args = '0000', []
            print(op)
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
    return str(hex(val & 0xFFFF))[2:].zfill(4).upper()


def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if val & (1 << (bits - 1)) != 0:
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
                print(' =', twos_comp(int(l[i + 1], 16), 16))
    return l


def load(program):
    memory = ram.RAM()
    program = list(program)
    program = find_jumps(list(flatten(parse(tokenize(program)))))
    for i in range(len(program)):
        memory.put(hex(i), program[i])
    return memory


if __name__ == '__main__':
    with open('BUBBLE2.asm') as file:
        load(file).show()
