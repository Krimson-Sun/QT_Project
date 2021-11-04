from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QMessageBox
from PyQt5.QtWidgets import QLineEdit
import sqlite3
import sys
from os.path import join as path_to

ADDRESS = path_to('data', 'qt_project_database.db')
AUTHED_USER_ID = 0
AUTHED_USER_STATUS = 'student'
AUTHED_USER_NAME = ''


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

    def get_info(self, table, rows, column=None, condition=None):
        if rows != '*':
            rows = f'"{rows}"'
        if condition and column:
            request = f'SELECT {rows} FROM {table} WHERE {column} = "{condition}"'
        else:
            request = f'SELECT {rows} FROM {table}'
        print(request)
        result = self.cur.execute(request).fetchall()
        print(result)
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
        self.login_label.setText(f'Логин (ID для учеников)')
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
        global AUTHED_USER_ID, AUTHED_USER_STATUS, AUTHED_USER_NAME
        login, password = self.login_input.text(), self.password_input.text()
        print(login, password)
        if login.isdigit():
            res = db.get_info('Students', 'student_password', column='studentID', condition=login)[0][0]
            if res:
                if res == password:
                    print(f'successfully logged in as {login}')
                    AUTHED_USER_STATUS = 'student'
                    AUTHED_USER_NAME = db.get_info('Students', 'student_names', column='studentID', condition=login)[0][
                        0]
                    AUTHED_USER_ID = login
                    self.main = MainWindow()
                    self.main.show()
                    self.close()
                else:
                    print('log in failed')
                    QMessageBox.critical(None, 'Ошибка',
                                         'Авторизация не удалась. Проверьте правильность введенных данных и повторите '
                                         'попытку')
        else:
            res = db.get_info('teachers', 'teacher_password', column='teacher_login', condition=login)[0][0]
            print('res: ', res)
            if res == password:
                print(f'successfully logged in as {login}')
                AUTHED_USER_ID = db.get_info('teachers', 'teacherID', column='teacher_login', condition=login)[0][0]
                AUTHED_USER_STATUS = 'teacher'
                AUTHED_USER_NAME = login
                self.main = MainWindow()
                self.main.show()
                self.close()
            else:
                print('log in failed')
                QMessageBox.critical(None, 'Ошибка',
                                     'Авторизация не удалась. Проверьте правильность введенных данных и повторите '
                                     'попытку')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global AUTHED_USER_NAME, AUTHED_USER_STATUS
        self.setGeometry(100, 100, 650, 400)
        self.setWindowTitle('')
        self.setStyleSheet('background-color: #eeeeee')

        self.name_label = QLabel(self)
        self.name_label.setText(f'Авторизованный пользователь: {AUTHED_USER_NAME}')
        self.name_label.move(20, 30)

        self.logout = QPushButton(self)
        self.logout.setStyleSheet('background-color: #f0f0f0')
        self.logout.resize(100, 20)
        self.logout.move(25, 50)
        self.logout.setStyleSheet('font-style:italic')
        self.logout.setText('Выход')
        self.logout.clicked.connect(self.quit)

        if AUTHED_USER_STATUS == 'teacher':
            self.new_student = QPushButton(self)
            self.new_student.resize(200, 50)
            self.new_student.move(100, 100)
            self.new_student.setText('Добавить ученика')
            self.new_student.clicked.connect(self.create_student)

            self.show_students_b = QPushButton(self)
            self.show_students_b.resize(200, 50)
            self.show_students_b.move(350, 100)
            self.show_students_b.setText('Просмотреть список учеников')
            self.show_students_b.clicked.connect(self.show_students)

        else:
            self.start_work_ = QPushButton(self)
            self.start_work_.resize(200, 50)
            self.start_work_.move(100, 100)
            self.start_work_.setText('Решать')
            self.start_work_.clicked.connect(self.start_work)

            self.show_tasks_ = QPushButton(self)
            self.show_tasks_.resize(200, 50)
            self.show_tasks_.move(350, 100)
            self.show_tasks_.setText('Задания от преподавателя')
            self.show_tasks_.clicked.connect(self.show_tasks)

    def quit(self):
        global AUTHED_USER_NAME, AUTHED_USER_ID, AUTHED_USER_STATUS
        AUTHED_USER_ID, AUTHED_USER_STATUS, AUTHED_USER_NAME = 0, 'student', ''
        self.auth = AuthWindow()
        self.auth.show()
        self.close()

    def create_student(self):
        self.new = NewStudent()
        self.new.show()

    def show_students(self):
        pass

    def start_work(self):
        pass

    def show_tasks(self):
        pass

class NewStudent(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 650, 400)
        self.setWindowTitle('Создание аккаунта')
        self.setStyleSheet('background-color: #eeeeee')

        self.id_label = QLabel(self)
        self.id_label.setText(f'ID создаваемового аккаунта: {db.get_info("Students", "id")}')
        self.id_label.move(20, 30)

        self.password_label = QLabel(self)
        self.password_label.setText(f'Пароль')
        self.password_label.move(150, 130)

        self.password_input = QLineEdit(self)
        self.password_input.move(150, 150)

        self.log_up = QPushButton(self)
        self.log_up.resize(200, 50)
        self.log_up.move(220, 220)
        self.log_up.setText('Зарегистрировать')
        self.log_up.clicked.connect(self.save_new_student)

    def save_new_student(self):
        global AUTHED_USER_ID
        try:
            db.add_info()
            print('a new student created successfully')

        except Exception as e:
            print('creation of a new student failed cause of', e)
            QMessageBox.critical(None, 'Ошибка', e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = Database()
    win = AuthWindow()
    win.show()
    sys.exit(app.exec())
