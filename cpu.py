import ram
import assembler
from operator import add, sub, mul, mod, floordiv
from functools import partial


def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if val & (1 << (bits - 1)) != 0:
        val -= (1 << bits)
    return val


def sign(a):
    if a < 0:
        return -1
    elif a > 0:
        return 1
    else:
        return 0


def cmp(a, b):
    return sign(a - b)


class CPU:
    def __init__(self):
        self.registers = {'00': '00', '01': '00', '02': '00', '03': '00'}
        self.IP = 0
        self.SP = int('0xBF', 16)
        self.SR = [0, 0, 0, 0, 0, 0, 0, 0]
        self.jumped = 0
        self.ram = ram.RAM()
        self.table = {'A0': {'len': 2, 'op': add},
                      'A1': {'len': 2, 'op': sub},
                      'A2': {'len': 2, 'op': mul},
                      'A3': {'len': 2, 'op': floordiv},
                      'A4': {'len': 1, 'op': self.inc},
                      'A5': {'len': 1, 'op': self.dec},
                      'A6': {'len': 2, 'op': mod},
                      'B0': {'len': 2, 'op': add},
                      'B1': {'len': 2, 'op': sub},
                      'B2': {'len': 2, 'op': mul},
                      'B3': {'len': 2, 'op': floordiv},
                      'B6': {'len': 2, 'op': mod},
                      'C0': {'len': 1, 'op': self.jmp},
                      'C1': {'len': 1, 'op': self.jz},
                      'C2': {'len': 1, 'op': self.jnz},
                      'C3': {'len': 1, 'op': self.js},
                      'C4': {'len': 1, 'op': self.jns},
                      'C5': {'len': 1, 'op': self.jo},
                      'C6': {'len': 1, 'op': self.jno},
                      'D0': {'len': 2, 'op': self.mov},
                      'D1': {'len': 2, 'op': self.mov},
                      'D2': {'len': 2, 'op': self.mov},
                      'D3': {'len': 2, 'op': self.mov},
                      'D4': {'len': 2, 'op': self.mov},
                      'DA': {'len': 2, 'op': self.cmp},
                      'DB': {'len': 2, 'op': self.cmp},
                      'DC': {'len': 2, 'op': self.cmp},
                      'E0': {'len': 1, 'op': self.push},
                      'E1': {'len': 1, 'op': self.pop},
                      '00': {'len': 0, 'op': 'HALT'}}

    def math(self, func, args):
        a = args[0]
        if func == self.inc:
            return self.inc(args)
        elif func == self.dec:
            return self.dec(args)
        args[0] = func(*args)
        if args[0] > 255:
            args[0] = mod(args[0], 255)
        if cmp(a, args[0]) == 0:
            self.SR = 2
        elif cmp(a, args[0]) == -1:
            self.SR = 8
        return args[0]

    def jmp(self, arg):
        jump = twos_comp(int(arg[0], 16), 8)
        print('Added', jump, 'to IP')
        self.IP += jump
        self.jumped = 1

    def jz(self, arg):
        if self.SR == 2:
            self.jmp(arg)

    def jnz(self, arg):
        if self.SR != 2:
            self.jmp(arg)

    def js(self, arg):
        if self.SR == 8:
            self.jmp(arg)

    def jns(self, arg):
        if self.SR != 8:
            self.jmp(arg)

    def jo(self, arg):
        if self.SR == 4:
            self.jmp(arg)

    def jno(self, arg):
        if self.SR != 4:
            self.jmp(arg)

    def mov(self, op: str, args: list):
        if op == 'D0':
            self.registers[args[0]] = args[1]
        elif op == 'D1':
            self.registers[args[0]] = self.ram.get(args[1])
        elif op == 'D2':
            self.ram.put(args[0], self.registers[args[1]])
        elif op == 'D3':
            self.registers[args[0]] = self.ram.get(self.registers[args[1]])
        elif op == 'D4':
            self.ram.put(self.registers[args[0]], self.registers[args[1]])
        self.ram.show()

    def cmp(self, op: str, args: list):
        self.SR = 0
        if op == 'DA':
            args = [self.registers[args[0]], self.registers[args[1]]]
        elif op == 'DB':
            args = [self.registers[args[0]], args[1]]
        elif op == 'DC':
            args = [self.registers[args[0]], self.ram.get(args[1])]
        res = cmp(*map(partial(int, base=16), args))
        if res == 0:
            self.SR = 2
        elif res == -1:
            self.SR = 8

    def push(self, arg):
        self.ram.put(assembler.tohex(self.SP), self.registers[arg[0]])
        self.SP -= 1
        self.ram.show()

    def pop(self, arg):
        self.SP += 1
        self.registers[arg[0]] = self.ram.get(assembler.tohex(self.SP))

    @staticmethod
    def inc(arg):
        return arg[0] + 1

    @staticmethod
    def dec(arg):
        return arg[0] - 1

    def fetch(self, loc):
        op = self.ram.get(loc)
        lookup = self.table[op]
        func, forward = lookup['op'], lookup['len']
        args = [self.ram.get(hex(int(loc, 16) + i + 1)) for i in range(forward)]
        return func, args, forward, op

    def load(self, code):
        self.ram.image = assembler.load(code).image

    def run(self):
        self.registers = {'00': '00', '01': '00', '02': '00', '03': '00'}
        self.IP = 0
        self.SP = int('0xBF', 16)
        self.SR = 0
        while True:
            print(assembler.tohex(self.IP))
            self.jumped = 0
            func, args, forward, op = self.fetch(hex(self.IP))
            if func == 'HALT':
                break
            elif op[0] == 'A':
                self.registers[args[0]] = assembler.tohex(
                    self.math(func, [int(self.registers[register], 16) for register in args]))
            elif op[0] == 'B':
                self.registers[args[0]] = assembler.tohex(
                    self.math(func, [int(self.registers[args[0]], 16), int(args[1], 16)]))
            elif op[0] == 'D':
                func(op, args)
            else:
                func(args)
            print(self.registers)
            if not self.jumped:
                self.IP += forward + 1
        print('Program finished')


if __name__ == '__main__':
    test = CPU()
    with open('BUBBLE2.asm') as file:
        test.load(file)
        test.run()
        test.ram.show()
    # code = ['MOV AL,10',
    # 'MOV AL,[50]',
    #         'MOV [40],BL',
    #         'MOV AL,[BL]',
    #         'MOV [AL],BL',
    #         '	END			; End program']
    # test.load(code)
    # test.run()
    # test.ram.show()
    print(test.registers)