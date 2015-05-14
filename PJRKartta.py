import csv, sys

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import *
from PyQt5.QtCore import QPointF

from PJRRatapala import Ratapala

class Kartta(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)  
        
        self.jatkoPiste = QPointF(0,0)
        self.jatkoKulma = 0.0
        
        self.valittu = None
       
    def addGenericItem(self, item):    
        self.addItem(item)

    def tallenna(self, fileName):
    
        with open(fileName, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            try:
                for i in self.items():
                    spamwriter.writerow(i.muutaTekstiksi())
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(fileName, reader.line_num, e))

    def lataa (self, fileName):

        with open(fileName, newline='') as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    self.addGenericItem(Ratapala(float(row[0]), float(row[1]), self, float(row[2]), float(row[3])))
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(fileName, reader.line_num, e))
                