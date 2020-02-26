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
        uic.loadUi('avtorization.ui', self)
        palette = QPalette()
        oImage = QImage("й.jpg")
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)
        self.registrate.clicked.connect(self.registrated)
        self.login.clicked.connect(self.whod)
        self.setWindowTitle('Авторизация')

    def registrated(self):  ## функция регистрации пользователей
        z = self.login1.text()
        w = self.password.text()
        has = hashlib.md5(w.encode('utf-8')).hexdigest()
        if len(z) == 0 or len(w) == 0:
            i, okBtnPressed = QInputDialog.getText(self, "Поле", "Придумайте новый пароль")
        else:
            con = sqlite3.connect('rabota.db')

            cur1 = con.cursor()
            pepole = cur1.execute("""SELECT  id FROM users
            WHERE login = ?""", (z,)).fetchall()
            if len(pepole) == 0:
                try:
                    # Создание курсора
                    cur = con.cursor()

                    # Выполнение запроса и добавляем логин и пароль
                    cur.execute("""INSERT INTO users("login", "password") VALUES(?, ?)
                                    """, (z, has))
                    con.commit()
                    con.close()
                    i, okBtnPressed = QInputDialog.getText(self, "Регистрация",
                                                           "Пользователь успешно зарегистрирован")
                except sqlite3.IntegrityError:
                    i, okBtnPressed = QInputDialog.getText(self, "Пароль", "Придумайте новый пароль")
            else:
                i, okBtnPressed = QInputDialog.getText(self, "Такой пользователь уже существует",
                                                       "придумайте другой логин")

    def whod(self):  ## функция для проверки и входа в систему
        z = self.login1.text()
        w = self.password.text()
        has = hashlib.md5(w.encode('utf-8')).hexdigest()
        con = sqlite3.connect('rabota.db')

        # Создание курсора
        cur = con.cursor()

        # Выполнение запроса и добавляем логин и пароль
        z = cur.execute("""SELECT login, password FROM users
        WHERE login = ? AND password = ?
                               """, (z, has)).fetchall()
        con.close()
        if len(z) == 0:
            i, okBtnPressed = QInputDialog.getText(self, "Ошибка",
                                                   "Пользователь не зарегистрирован")
        else:
            self.new = SecondWidget()
            self.new.show()
            self.hide()


class SecondWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('new_company.ui', self)
        self.evention.clicked.connect(self.super_event)
        self.add_ev.clicked.connect(self.add_event)
        self.add_challenge.clicked.connect(self.add_challenge1)
        self.pushButton_7.clicked.connect(self.my_challenge)

    def add_challenge1(self):
        self.z = Challenge()
        self.z.show()

    def add_event(self):
        self.z = Event()
        self.z.show()

    def my_challenge(self):
        con = sqlite3.connect('rabota.db')
        cur1 = con.cursor()
        pepole = cur1.execute("""SELECT * FROM challenge""").fetchall()
        self.listWidget.clear()
        for i in pepole:
            z = Dostal_challenge(i[1])
            self.dobav_list(z)
        print(pepole)

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


class Challenge(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_challenge.ui', self)
        self.pushButton.clicked.connect(self.dobavim_challenge)

    def dobavim_challenge(self):
        con = sqlite3.connect('rabota.db')
        cur = con.cursor()
        z = cur.execute("""INSERT INTO challenge("opis")
                             VALUES(?)""",
                        (self.textEdit.toPlainText(),))
        con.commit()
        con.close()
        self.hide()


class Dostal_challenge(QWidget):
    def __init__(self, shto):
        super().__init__()
        uic.loadUi('challenge.ui', self)
        self.label.setText(str(shto))


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
