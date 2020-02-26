import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QInputDialog, QListWidget, \
    QListWidgetItem, \
    QTableWidget, QTableWidgetItem, QFileDialog, QComboBox
from PyQt5.QtGui import QPalette, QImage, QBrush, QIcon, QPixmap
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
        self.add_ev.clicked.connect(self.add_event)

    def add_event(self):
        super().__init__()
        self.z = Event()
        self.z.show()

    def super_event(self):
        self.listWidget.clear()
        z = Add_Event()
        self.dobav_list(z)
        con = sqlite3.connect('rabota.db')
        cur1 = con.cursor()
        pepole = cur1.execute("""SELECT * FROM event""").fetchall()
        for i in pepole:
            self.f = Govoryu_obyav(i[1], i[2], i[3], i[4])
            self.dobav_list(self.f)
        self.listWidget.update()

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
        self.fname = 0
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.load_image)

    def add(self):
        al = str(self.dateTimeEdit.dateTime())[23:-1].split(', ')
        print(al)
        year = al[0]
        mounth = al[1]
        day = al[2]
        house = al[3]
        minutes = al[-1]
        data = '.'.join(list(reversed(al[:3])))
        time = ':'.join(al[3:])
        print(time)
        print(data)
        print(self.textEdit.toPlainText())
        if self.fname == 0:
            con = sqlite3.connect('rabota.db')
            cur = con.cursor()
            z = cur.execute("""INSERT INTO event("data1", "time1", "event")
            VALUES(?, ?, ?)""", (data, time, self.textEdit.toPlainText()))
            con.commit()
            con.close()
            self.hide()
        else:
            con = sqlite3.connect('rabota.db')
            cur = con.cursor()
            z = cur.execute("""INSERT INTO event("data1", "time1", "event" , "foto")
                      VALUES(?, ?, ?, ?)""", (data, time, self.textEdit.toPlainText(), self.fname))
            con.commit()
            con.close()
            self.hide()

    def load_image(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку',
                                                 '', "Картинка(*.jpg)")[0]
        pixmap = QPixmap(self.fname)
        self.label_2.setPixmap(pixmap)


class Govoryu_obyav(QWidget):
    def __init__(self, data, time, event, foto):
        super().__init__()
        uic.loadUi('ev.ui', self)
        self.data.setText(data)
        self.label_6.setText(time)
        self.label_4.setText(event)
        if foto is not None:
            pixmap = QPixmap(foto)
            self.label_3.setPixmap(pixmap)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
