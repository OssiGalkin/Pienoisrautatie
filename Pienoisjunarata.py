#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
##
## Ossi Galkin
## CSE-A1121 Ohjelmoinnin peruskurssi Y2 (5 op) Projektityö
## Aihepiiri: grafiikka, työ 110: Pienoisrautatie
##
## Käyttö: aja tämä tiedosto
## Vaatimukset: Python 3.4 tulkki ja PyQt 5, testattu: Windows 7
##
#############################################################################

import sys
from PyQt5.QtWidgets import QApplication
from Data.PJRUI import Ikkuna

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Ikkuna(None)
    myWindow.show()
    app.exec_()