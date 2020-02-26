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
        self.evention.clicked.connect(self.super_event)

    def add_event(self):
        super().__init__()
        self.z = Event()
        self.z.show()

    def super_event(self):
        self.listWidget.clear()
        z = Add_Event()
        self.dobav_list(z)

    def dobav_list(self, clas):  # добавляем виджеты на главный экран
        item = QListWidgetItem(self.listWidget)
        self.mywid = clas
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, self.mywid)
        item.setSizeHint(self.mywid.size())


class Add_Event(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_event.ui', self)
        self.pushButton.clicked.connect(self.prikol)

    def prikol(self):
        super().__init__()
        self.z = Event()
        self.z.show()


class Event(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('zametka.ui', self)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
