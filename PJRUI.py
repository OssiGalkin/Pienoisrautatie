from PyQt5.QtGui import *
from PyQt5 import uic
from PJRKartta import Kartta
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPointF
from PJRRatapala import Ratapala
import math

form_class = uic.loadUiType("Junarata.ui")[0]      


class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.palaPituus = 0
        self.palaKulma = 0.0
        
        self.jatkoPiste = QPointF(0,0)
        self.jatkoKulma = 0.0
        
        self.valittu = None

        self.SliderPituus.valueChanged.connect(self.setPalaPituus)
        self.SliderPituus.valueChanged.connect(self.lcdNumber.display)
        self.SliderKulma.valueChanged.connect(self.setPalaKulma)
        self.SliderKulma.valueChanged.connect(self.lcdNumber_2.display)
        
        exitAction = QAction(QIcon('exit24.png'), 'Lopeta', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        openFile = QAction(QIcon('open.png'), 'Avaa', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Avaa tallennettu rata')
        openFile.triggered.connect(self.showOpenDialog)
        
        newFile = QAction(QIcon('new.png'), 'Uusi', self)
        newFile.setShortcut('Ctrl+N')
        newFile.setStatusTip('Luo uusi tyhjä rata')
        newFile.triggered.connect(self.showNewDialog)
        
        saveFile = QAction(QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Tallenna rata')
        saveFile.triggered.connect(self.showSaveDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openFile)
        fileMenu.addAction(newFile) 
        fileMenu.addAction(saveFile)         

        self.scene =  Kartta()
        self.graphicsView.setScene(self.scene)
  
        self.BtnPuu.clicked.connect(self.buttonClicked)            
        self.BtnPoista.clicked.connect(self.poistaPainettu)        
        self.BtnYhdista.clicked.connect(self.buttonClicked)
        
        
        self.BtnSuora.clicked.connect(self.suoraPainettu)
        self.BtnMutkaVasen.clicked.connect(self.mutkaVasenPainettu)
        self.BtnMutkaOikea.clicked.connect(self.mutkaOikeaPainettu)
        
        self.statusBar()
        self.center()

        
    def suoraPainettu(self):

        self.scene.addGenericItem(Ratapala(self.palaPituus, self.jatkoKulma, self))
        
    def mutkaOikeaPainettu(self):
    
        self.jatkoKulma = self.jatkoKulma + self.palaKulma
        self.scene.addGenericItem(Ratapala(self.palaPituus, self.jatkoKulma, self))
    
    def mutkaVasenPainettu(self):
    
        #print(self.jatkoPiste.x(), self.jatkoPiste.y())
        self.jatkoKulma = self.jatkoKulma - self.palaKulma
        self.scene.addGenericItem(Ratapala(self.palaPituus, self.jatkoKulma, self))
    
    def poistaPainettu(self):
        self.scene.removeItem(self.valittu)
    
    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def buttonClicked(self):
      
        sender = self.sender()
        self.statusBar().showMessage('Nappia: ' + sender.text() + ' painettiin')
        
    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Viesti',
            "Haluatko varmasti lopettaa?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()    
            
    def showOpenDialog(self):

        fname, _ = QFileDialog.getOpenFileName(self, 'Avaa', '/home')
        # TODO Tiedostotyyppi
        
        if fname:
            f = open(fname, 'r')
            with f:        
                data = f.read()
                self.statusBar().showMessage(data)
            
    def showSaveDialog(self):

        fileName = QFileDialog.getSaveFileName(self, 'Dialog Title', '/path/to/default/directory')
        # TODO Tiedostotyyppi
        # TODO
        self.statusBar().showMessage(str(fileName))
        
    def showNewDialog(self, event):
        
        reply = QMessageBox.question(self, 'Viesti',
            "Uusi rata? Menetät vanhan radan tallentamattomat tiedot.", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.scene =  Kartta()
            self.graphicsView.setScene(self.scene)
            #self.statusBar().showMessage('Nyt tulisi tyhjä kartta')
            # TODO
            
    def setPalaPituus(self, arvo):
        self.palaPituus = arvo
        
    def setPalaKulma(self, arvo):
        self.palaKulma = math.radians(arvo)