import Drip


class RAM:
    """Simple RAM interface and storage object"""

    def __init__(self, size):
        self.image = [['0000' for _ in range(size)] for _ in range(size)]
        self.size = size

    def get(self, location: str) -> str:
        x, y = divmod(int(location, 16), self.size)
        return self.image[x][y]

    def put(self, location: str, data: str):
        if data == 'C1':
            print(location, data)
        x, y = divmod(int(location, 16), self.size)
        self.image[x][y] = data.zfill(4).upper()

    def show(self):
        print('      ' + ' '.join([Drip.tohex(x).zfill(4).upper() for x in range(self.size)]))
        for y, row in enumerate(self.image):
            print(Drip.tohex(y * self.size), end='  ')
            for item in row:
                print(item, end=' ')
            print('')


if __name__ == "__main__":
    _a = RAM(256)
    _a.put('010E', '12')
    _a.show()
    print(_a.get('11'))
