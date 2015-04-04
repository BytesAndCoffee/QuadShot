import Drip
class RAM:
    """Simple RAM interface and storage object"""
    def __init__(self):
        self.image = [['00' for _ in range(16)] for _ in range(12)] + [['20' for _ in range(16)] for _ in range(4)]

    def get(self, location: str) -> str:
        x, y = divmod(int(location, 16), 16)
        return self.image[x][y]

    def put(self, location: str, data: str):
        if data == 'C1':
            print(location, data)
        x, y = divmod(int(location, 16), 16)
        self.image[x][y] = data.zfill(2).upper()

    def show(self):
        print('    00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F')
        for y, row in enumerate(self.image):
            print(Drip.tohex(y*16), end='  ')
            for item in row:
                print(item, end=' ')
            print('')


if __name__ == "__main__":
    _a = RAM()
    _a.put('1E', '12')
    _a.show()
    print(_a.get('11'))
