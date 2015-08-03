from Drip import tohex
import ram
import QuadShot


def concat(l: list, sep=' '):
    out = ''
    for item in l:
        out += item + sep
    return out


def chill(filename, image: ram.RAM, forward: int):
    with open(filename + '.mug', 'w') as file:
        out = [forward]
        for address in range(16 ** 2):
            # noinspection PyTypeChecker
            out.append(image.get(tohex(address)))
        file.write(concat(out))


def reheat(filename, cpu: QuadShot.CPU):
    with open(filename + '.mug', 'r') as file:
