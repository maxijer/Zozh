import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QInputDialog, QListWidget, \
    QListWidgetItem, \
    QTableWidget, QTableWidgetItem, QFileDialog, QComboBox
from PyQt5.QtGui import QPalette, QImage, QBrush, QIcon, QPixmap
import sqlite3
import hashlib


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/avtorization1.ui', self)
        self.registrate.clicked.connect(self.registrated)
        self.login.clicked.connect(self.whod)
        self.setWindowTitle('Авторизация')

    def registrated(self):  ## функция регистрации пользователей
        z = self.login1.text()
        w = self.password.text()
        has = hashlib.md5(w.encode('utf-8')).hexdigest()
        if len(z) == 0 or len(w) == 0:
            self.h = Nelza()
            self.h.show()
        else:
            con = sqlite3.connect('rabota.db')

            cur1 = con.cursor()
            pepole = cur1.execute("""SELECT number1 FROM users
            WHERE ID = ?""", (z,)).fetchall()
            if len(pepole) == 0:
                try:
                    # Создание курсора
                    cur = con.cursor()

                    # Выполнение запроса и добавляем логин и пароль
                    cur.execute("""INSERT INTO users("ID", "password") VALUES(?, ?)
                                    """, (z, has))
                    con.commit()
                    con.close()
                    self.h = OK()
                    self.h.show()
                except sqlite3.IntegrityError:
                    self.w = Nelza()
                    self.w.show()
            else:
                self.w = Nelza()
                self.w.show()

    def whod(self):  ## функция для проверки и входа в систему
        z = self.login1.text()
        w = self.password.text()
        has = hashlib.md5(w.encode('utf-8')).hexdigest()
        con = sqlite3.connect('rabota.db')

        # Создание курсора
        cur = con.cursor()

        # Выполнение запроса и добавляем логин и пароль
        z = cur.execute("""SELECT ID, password FROM users
        WHERE ID = ? AND password = ?
                               """, (z, has)).fetchall()
        con.close()
        if len(z) == 0:
            self.w = No_registr()
            self.w.show()
        else:
            self.new = SecondWidget()
            self.new.show()
            self.hide()


class OK(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/OK.ui', self)


class Nelza(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/nelza.ui', self)


class SecondWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/all.ui', self)
        self.pushButton_8.clicked.connect(self.add_challenge1)
        self.pushButton_5.clicked.connect(self.chalenge)
        self.pushButton_7.clicked.connect(self.add_event)
        self.pushButton_4.clicked.connect(self.super_event)
        self.pushButton_3.clicked.connect(self.dobavim_raiting)

    def dobavim_raiting(self):
        self.mast = I_am_reiting()
        self.dobav_list(self.mast)

    def super_event(self):
        self.listWidget.clear()
        con = sqlite3.connect('rabota.db')
        cur1 = con.cursor()
        pepole = cur1.execute("""SELECT * FROM event""").fetchall()
        for i in pepole:
            self.f = Govoryu_obyav(i[1], i[2], i[3], i[4])
            self.dobav_list(self.f)
        self.listWidget.update()

    def add_event(self):
        self.h = Event()
        self.h.show()

    def add_challenge1(self):
        self.z = Challenge()
        self.z.show()

    def chalenge(self):
        con = sqlite3.connect('rabota.db')
        cur1 = con.cursor()
        pepole = cur1.execute("""SELECT * FROM challenge""").fetchall()
        self.listWidget.clear()
        for i in pepole:
            z = Dostal_challenge(i[1])
            self.dobav_list(z)
        print(pepole)

    def dobav_list(self, clas):  # добавляем виджеты на главный экран
        item = QListWidgetItem(self.listWidget)
        self.mywid = clas
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, self.mywid)
        item.setSizeHint(self.mywid.size())


class I_am_reiting(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/tabel.ui', self)
        con = sqlite3.connect('rabota.db')
        cur1 = con.cursor()
        pepole = cur1.execute("""SELECT * FROM users""").fetchall()
        reader = list()
        for i in pepole:
            z = (i[1], i[3], i[4], i[5], i[6])
            reader.append(z)
        reader = sorted(reader, key=lambda x: x[1])
        self.tableWidget.setRowCount(len(reader))
        self.tableWidget.setColumnCount(len(reader[0]))
        # Заполнили размеры таблицы
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Балы', 'роль', 'И.Ф.О', 'Должность'])
        w = 0
        # Заполнили таблицу полученными элементами
        for k in range(len(reader)):
            for i, elem in enumerate(list(reader[k])):
                self.tableWidget.setItem(w, i, QTableWidgetItem(str(elem)))
            w += 1


class No_registr(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('No_registration.ui', self)


class Add_Event(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/add_event.ui', self)
        self.pushButton.clicked.connect(self.prikol)

    def prikol(self):
        super().__init__()
        self.z = Event()
        self.z.show()


class Event(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/zametka.ui', self)
        self.fname = 0
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.load_image)

    def add(self):
        al = str(self.dateTimeEdit.dateTime())[23:-1].split(', ')
        data = '.'.join(list(reversed(al[:3])))
        time = ':'.join(al[3:])
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
        uic.loadUi('data/event.ui', self)
        self.data.setText(data)
        self.label_7.setText(time)
        self.label_6.setText(event)
        if foto is not None:
            pixmap = QPixmap(foto)
            self.label_3.setPixmap(pixmap)


class Challenge(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/add_challenge.ui', self)
        self.pushButton.clicked.connect(self.dobavim_challenge)
        self.pushButton_2.clicked.connect(self.delitnem)

    def dobavim_challenge(self):
        con = sqlite3.connect('rabota.db')
        cur = con.cursor()
        z = cur.execute("""INSERT INTO challenge("opis")
                             VALUES(?)""",
                        (self.textEdit.toPlainText(),))
        con.commit()
        con.close()
        self.hide()

    def delitnem(self):
        self.textEdit.clear()


class Dostal_challenge(QWidget):
    def __init__(self, shto):
        super().__init__()
        uic.loadUi('data/challenge.ui', self)
        self.label.setText(str(shto))


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
