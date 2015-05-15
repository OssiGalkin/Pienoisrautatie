import csv, sys

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import *
from PyQt5.QtCore import QPointF

from Data.PJRRatapala import Ratapala
from PyQt5.QtCore import Qt
class Kartta(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)  
        
        self.jatkoPiste = QPointF(1,1)
        self.jatkoKulma = 0.0
        
        self.valittu = None
        self.valittuVanha = None
       
    def addRatapala(self, palaPituus, kulma, sijainti = None, suunta = None):    
        item = Ratapala(palaPituus, kulma, self, sijainti, suunta)
        pen = QPen(Qt.black, 1.5, Qt.SolidLine)
        
        item.setPen(pen)
        self.addItem(item)

    def tallenna(self, fileName):
        '''
        Tallentaa kartan kaikki ratapalat csv tiedostoon
        '''
        with open(fileName, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            try:
                for i in self.items():
                    spamwriter.writerow(i.muutaTekstiksi())
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(fileName, reader.line_num, e))

    def lataa (self, fileName):
        '''
        Lataa ratapaloja csv tiedostosta kartalle. Kartalla voi olla jo ennestään ratapaloja.
        '''
        with open(fileName, newline='') as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    self.addRatapala(None, None, QPointF(float(row[0]), float(row[1])), QPointF(float(row[2]), float(row[3])))
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(fileName, reader.line_num, e))
                