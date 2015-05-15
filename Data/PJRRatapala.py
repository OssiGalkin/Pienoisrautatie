import math

from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PyQt5.QtGui import QPainterPath, QDrag
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt, QMimeData

class Ratapala(QGraphicsPathItem):
    def __init__(self, palaPituus, kulma, scene, sijainti = None, suunta = None):
  
        self.scene = scene
        self.kulma = kulma
        self.pituus = palaPituus
        
        if sijainti == None:
            self.sijainti = self.scene.jatkoPiste 
            
        else:
            self.sijainti = sijainti
            
        if suunta == None and sijainti == None:
        
            lx = self.pituus * math.cos(kulma)
            ly = self.pituus * math.sin(kulma)
            self.suunta = QPointF(lx,ly)
                
        else:             
            self.kulma = math.atan2(sijainti.y()-suunta.y(), sijainti.x()-suunta.x())
            self.pituus = math.sqrt((sijainti.x()-suunta.x())**2 + (sijainti.y()-suunta.y())**2) 
            self.suunta = suunta
            
        self.scene.jatkoPiste  = self.scene.jatkoPiste + self.suunta

        self.path = QPainterPath()
        self.path.lineTo(self.suunta) 
        QGraphicsPathItem.__init__(self, self.path)
        self.setPos(self.sijainti)

        self.setFlag( QGraphicsItem.ItemIsMovable, True)
        self.setFlag( QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptDrops(True)
        
    def muutaTekstiksi(self):
        return [str(self.pituus), str(self.kulma), str(self.sijainti.x()), str(self.sijainti.y()), str(self.suunta.x()), str(self.suunta.y())]

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
        
    def kaanna(self):
        self.scene.addGenericItem(Ratapala(None, None, self.scene, self.sijainti + self.suunta, -self.suunta))
        self.scene.removeItem(self)
    
