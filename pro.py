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

znach = ''
count_for_play = 0
true_otw = 0
flag = False
korzina = list()
titeks = list()
sravnenie = list()


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('avtorization.ui', self)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
