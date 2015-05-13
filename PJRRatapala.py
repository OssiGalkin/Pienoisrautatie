from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PyQt5.QtGui import QPainterPath, QDrag

import math
from PyQt5.QtCore import QPointF

from PyQt5.QtCore import Qt, QMimeData

class Ratapala(QGraphicsPathItem):
    def __init__(self, palaPituus, kulma, kayttoliittyma, edellinen=None):

        self.UI = kayttoliittyma        
        alku = self.UI.jatkoPiste 
        
        
        lx = palaPituus * 5 * math.cos(kulma)
        ly = palaPituus * 5 * math.sin(kulma)

        loppu = QPointF(lx,ly)

        self.UI.jatkoPiste  = self.UI.jatkoPiste + loppu

        self.path = QPainterPath()
        self.path.lineTo(loppu) 
        QGraphicsPathItem.__init__(self, self.path)
        self.setPos(alku)

        self.setFlag( QGraphicsItem.ItemIsMovable, True)
        self.setFlag( QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptDrops(True)

        self.alku = alku
        self.loppu = loppu
        self.kulma = kulma  

        self.lahdot = []
        self.seuraava = None

    def mouseReleaseEvent(self, event):
        self.UI.jatkoPiste = self.loppu + self.alku
        self.UI.jatkoKulma = self.kulma
        
    def dragEnterEvent(self, e):
      
        e.accept()
        

    def mouseMoveEvent(self, e):

        #if e.buttons() != Qt.RightButton:
        #    return

        mimeData = QMimeData()

        drag = QDrag(e.widget())
        drag.setMimeData(mimeData)
        paikka = e.pos() - self.alku
        #drag.setHotSpot(paikka.toPoint())

        self.UI.valittu = self
        
        dropAction = drag.exec_(Qt.MoveAction)
        
    
    def dropEvent(self, e):

        #position = e.pos()
        self.UI.valittu.setPos(self.loppu + self.alku)
        
        self.UI.jatkoPiste = self.loppu
        self.UI.jatkoKulma = self.kulma

        e.setDropAction(Qt.MoveAction)
        e.accept()

    def seuraava(self):
        return self.seuraava
        
    def edellinen(self):
        return self.edellinen

    def asetaSeuraava(self, seuraava):
        self.seuraava = seuraava
    
        # Todo onko olemassa
    
    def poistaSeuraava(self):
        self.seuraava = None
        
        #  Todo onko muita
        
    def asetaEdellinen(self, edellinen):
        self.edellinen = edellinen
        
        # Todo onko olemassa
    
    def poistaEdellinen(self):
        self.edellinen = None
    
        # Todo 
    
    def lisaaLahto(self, lahto):
        self.lahdot.append(lahto)
        
    def poistaLahto(self, lahto):
        self.lahdot.remove(lahto)
        
    def __eq__(self, other):
        return self.alku == other.alku and  self.loppu == other.loppu
    

