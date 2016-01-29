# register API class file
# TODO: implement [ABCD][HL][HL]
from Drip import registers
registers = list(registers.values())
mask = {'000_': 'l', '00_0': 'h', '0_00': 'x', '_000': 'a'}


def build(reg):
    r = reg.replace('0', '')
    slot = mask[reg.replace(r, '_')]
    return r, slot


class Single:
    def __init__(self, size):
        # super(Single, self).__init__()
        self.val = '0' * int(size / 4)
        self.size = size

    def __add__(self, other):
        return self.val + str(other)

    def assign(self):
        return self

    def get(self):
        return self.val

    def set(self, val):
        self.val = val.zfill(int(self.size / 4))


class Double:
    def __init__(self, l: Single, h: Single):
        self.l, self.h = l, h
        self.size = self.l.size * 2

    def get(self):
        return self.h.get() + self.l.get()

    def set(self, value):
        value = value.zfill(int(self.size / 4))
        self.h.set(value[:int(self.size / 8)])
        self.l.set(value[int(self.size / 8):])

    def assign(self):
        return self


class Adjacent:
    def __init__(self, y: Double, z: Double):
        self.y, self.z = y, z
        self.size = self.y.size * 2

    def get(self):
        return self.y.get() + self.z.get()

    def set(self, value):
        value = value.zfill(int(self.size / 4))
        self.y.set(value[:int(self.size / 8)])
        self.z.set(value[int(self.size / 8):])

    def assign(self):
        return self


def build_register(size):
    l, h = Single(size), Single(size)
    x = Double(l, h)
    loc = locals()
    return tuple([loc[inst].assign() for inst in ['x', 'h', 'l']])


class Register(dict):
    def __init__(self, size):
        dict.__init__(self, dict(zip(['x', 'h', 'l'], build_register(size))))

    def add_adjacent(self, adj):
        dict.__setitem__(self, 'a', adj)

    def __setitem__(self, key, value):
        dict.__getitem__(self, key).set(value)

    def __getitem__(self, item):
        return dict.__getitem__(self, item).get()

    def assign(self, item):
        return dict.__getitem__(self, item).assign()


class Registers(dict):
    def __init__(self, size):
        dict.__init__(self)
        dict.update(self, dict(zip([str(n) for n in range(1, 5)], [Register(size) for _ in range(12)])))
        doubles = [dict.__getitem__(self, k).assign('x') for k in [str(n) for n in range(1, 5)]]
        doubles.append(doubles[0])
        adjacents = [Adjacent(doubles[i], doubles[i + 1]) for i in range(4)]
        for i in range(1, 5):
            dict.__getitem__(self, str(i)).add_adjacent(adjacents[i - 1])

    def __getitem__(self, item):
        reg, slot = build(item)
        return dict.__getitem__(self, reg)[slot]

    def __setitem__(self, key, value):
        reg, slot = build(key)
        dict.__getitem__(self, reg)[slot] = value


if __name__ == '__main__':
    r = Registers(16)
    r['0100'] = '12345678'
    r['0020'] = 'FFFF'
    r['0003'] = '1111'
    for i in ['0100', '0200', '0300', '1000', '2000', '3000', '4000']:
        print(i, r[i])
