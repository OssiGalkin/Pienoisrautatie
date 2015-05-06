from PJRUI import MyWindowClass
from PJRKartta import Kartta

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    Kartta()
    myWindow.show()
    app.exec_()