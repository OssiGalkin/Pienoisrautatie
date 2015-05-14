import math

from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PyQt5.QtGui import QPainterPath, QDrag
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt, QMimeData

class Ratapala(QGraphicsPathItem):
    def __init__(self, palaPituus, kulma, scene, sijaintiX=None, sijaintiY=None):
  
        self.scene = scene
        self.kulma = kulma
        self.pituus = palaPituus
        
        if sijaintiX == None or sijaintiY == None:
            self.sijainti = self.scene.jatkoPiste 
        else:
            self.sijainti = QPointF(sijaintiX,sijaintiY)
        
        lx = self.pituus * math.cos(self.kulma)
        ly = self.pituus * math.sin(self.kulma)

        self.suunta = QPointF(lx,ly)

        self.scene.jatkoPiste  = self.scene.jatkoPiste + self.suunta

        self.path = QPainterPath()
        self.path.lineTo(self.suunta) 
        QGraphicsPathItem.__init__(self, self.path)
        self.setPos(self.sijainti)

        self.setFlag( QGraphicsItem.ItemIsMovable, True)
        self.setFlag( QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptDrops(True)
        
    def muutaTekstiksi(self):
        return [str(self.pituus), str(self.kulma), str(self.sijainti.x()), str(self.sijainti.y())]

    def mouseReleaseEvent(self, event):
        self.scene.jatkoPiste = self.suunta + self.sijainti
        self.scene.jatkoKulma = self.kulma
        self.scene.valittu = self
        
    def dragEnterEvent(self, e):
        e.accept()

    def mouseMoveEvent(self, e):
        
        mimeData = QMimeData()
        drag = QDrag(e.widget())
        drag.setMimeData(mimeData)
        self.scene.valittu = self
        dropAction = drag.exec_(Qt.MoveAction)
        
    def dropEvent(self, e):

        uusiSijainti = self.suunta + self.sijainti
        
        self.scene.valittu.setPos(uusiSijainti)
        self.scene.valittu.sijainti = uusiSijainti
        
        self.scene.jatkoPiste = self.scene.valittu.sijainti + self.scene.valittu.suunta
        self.scene.jatkoKulma = self.scene.valittu.kulma
        e.setDropAction(Qt.MoveAction)
        e.accept()

    def alkuNaapurit(self, sijainti):
        return self.scene.self.itemAt(self.sijainti)
        
    def loppuNaapurit(self, sijainti):
        return self.scene.self.itemAt(self.sijainti + self.self.suunta)
