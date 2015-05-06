from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Kartta(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)
        self.addRectangle()
        
    def addRectangle(self):    
        item =  QGraphicsRectItem(0, 0, 60, 40)
        item.setFlag( QGraphicsItem.ItemIsMovable, True)
        item.setFlag( QGraphicsItem.ItemIsSelectable, True)
        self.addItem(item)
        
    def addGenericItem(self, item):    
        self.addItem(item)