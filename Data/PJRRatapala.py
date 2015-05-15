import math

from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PyQt5.QtGui import QPainterPath, QDrag
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt, QMimeData

class Ratapala(QGraphicsPathItem):
    def __init__(self, pituus, kulma, scene, sijainti = None, suunta = None):
        '''
        Luo uuden ratapalan, joko sen pituuden ja kulman avulla, jolloin pala lisätään edellisen perään, tai käyttäen koordinaatteja sijainti ja suunta.
        Tämän konstruktorin toiminta on hieman omalaatuinen, se on selitetty seikkaperäisesti työn dokumentissa.
        '''
        self.scene = scene
        self.kulma = kulma
        self.pituus = pituus
        
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
        ''' 
        Luo tekstimuotoisen esityksen ratapalasta
        '''
        return [str(self.sijainti.x()), str(self.sijainti.y()), str(self.suunta.x()), str(self.suunta.y())]
        
    def mouseReleaseEvent(self, event):
        '''
        "Valitsee" Ratapalan kun sitä klikataan hiirellä
        '''
        self.scene.jatkoPiste = self.suunta + self.sijainti
        self.scene.jatkoKulma = self.kulma
        self.scene.valittu = self
        
    def dragEnterEvent(self, e):
        '''
        Sallii ratapalan draggaamisen. Metodi on Qt:ta varten.
        '''
        e.accept()

    def mouseMoveEvent(self, e):
        '''
        Luo ratapalsata Mime tiedot, kun sitä liikuttaa
        '''
        mimeData = QMimeData()
        drag = QDrag(e.widget())
        drag.setMimeData(mimeData)
        self.scene.valittu = self
        dropAction = drag.exec_(Qt.MoveAction)
        
    def dropEvent(self, e):
        '''
        Liittää palan päälle tiputettavan ratapalan palan perään
        '''
    
        uusiSijainti = self.suunta + self.sijainti
        
        self.scene.valittu.setPos(uusiSijainti)
        self.scene.valittu.sijainti = uusiSijainti
        
        self.scene.jatkoPiste = self.scene.valittu.sijainti + self.scene.valittu.suunta
        self.scene.jatkoKulma = self.scene.valittu.kulma
        e.setDropAction(Qt.MoveAction)
        e.accept()

    def annaNaapurit(self):
        '''
        Palauttaa naapuripalat listana 
        '''
        return self.scene.collidingItems(self)
        
    def kaanna(self):
        '''
        Vaihtaa alku ja loppupisteen paikat keskenään
        '''
        self.scene.addGenericItem(Ratapala(None, None, self.scene, self.sijainti + self.suunta, -self.suunta))
        self.scene.removeItem(self)
    
