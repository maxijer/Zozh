import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QInputDialog, QListWidget, \
    QListWidgetItem, \
    QTableWidget, QTableWidgetItem, QFileDialog, QComboBox
from PyQt5.QtGui import QPalette, QImage, QBrush, QIcon
from PyQt5.QtCore import QSize
import sqlite3
import hashlib
import random
import csv


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('new_company.ui', self)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
