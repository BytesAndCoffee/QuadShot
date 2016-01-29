# Visual Display Unit file, separate component with dedicated memory and special data manipulation methods
# from operator import add, sub, mul, mod, floordiv, xor
from registers import Registers, mask
import ram

mask = {value: key for key, value in mask.items()}


class VDU:
    def __init__(self, parent, size):
        self.ram = ram.RAM(size)
        self.registers = Registers(4)
        self.parent = parent
        self.high = [mask['h'].replace('_', str(n)) for n in range(1, 5)]
        self.low = [mask['l'].replace('_', str(n)) for n in range(1, 5)]

    def get(self, loc, arg):
        self.parent.registers[arg[0]] = self.ram.get(loc)

    def put(self, loc, data):
        self.ram.put(loc, data[0])

    def geth(self, loc):
        pixel = list(self.ram.get(loc))
        for channel, register in zip(pixel, self.high):
            self.registers[register] = channel

    def puth(self, loc):
        pixel = []
        for register in self.high:
            pixel.append(self.registers[register])

    def getl(self, loc):
        pixel = list(self.ram.get(loc))
        for channel, register in zip(pixel, self.low):
            self.registers[register] = channel

    def putl(self, loc):
        pixel = []
        for register in self.low:
            pixel.append(self.registers[register])
