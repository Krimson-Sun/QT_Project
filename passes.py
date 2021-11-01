from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QApplication, QTextBrowser, QPushButton, QLabel, QMessageBox
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QColorDialog, QLineEdit
import os
import sqlite3
import sys
from os.path import join as path_to

ADDRESS = path_to('data', 'qt_project_database.db')
AUTHED_USER_ID = 12345


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))
    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()


sys.excepthook = log_uncaught_exceptions


def auth(idd):
    pass


def read_tasks(idd):
    pass


def check_answers(answers):
    pass


class Database:
    def __init__(self):
        self.con = sqlite3.connect(ADDRESS)
        self.cur = self.con.cursor()

    def get_info(self, table, rows, column, condition):
        request = f'''SELECT {rows} FROM {table}
                                                      WHERE {column} = "{condition}"'''
        print(request)
        result = self.cur.execute(request).fetchall()
        return result if result else None

    def del_info(self):
        pass

    def add_info(self):
        pass


class Teacher:
    def __init__(self):
        pass

    def add_student(self):
        pass

    def del_student(self):
        pass

    def add_task(self):
        pass


class Student:
    def __init__(self):
        pass

    def give_stats(self):
        pass


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # noinspection PyAttributeOutsideInit
    def initUI(self):
        self.setGeometry(100, 100, 650, 400)
        self.setWindowTitle('Авторизуйтесь')
        self.setStyleSheet('background-color: #eeeeee')

        self.login_label = QLabel(self)
        self.login_label.setText(f'Логин')
        self.login_label.move(150, 130)

        self.login_input = QLineEdit(self)
        self.login_input.move(150, 150)

        self.password_label = QLabel(self)
        self.password_label.setText(f'Пароль')
        self.password_label.move(350, 130)

        self.password_input = QLineEdit(self)
        self.password_input.move(350, 150)

        self.log_in = QPushButton(self)
        self.log_in.resize(200, 50)
        self.log_in.move(220, 220)
        self.log_in.setText('Войти')
        self.log_in.clicked.connect(self.auth)

    def auth(self):
        login, password = self.login_input.text(), self.password_input.text()
        print(login, password)
        res = db.get_info('teachers', 'teacher_password', 'teacher_login', login)[0][0]
        if res:
            if res == password:
                print(f'successfully logged in as {login}')
            else:
                print('log in failed')
        else:
            return None



if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = Database()
    win = AuthWindow()
    win.show()
    sys.exit(app.exec())
