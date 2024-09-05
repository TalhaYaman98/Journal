import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow,QToolTip,QMessageBox
from PyQt5.QtGui import QIcon,QColor
from Interface import Ui_MainWindow
from datetime import datetime
import os

class pencere(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("GÜNLÜK")
        self.setToolTip("DevamEt!!")
        self.msgBox = QMessageBox()
        
        self.ui.pushButton.clicked.connect(self.yazma)
        self.ui.pushButton_2.clicked.connect(self.temizleme)
        self.ui.pushButton_3.clicked.connect(self.okuma)
        self.ui.pushButton_4.clicked.connect(self.sil)

        result = os.listdir("C:/Users/Talha/Documents/Gunluk") 
        for dosya in result:      
            if dosya.endswith(".txt"):
                self.ui.listWidget.addItem(str(dosya))
        self.ui.listWidget.setCurrentRow(0)

        self.simdi = datetime.now()
        year = self.simdi.year
        month = self.simdi.month
        day = self.simdi.day
        minute = self.simdi.minute
        second = self.simdi.second
        hour = self.simdi.hour
        self.ui.label_2.setText(str(self.simdi.time()))
        self.ui.label_3.setText(str(self.simdi.date()))
        

        self.value=os.path.isdir("C:/Users/Talha/Documents/Gunluk") #varmı? yokmu? klasör

        if self.value == True:
            pass
        else:
            os.mkdir("C:/Users/Talha/Documents/Gunluk")
        

    def yazma(self):
        gundelik=self.ui.textEdit.toPlainText()
        bugun=f"{gundelik} \n{str(self.simdi.date())}           {str(self.simdi.time())}"
        
        sayac=0
        result = os.listdir("C:/Users/Talha/Documents/Gunluk") 
        for dosya in result:      
            if dosya.endswith(".txt"):
                sayac+=1
        sayac+=1
        dosyadi=f"gunluk{sayac}.txt"

        if self.value == True:
            with open(f"C:/Users/Talha/Documents/Gunluk/{dosyadi}","w",encoding="utf-8") as file:
                file.write(bugun)
                self.ui.textEdit.clear()
        else:
            self.msgBox.setIcon(QMessageBox.Information)
            self.msgBox.setText("Dosya bulunamadı!!!")
            self.msgBox.setWindowTitle("HATA")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()
        
        self.ui.listWidget.clear()
        result = os.listdir("C:/Users/Talha/Documents/Gunluk") 
        for dosya in result:      
            if dosya.endswith(".txt"):
                self.ui.listWidget.addItem(str(dosya))
        self.ui.listWidget.setCurrentRow(0)

    def okuma(self):
        self.ui.textEdit_2.clear()
        index=self.ui.listWidget.currentRow()
        item=self.ui.listWidget.item(index)
        adres=f"C:/Users/Talha/Documents/Gunluk/{str(item.text())}"
        
        if self.value == True:
            with open(adres,"r",encoding="utf-8") as file:
                for metin in file:
                    self.ui.textEdit_2.append(metin)
        else:
            self.msgBox.setIcon(QMessageBox.Information)
            self.msgBox.setText("Dosya bulunamadı!!!")
            self.msgBox.setWindowTitle("HATA")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()

    def temizleme(self):
        self.ui.textEdit.clear()
    def sil(self):
        index=self.ui.listWidget.currentRow()
        self.item=self.ui.listWidget.item(index)
        q=QMessageBox.question(self,"gün silme","emin misin?: ",QMessageBox.Yes | QMessageBox.No)
        if q==QMessageBox.Yes:
            item=self.ui.listWidget.takeItem(index)
            del item
            os.remove(f"C:/Users/Talha/Documents/Gunluk/{str(self.item.text())}")
        self.ui.textEdit_2.clear()
        
app=QApplication(sys.argv)
win=pencere()
win.show()
app.exec_()