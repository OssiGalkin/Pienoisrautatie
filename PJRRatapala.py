from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PyQt5.QtGui import QPainterPath, QDrag

import math
from PyQt5.QtCore import QPointF

from PyQt5.QtCore import Qt, QMimeData

class Ratapala(QGraphicsPathItem):
    def __init__(self, palaPituus, kulma, kayttoliittyma, edellinen=None):

        self.UI = kayttoliittyma        
        sijainti = self.UI.jatkoPiste 
        
        
        lx = palaPituus * 5 * math.cos(kulma)
        ly = palaPituus * 5 * math.sin(kulma)

        suunta = QPointF(lx,ly)

        self.UI.jatkoPiste  = self.UI.jatkoPiste + suunta

        self.path = QPainterPath()
        self.path.lineTo(suunta) 
        QGraphicsPathItem.__init__(self, self.path)
        self.setPos(sijainti)

        self.setFlag( QGraphicsItem.ItemIsMovable, True)
        self.setFlag( QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptDrops(True)

        self.sijainti = sijainti
        self.suunta = suunta
        self.kulma = kulma  

        self.lahdot = []
        self.seuraava = None

    def mouseReleaseEvent(self, event):
        self.UI.jatkoPiste = self.suunta + self.sijainti
        self.UI.jatkoKulma = self.kulma
        self.UI.valittu = self
        
    def dragEnterEvent(self, e):
      
        e.accept()
        

    def mouseMoveEvent(self, e):

        #if e.buttons() != Qt.RightButton:
        #    return

        mimeData = QMimeData()

        drag = QDrag(e.widget())
        drag.setMimeData(mimeData)
        paikka = e.pos() - self.sijainti
        #drag.setHotSpot(paikka.toPoint())

        self.UI.valittu = self
        
        dropAction = drag.exec_(Qt.MoveAction)
        
    
    def dropEvent(self, e):

        #position = e.pos()
        self.UI.valittu.setPos(self.suunta + self.sijainti)
        
        self.UI.jatkoPiste = self.suunta
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
        return self.sijainti == other.sijainti and  self.suunta == other.suunta
    

