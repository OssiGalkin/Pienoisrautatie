
from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PyQt5.QtGui import QPainterPath

# Ratapala on kahden liitoksen välissä oleva näkyvä radan osa
class Ratapala(QGraphicsPathItem):
    def __init__(self, alku, kpiste, loppu, edellinen=None):
    
        self.path = QPainterPath()
        
        self.path.quadTo(kpiste,loppu)
        
        #self.path.lineTo(loppu)

        QGraphicsPathItem.__init__(self, self.path)

        self.setFlag( QGraphicsItem.ItemIsMovable, True)
        self.setFlag( QGraphicsItem.ItemIsSelectable, True)
        self.setPos(alku)
        
        self.alku = alku
        self.kpiste = kpiste
        self.loppu = loppu
        
        # TODO parent systeemi
        # alku -> ratapala ->loppu
    # The dragEnterEvent() handler is called when a Drag and Drop element  dragged into the element's area.
    #def dragEnterEvent(self, e): pass
  
    # The dragLeaveEvent() handler is called when a Drag and Drop element is dragged away element's area.    
    #def dragLeaveEvent(self, e): pass
    
    #The dropEvent() handler is called when a Drag and Drop element is dropped onto an item (i.e., when the mouse button is released over the item while dragging).    

        self.lahdot = []
        self.seuraava = None
        
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
    

    def dropEvent(self, e):
    
        # QtWidgets.selectedItems()[0]
    
        pass
        