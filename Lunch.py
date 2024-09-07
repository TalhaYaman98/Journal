import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QMessageBox
from PyQt5.QtGui import QIcon, QColor
from Interface import Ui_MainWindow
from datetime import datetime
import os

class pencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("GÜNLÜK")  # Set the window title
        self.setToolTip("DevamEt!!")  # Set a tooltip for the window
        self.msgBox = QMessageBox()  # Create a message box for alerts
        
        # Connect button clicks to their respective methods
        self.ui.pushButton.clicked.connect(self.yazma)  # Connect the "Write" button
        self.ui.pushButton_2.clicked.connect(self.temizleme)  # Connect the "Clear" button
        self.ui.pushButton_3.clicked.connect(self.okuma)  # Connect the "Read" button
        self.ui.pushButton_4.clicked.connect(self.sil)  # Connect the "Delete" button

        # List all text files in the specified directory
        result = os.listdir("C:/Users/Talha/Documents/Gunluk")
        for dosya in result:
            if dosya.endswith(".txt"):  # Filter out only .txt files
                self.ui.listWidget.addItem(str(dosya))  # Add file names to the list widget
        self.ui.listWidget.setCurrentRow(0)  # Set the first item as selected

        # Get the current date and time
        self.simdi = datetime.now()
        year = self.simdi.year
        month = self.simdi.month
        day = self.simdi.day
        minute = self.simdi.minute
        second = self.simdi.second
        hour = self.simdi.hour
        # Display the current time and date on the UI
        self.ui.label_2.setText(str(self.simdi.time()))
        self.ui.label_3.setText(str(self.simdi.date()))

        # Check if the directory exists
        self.value = os.path.isdir("C:/Users/Talha/Documents/Gunluk")
        if not self.value:
            # Create the directory if it does not exist
            os.mkdir("C:/Users/Talha/Documents/Gunluk")

    def yazma(self):
        # Get text from the text editor
        gundelik = self.ui.textEdit.toPlainText()
        # Format the entry with the current date and time
        bugun = f"{gundelik} \n{str(self.simdi.date())}           {str(self.simdi.time())}"
        
        # Count the number of existing .txt files in the directory
        sayac = 0
        result = os.listdir("C:/Users/Talha/Documents/Gunluk")
        for dosya in result:
            if dosya.endswith(".txt"):
                sayac += 1
        sayac += 1
        # Generate a new file name
        dosyadi = f"gunluk{sayac}.txt"

        if self.value:
            # Write the formatted entry to the new file
            with open(f"C:/Users/Talha/Documents/Gunluk/{dosyadi}", "w", encoding="utf-8") as file:
                file.write(bugun)
                # Clear the text editor after writing
                self.ui.textEdit.clear()
        else:
            # Show an error message if the directory is missing
            self.msgBox.setIcon(QMessageBox.Information)
            self.msgBox.setText("Dosya bulunamadı!!!")
            self.msgBox.setWindowTitle("HATA")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()

        # Update the list of files in the list widget
        self.ui.listWidget.clear()
        result = os.listdir("C:/Users/Talha/Documents/Gunluk")
        for dosya in result:
            if dosya.endswith(".txt"):
                self.ui.listWidget.addItem(str(dosya))
        self.ui.listWidget.setCurrentRow(0)  # Set the first item as selected

    def okuma(self):
        # Clear the second text editor
        self.ui.textEdit_2.clear()
        # Get the index of the currently selected item in the list widget
        index = self.ui.listWidget.currentRow()
        item = self.ui.listWidget.item(index)
        # Construct the file path for the selected entry
        adres = f"C:/Users/Talha/Documents/Gunluk/{str(item.text())}"

        if self.value:
            # Read the content of the selected file and display it in the second text editor
            with open(adres, "r", encoding="utf-8") as file:
                for metin in file:
                    self.ui.textEdit_2.append(metin)
        else:
            # Show an error message if the directory is missing
            self.msgBox.setIcon(QMessageBox.Information)
            self.msgBox.setText("Dosya bulunamadı!!!")
            self.msgBox.setWindowTitle("HATA")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.show()

    def temizleme(self):
        # Clear the content of the first text editor
        self.ui.textEdit.clear()

    def sil(self):
        # Get the index of the currently selected item in the list widget
        index = self.ui.listWidget.currentRow()
        self.item = self.ui.listWidget.item(index)
        # Ask for confirmation before deleting the entry
        q = QMessageBox.question(self, "gün silme", "emin misin?: ", QMessageBox.Yes | QMessageBox.No)
        if q == QMessageBox.Yes:
            # Remove the item from the list widget
            item = self.ui.listWidget.takeItem(index)
            del item
            # Delete the file from the directory
            os.remove(f"C:/Users/Talha/Documents/Gunluk/{str(self.item.text())}")
        # Clear the second text editor after deletion
        self.ui.textEdit_2.clear()

# Create a QApplication instance and run the application
app = QApplication(sys.argv)
win = pencere()
win.show()
app.exec_()
