#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
##
## Ossi Galkin
## CSE-A1121 Ohjelmoinnin peruskurssi Y2 (5 op) Projektityö
## Aihepiiri: grafiikka, työ 110: Pienoisrautatie
##
#############################################################################

import sys

from PyQt5.QtWidgets import QApplication

from PJRUI import MyWindowClass
from PJRKartta import Kartta

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()