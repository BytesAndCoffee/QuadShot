# register API class file
from Drip import registers
registers = list(registers.values())
print(registers)
mask = {'000_': 'l', '00_0': 'h', '0_00': 'x'}


def build(reg):
    r = reg.replace('0', '')
    slot = mask[reg.replace(r, '_')]
    return r, slot


class Double:
    def __init__(self, l, h):
        self.l, self.h = l, h

    def get(self):
        return self.h.get() + self.l.get()

    def __repr__(self):
        return self.get()

    def set(self, value):
        value = value.zfill(8)
        self.h.set(value[:4])
        self.l.set(value[4:])

    def assign(self):
        return self


class Single:
    def __init__(self):
        # super(Single, self).__init__()
        self.val = '0000'

    def __get__(self, instance, owner):
        print(instance, owner)
        return self.val

    def __set__(self, instance, value):
        print(instance)
        self.val = value

    def __repr__(self):
        return self.val

    def __add__(self, other):
        return self.val + str(other)

    def assign(self):
        return self

    def get(self):
        return self.val

    def set(self, val):
        self.val = val


def build_register():
    l, h = Single(), Single()
    x = Double(l, h)
    loc = locals()
    return tuple([loc[inst].assign() for inst in ['x', 'h', 'l']])


class Register(dict):
    def __init__(self):
        dict.__init__(self, dict(zip(['x', 'h', 'l'], build_register())))

    def __setitem__(self, key, value):
        dict.__getitem__(self, key).set(value)

    def __getitem__(self, item):
        return dict.__getitem__(self, item).get()


class Registers(dict):
    def __init__(self):
        dict.__init__(self)
        dict.update(self, dict(zip([str(n) for n in range(1,5)], [Register() for _ in range(12)])))

    def __getitem__(self, item):
        reg, slot = build(item)
        return dict.__getitem__(self, reg)[slot]

    def __setitem__(self, key, value):
        reg, slot = build(key)
        print('1', key, reg, slot, dict.__getitem__(self, reg))
        dict.__getitem__(self, reg)[slot] = value
        print('2', key, reg, slot, dict.__getitem__(self, reg))


if __name__ == '__main__':
    r = Registers()
    r['0100'] = '123456789'
    r['0020'] = 'FFFF'
    r['0003'] = '1111'
    for i in registers:
        print(i, r[i])