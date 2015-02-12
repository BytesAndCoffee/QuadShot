from ram import RAM
from assembler import load
from operator import add, sub, mul, floordiv, mod

inc = lambda x: x + 1
dec = lambda x: x - 1


def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if val & (1 << (bits - 1)) != 0:
        val -= (1 << bits)
    return val


def cmp(a, b):
    return (a > b) - (a < b)


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
                      'E1': {'len': 1, 'op': 'POP'},
                      '00': {'len': 0, 'op': 'HALT'}}

    def jmp(self, arg):
        self.IP += twos_comp(arg, 8)

    def jz(self, arg):
        if self.SR[6]:
            self.IP += twos_comp(arg, 8)

    def jnz(self, arg):
        if not self.SR[6]:
            self.IP += twos_comp(arg, 8)

    def js(self, arg):
        if self.SR[4]:
            self.IP += twos_comp(arg, 8)

    def jns(self, arg):
        if not self.SR[4]:
            self.IP += twos_comp(arg, 8)

    def jo(self, arg):
        if self.SR[5]:
            self.IP += twos_comp(arg, 8)

    def jno(self, arg):
        if not self.SR[5]:
            self.IP += twos_comp(arg, 8)

    def mov(self, op, *args):
        pass

    def cmp(self, *args):
        res = cmp(*args)
        if res == -1:
            self.SR[4] = 1
        elif not res:
            self.SR[6] = 1

    def push(self, arg):
        self.ram.put(self.SP,)

    def pop(self, arg):
        pass

    def fetch(self, loc):
        op = self.ram.get(loc)
        lookup = self.table[op]
        func, forward = lookup['op'], lookup['len']
        args = [self.ram.get(hex(int(loc, 16) + i + 1)) for i in range(forward)]
        return func, args, forward

    def load(self, file):
        self.ram.image = load(open(file)).image

    def run(self):
        """
        So far this is a debug method to list what the CPU sees in the code
        """
        self.registers = {'00': 0, '01': 0, '02': 0, '03': 0}
        self.IP = 0
        self.SP = int('0xBF', 16)
        self.SR = [0, 0, 0, 0, 0, 0, 0, 0]
        while True:
            func, args, forward = self.fetch(hex(self.IP))
            print(func, args)
            if func == 'HALT':
                break
            self.IP += forward + 1

if __name__ == '__main__':
    test = CPU()
    with open('BUBBLE2.asm') as file:
        test.load('BUBBLE2.asm')
        test.run()