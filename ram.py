class RAM:
    '''Simple RAM interface and storage object'''
    def __init__(self):
        self.image = [[hex(0)+'0' for _ in range(16)] for _ in range(16)]

    def get(self, location):
        x, y = divmod(int(location, 16), 16)
        return self.image[x][y]

    def put(self, location, data):
        x, y = divmod(int(location, 16), 16)
        self.image[x][y] = '0x'+data

    def show(self):
        for line in self.image:
            print(line)


if __name__ == "__main__":
    a = RAM()
    a.put('11', '12')
    a.show()
    print(a.get('11'))
