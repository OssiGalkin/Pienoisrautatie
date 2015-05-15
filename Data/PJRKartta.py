import csv, sys

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import *
from PyQt5.QtCore import QPointF

from Data.PJRRatapala import Ratapala

class Kartta(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)  
        
        self.jatkoPiste = QPointF(1,1)
        self.jatkoKulma = 0.0
        
        self.valittu = None
        self.valittuVanha = None
       
    def addRatapala(self, palaPituus, kulma, scene, sijainti = None, suunta = None):    
        self.addItem(Ratapala(palaPituus, kulma, scene, sijainti, suunta))

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
                    self.addGenericItem(Ratapala(float(row[0]), float(row[1]), self, QPointF(float(row[2]), float(row[3])), QPointF(float(row[4]), float(row[5]))))
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(fileName, reader.line_num, e))
                