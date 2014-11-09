# pylint: disable:E501
from ram import RAM
from operator import add, sub


class CPU:

    def __init__(self):
        self.registers = {'00': 0, '01': 0, '02': 0, '03': 0}
        self.IP = 0
        self.SP = int('0xBF', 16)
        self.SR = 0
        self.ram = RAM()
        self.table = {'ADD':
                      {'ARG': 2,
                       'OP': add},
                      'SUB':
                      {'ARG': 2,
                       'OP': sub}
                      }

    def fetch(self, loc):
        op = self.ram.get(loc)
        reg = [self.ram.get(loc + x) for x in range(self.table[op]['ARG'])]
        if
