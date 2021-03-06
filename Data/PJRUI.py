import math

from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPointF

from Data.PJRKartta import Kartta

form_class = uic.loadUiType("Junarata.ui")[0]      

class Ikkuna(QMainWindow, form_class):
    def __init__(self, parent=None):
        '''
        Luo ohjelman ikkunan, sekä lisää kaikkiin nappuloihin ja muihin tarvittavan toiminnalisuuden.
        '''
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        self.palaPituus = 0
        self.palaKulma = 0.0

        self.scene =  Kartta()
        self.graphicsView.setScene(self.scene)
  
        self.statusBar()
        self.center()
 
        self.SliderPituus.valueChanged.connect(self.setPalaPituus)
        self.SliderPituus.valueChanged.connect(self.lcdNumber.display)
        self.SliderPituus.setToolTip("Asettaa lisättävän ratapalan pituuden")
        self.lcdNumber.setToolTip("Näyttää lisättävän ratapalan pituuden")
        self.SliderPituus.setValue(7)
        
        self.SliderKulma.valueChanged.connect(self.setPalaKulma)
        self.SliderKulma.valueChanged.connect(self.lcdNumber_2.display)
        self.SliderKulma.setToolTip("Asettaa lisättävän mutkan kulman")
        self.lcdNumber_2.setToolTip("Näyttää lisättävän mutkan kulman")
        self.SliderKulma.setValue(12)
        
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
        
        saveFile = QAction(QIcon('save.png'), 'Tallenna', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Tallenna rata')
        saveFile.triggered.connect(self.showSaveDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Tiedosto')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openFile)
        fileMenu.addAction(newFile) 
        fileMenu.addAction(saveFile)         
        
        self.BtnPoista.clicked.connect(self.poistaPainettu)
        self.BtnPoista.setToolTip("Poistaa valitun palan") 
        
        self.BtnValitseYhdistettavaksi.clicked.connect(self.valitseYhdistettavaksi)
        self.BtnValitseYhdistettavaksi.setToolTip("Yhdistää valitun palan myöhemmin valittavaan palaan") 
        
        self.BtnYhdista.clicked.connect(self.yhdistaValitut)
        self.BtnYhdista.setToolTip("Yhdistää valitun palan aiemmin valituun palaan") 
        
        self.BtnSuora.clicked.connect(self.suoraPainettu)
        self.BtnSuora.setToolTip("Luo kartalle uuden suoran ratapalan") 
        
        self.BtnMutkaVasen.clicked.connect(self.mutkaVasenPainettu)
        self.BtnMutkaVasen.setToolTip("Luo kartalle uuden vasemmalle kääntyvän ratapalan") 
        
        self.BtnMutkaOikea.clicked.connect(self.mutkaOikeaPainettu)
        self.BtnMutkaOikea.setToolTip("Luo kartalle uuden oikealle kääntyvän ratapalan") 
        
        self.BtnKaanna.clicked.connect(self.kaannaPainettu)
        self.BtnKaanna.setToolTip("Kääntää valitun ratapalan") 

    def suoraPainettu(self):

        self.scene.addRatapala(self.palaPituus, self.scene.jatkoKulma)
        
    def mutkaOikeaPainettu(self):
    
        self.scene.jatkoKulma = self.scene.jatkoKulma + self.palaKulma
        self.scene.addRatapala(self.palaPituus, self.scene.jatkoKulma)
    
    def mutkaVasenPainettu(self):
    
        self.scene.jatkoKulma = self.scene.jatkoKulma - self.palaKulma
        self.scene.addRatapala(self.palaPituus, self.scene.jatkoKulma)
    
    def poistaPainettu(self):
    
        self.scene.removeItem(self.scene.valittu)
    
    def valitseYhdistettavaksi(self):
    
        self.scene.valittuVanha = self.scene.valittu
        self.statusBar().showMessage('Valitse vielä pala johon halua yhdistää')
    
    def yhdistaValitut(self):
    
        if self.scene.valittu != None and self.scene.valittuVanha != None:
            sijainti = self.scene.valittuVanha.sijainti + self.scene.valittuVanha.suunta
            suunta = self.scene.valittu.sijainti + self.scene.valittu.suunta
            self.scene.addRatapala(None, None, sijainti, suunta - sijainti)
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Viesti',
            "Haluatko varmasti lopettaa?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()    
            
    def showOpenDialog(self):

        fileName, _ = QFileDialog.getOpenFileName(self, 'Avaa', '/path/to/default/directory')
        
        if fileName != '':
            self.scene =  Kartta()
            self.graphicsView.setScene(self.scene)
            self.scene.lataa(fileName)
            
    def showSaveDialog(self):

        fileName, _ = QFileDialog.getSaveFileName(self, 'Tallenna', '/path/to/default/directory')   
        
        if fileName != '':
            self.scene.tallenna(fileName)
        
    def showNewDialog(self, event):
        
        reply = QMessageBox.question(self, 'Viesti',
            "Uusi rata? Menetät vanhan radan tallentamattomat tiedot.", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.scene =  Kartta()
            self.graphicsView.setScene(self.scene)
            
    def setPalaPituus(self, arvo):
    
        self.palaPituus = arvo
        
    def setPalaKulma(self, arvo):
    
        self.palaKulma = math.radians(arvo)
        
    def kaannaPainettu(self):
    
        if self.scene.valittu != None:
            self.scene.valittu.kaanna()

        