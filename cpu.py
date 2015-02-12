# pylint: disable:E501
from ram import RAM
from assembler import load
from operator import add, sub, mul, floordiv, mod
from math import floor
inc = lambda x: x + 1
dec = lambda x: x - 1


def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if val & (1 << (bits - 1)) != 0:
        val -= (1 << bits)
    return val


class CPU:
    def __init__(self):
        self.registers = {'00': 0, '01': 0, '02': 0, '03': 0}
        self.IP = 0
        self.SP = int('0xBF', 16)
        self.SR = [0, 0, 0, 0, 0, 0, 0, 0]
        self.ram = RAM()
        self.table = {'A0': {'len': 2, 'op': add},
                      'A1': {'len': 2, 'op': sub},
                      'A2': {'len': 2, 'op': mul},
                      'A3': {'len': 2, 'op': floordiv},
                      'A4': {'len': 1, 'op': inc},
                      'A5': {'len': 1, 'op': dec},
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
                      'E0': {'len': 1, 'op': 'PUSH'},
                      'E1': {'len': 1, 'op': 'POP'}}

    def jmp(self, arg):
        self.IP += twos_comp(arg, 8)

    def jz(self, arg):
        self.IP += twos_comp(arg, 8)

    def jnz(self, arg):
        self.IP += twos_comp(arg, 8)

    def js(self, arg):
        self.IP += twos_comp(arg, 8)

    def jns(self, arg):
        self.IP += twos_comp(arg, 8)

    def jo(self, arg):
        self.IP += twos_comp(arg, 8)

    def jno(self, arg):
        self.IP += twos_comp(arg, 8)

    def mov(self, *args):
        pass

    def cmp(self, *args):
        pass

    def fetch(self, loc):
        op = self.ram.get(loc)
        lookup = self.table[op]
        func, forward = lookup['op'], lookup['len']
        args = [self.ram.get(hex(int(loc, 16) + i + 1)) for i in range(forward)]  # TypeError: 'method' object cannot be interpreted as an integer
        return func, args

if __name__ == '__main__':
    test = CPU()
    with open('BUBBLE2.asm') as file:
        test.ram = load(file)
        test.ram.show()
        test.fetch('00')