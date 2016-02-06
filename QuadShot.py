#!/usr/bin/env python

from operator import add, sub, mul, mod, floordiv, xor
from functools import partial
from registers import Registers
import sys

import ram
import Drip


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
        self.registers = Registers()  # dict.fromkeys(Drip.registers.values(), '0000')
        self.IP = 0
        self.init = 0
        self.CSP = int('0xFFFF', 16)
        self.GSP = int('0xFEFF', 16)
        self.MSP = int('0xFDFF', 16)
        self.PSP = self.MSP
        self.SR = [0, 0, 0, 0, 0, 0, 0, 0]
        self.jumped = 0
        self.ram = ram.RAM()
        self.stdout = []
        self.stack = []
        self.debug = ''
        self.table = {'00A0': {'len': 2, 'op': add},
                      '00A1': {'len': 2, 'op': sub},
                      '00A2': {'len': 2, 'op': mul},
                      '00A3': {'len': 2, 'op': floordiv},
                      '00A4': {'len': 1, 'op': self.inc},
                      '00A5': {'len': 1, 'op': self.dec},
                      '00A6': {'len': 2, 'op': mod},
                      '00A7': {'len': 2, 'op': xor},
                      '00B0': {'len': 2, 'op': add},
                      '00B1': {'len': 2, 'op': sub},
                      '00B2': {'len': 2, 'op': mul},
                      '00B3': {'len': 2, 'op': floordiv},
                      '00B6': {'len': 2, 'op': mod},
                      '00B7': {'len': 2, 'op': xor},
                      '00C0': {'len': 1, 'op': self.jmp},
                      '00C1': {'len': 1, 'op': self.jz},
                      '00C2': {'len': 1, 'op': self.jnz},
                      '00C3': {'len': 1, 'op': self.js},
                      '00C4': {'len': 1, 'op': self.jns},
                      '00C5': {'len': 1, 'op': self.jo},
                      '00C6': {'len': 1, 'op': self.jno},
                      '00D0': {'len': 2, 'op': self.mov},
                      '00D1': {'len': 2, 'op': self.mov},
                      '00D2': {'len': 2, 'op': self.mov},
                      '00D3': {'len': 2, 'op': self.mov},
                      '00D4': {'len': 2, 'op': self.mov},
                      '00DA': {'len': 2, 'op': self.cmp},
                      '00DB': {'len': 2, 'op': self.cmp},
                      '00DC': {'len': 2, 'op': self.cmp},
                      '00DD': {'len': 2, 'op': self.cmp},
                      '00E0': {'len': 1, 'op': self.push},
                      '00E1': {'len': 1, 'op': self.pop},
                      '00E2': {'len': 1, 'op': self.push},
                      '00E3': {'len': 1, 'op': self.pop},
                      '00EA': {'len': 1, 'op': self.push},
                      '00EB': {'len': 1, 'op': self.pop},
                      '00EC': {'len': 1, 'op': self.push},
                      '00ED': {'len': 1, 'op': self.pop},
                      '00F0': {'len': 1, 'op': self.out},
                      '00F1': {'len': 1, 'op': self.out},
                      '00F2': {'len': 1, 'op': self.out},
                      '0A00': {'len': 1, 'op': None},
                      '0B00': {'len': 1, 'op': None},
                      '0C00': {'len': 1, 'op': self.swap},
                      '0000': {'len': 0, 'op': 'HALT'}}

    def math(self, func, args):
        a = args[0]
        if func == self.inc:
            return self.inc(args)
        elif func == self.dec:
            return self.dec(args)
        args[0] = func(*args)
        if args[0] > (2**16)-1:
            args[0] = mod(args[0], (2**16)-1)
            self.SR = 4
        if cmp(a, args[0]) == 0:
            self.SR = 2
        elif cmp(a, args[0]) == -1:
            self.SR = 8
        return args[0]

    def jmp(self, arg):
        jump = twos_comp(int(arg[0], 16), 16)
        # print('Added', jump, 'to IP')
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
        if op == '00D0':
            self.registers[args[0]] = args[1]
        elif op == '00D1':
            self.registers[args[0]] = self.ram.get(args[1])
        elif op == '00D2':
            self.ram.put(args[0], self.registers[args[1]])
        elif op == '00D3':
            self.registers[args[0]] = self.ram.get(self.registers[args[1]])
        elif op == '00D4':
            self.ram.put(self.registers[args[0]], self.registers[args[1]])

    def cmp(self, op: str, args: list):
        self.SR = 0
        if op == '00DA':
            args = [self.registers[args[0]], self.registers[args[1]]]
        elif op == '00DB':
            args = [self.registers[args[0]], args[1]]
        elif op == '00DC':
            args = [self.registers[args[0]], self.ram.get(args[1])]
        elif op == '00DD':
            args = [self.ram.get(self.registers[args[0]]), args[1]]
        res = cmp(*map(partial(int, base=16), args))
        if res == 0:
            self.SR = 2
        elif res == -1:
            self.SR = 8

    def push(self, stack, arg):
        if stack == 'call':
            self.ram.put(Drip.tohex(self.CSP), arg)
            self.CSP -= 1
        elif stack == 'global':
            self.ram.put(Drip.tohex(self.GSP), arg)
            self.GSP -= 1
        elif stack == 'private':
            self.ram.put(Drip.tohex(self.PSP), arg)
            self.PSP -= 1

    def pop(self, stack):
        if stack == 'call':
            self.CSP += 1
            return self.ram.get(Drip.tohex(self.CSP))
        elif stack == 'global':
            self.GSP += 1
            return self.ram.get(Drip.tohex(self.GSP))
        elif stack == 'private':
            self.PSP += 1
            return self.ram.get(Drip.tohex(self.PSP))

    def out(self, op, arg):
        if op[3] == '0':
            self.stdout.append(arg[0])
        elif op[3] == '1':
            self.stdout.append(self.registers[arg[0]])
        else:
            self.stdout.append(self.ram.get(self.registers[arg[0]]))
        print(self.stdout)

    def swap(self, arg):
        data = self.registers[arg[0]]
        half = int(len(data) / 2)
        self.registers[arg[0]] = data[half:] + data[:half]

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

    def load(self, code, name):
        loaded = Drip.load(code, name)
        self.ram.image, self.init = loaded[0].image, loaded[1]

    def run(self):
        self.registers = Registers()
        self.IP = 0 + self.init
        print('init', self.init)
        self.CSP = int('0xFFFF', 16)
        self.GSP = int('0xFEFF', 16)
        self.MSP = int('0xFDFF', 16)
        self.SR = 0
        self.debug = ''
        while True:
            self.jumped = 0
            func, args, forward, op = self.fetch(hex(self.IP))
            if func == 'HALT':
                break
            elif op[2] == 'A':
                self.registers[args[0]] = Drip.tohex(
                    self.math(func, [int(self.registers[register], 16) for register in args]))
            elif op[2] == 'B':
                self.registers[args[0]] = Drip.tohex(
                    self.math(func, [int(self.registers[args[0]], 16), int(args[1], 16)]))
            elif op[2] == 'D' or op[2] == 'F':
                func(op, args)
            elif op[1] == 'A':
                self.push('call', Drip.tohex(self.IP))
                print('call branch')
                self.IP = int(args[0], 16)
                self.MSP -= 256
                self.PSP = self.MSP
                continue
            elif op[1] == 'B':
                self.IP = int(self.pop('call'), 16)
                self.MSP += 265
                self.PSP = self.MSP
            elif op == '00E0':
                self.push('private', self.registers[args[0]])
            elif op == '00E1':
                self.registers[args[0]] = self.pop('private')
            elif op == '00EA':
                self.push('global', self.registers[args[0]])
            elif op == '00EB':
                self.registers[args[0]] = self.pop('global')
            else:
                func(args)
            if not self.jumped:
                self.IP += forward + 1
        print('out', self.stdout)
        print(''.join(map(chr, map(partial(int, base=16), self.stdout))))
        print('Finished')


if __name__ == '__main__':
    test = CPU()
    if len(sys.argv) < 2:
        name = 'BUBBLE2'
    else:
        name = sys.argv[1]
    
    with open(name + '.drip') as file:
        test.load(file, name)
        test.run()
