import Drip
class RAM:
    """Simple RAM interface and storage object"""
    def __init__(self):
        self.image = [['0000' for _ in range(256)] for _ in range(252)] + [['0020' for _ in range(256)] for _ in range(4)]

    def get(self, location: str) -> str:
        x, y = divmod(int(location, 16), 256)
        return self.image[x][y]

    def put(self, location: str, data: str):
        if data == 'C1':
            print(location, data)
        x, y = divmod(int(location, 16), 256)
        self.image[x][y] = data.zfill(4).upper()

    def show(self):
        print('      '+' '.join([Drip.tohex(x).zfill(4).upper() for x in range(256)]))
        for y, row in enumerate(self.image):
            print(Drip.tohex(y*256), end='  ')
            for item in row:
                print(item, end=' ')
            print('')


if __name__ == "__main__":
    _a = RAM()
    _a.put('010E', '12')
    _a.show()
    print(_a.get('11'))
