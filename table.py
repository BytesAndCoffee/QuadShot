import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Table(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setmydata(self):

        horHeaders = [hex(n) for n in range(16)]
        for n, l in enumerate(self.data):
            for m, item in enumerate(l):
                newitem = QTableWidgetItem(item)
                self.setItem(n, m, newitem)


def showTable(data):
    app = QApplication(sys.argv)
    table = Table(data, 16, 16)
    table.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    showTable([[i + o for i in range(16)] for o in range(16)])