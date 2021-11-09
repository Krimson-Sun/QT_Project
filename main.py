from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QMessageBox, QStackedWidget
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QRadioButton
from PyQt5.QtGui import QPixmap
import sqlite3
import sys
from os.path import join as path_to
import matplotlib.pyplot as plt
from time import sleep

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


def read_tasks(student_id):
    pass
    # тут должна быть функция для чтения монолога препода
    # s = db.get_info('exercises', 'exercise_options', column='id', condition=student_id)[0][0]
    # tasks = s.split(' | ')
    # return tasks


def save_task(student_id, task):
    pass
    # а тут для записи


def check_answers(answers):
    pass


def show_stats(student_id):
    stats = db.get_info('Students', ('student_experience', 'student_efficiency'), column='studentID',
                        condition=student_id)[0]

    labels = ('Верно', 'Неверно')
    sizes = [stats[1], 100 - stats[1]]

    fig1, ax1 = plt.subplots()
    explode = (0, 0.1)
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)

    plt.title('Статистика')
    plt.show()


class Database:
    def __init__(self):
        self.con = sqlite3.connect(ADDRESS)
        self.cur = self.con.cursor()

    def get_info(self, table, rows, column=None, condition=None):
        if rows != '*':
            if type(rows) == str:
                rows = f'"{rows}"'
            elif type(rows) == tuple:
                rows = ','.join(rows)
        if condition and column:
            if type(condition) == str:
                request = f'SELECT {rows} FROM {table} WHERE {column} = "{condition}"'
            elif type(condition) == int:
                request = f'SELECT {rows} FROM {table} WHERE {column} = {condition}'
            else:
                return None
        else:
            request = f'SELECT {rows} FROM {table}'
        print(request)
        result = self.cur.execute(request).fetchall()
        print(result)
        return result if result else None

    def del_info(self):
        pass

    def add_info(self, table, values, columns=None):
        if columns:
            request = f'''INSERT INTO {table}({",".join(columns)}) VALUES{tuple(values)}'''
        else:
            request = f'''INSERT INTO {table} VALUES{tuple(values)}'''
        print('adding request:', request)
        result = self.cur.execute(request)
        print('adding result:', result)
        self.con.commit()
        return result if result else None


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
            try:
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
            except TypeError:
                QMessageBox.warning(None, 'Ошибка',
                                    'Авторизация не удалась. Ученики для входа должны использовать id')


# noinspection PyAttributeOutsideInit
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
            self.start_work_.setText('Решать задания')
            self.start_work_.clicked.connect(self.start_work)

            self.show_tasks_ = QPushButton(self)
            self.show_tasks_.resize(200, 50)
            self.show_tasks_.move(350, 100)
            self.show_tasks_.setText('Смотреть статистику')
            self.show_tasks_.clicked.connect(lambda x: show_stats(AUTHED_USER_ID))

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
        self.new = ShowStudents()
        self.new.show()

    def start_work(self):
        self.new = StartWork()
        self.new.show()

    # def show_stats(self):
    #     show_stats()


# noinspection PyAttributeOutsideInit
class StartWork(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.answers = []
        self.committed = False
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 650, 600)
        self.setWindowTitle('Задания')
        self.setStyleSheet('background-color: #eeeeee')

        exercises = db.get_info('exercises', '*')

        self.exercises_wins = QStackedWidget(self)

        for exercise in exercises:
            self.exercises_wins.addWidget(Exercise(exercise, self))

        for i in range(1, len(exercises) + 1):
            self.exercises_wins.setCurrentIndex(i)
            while not self.committed:
                pass

        self.new = Results()
        self.new.show()
        self.close()


# noinspection PyAttributeOutsideInit
class Exercise(QWidget):
    def __init__(self, exercise, parent):
        super().__init__()
        self.parent = parent
        self.initUI(exercise)

    def initUI(self, exercise):
        self.setGeometry(100, 100, 650, 600)
        self.setWindowTitle('Задания')
        self.setStyleSheet('background-color: #eeeeee')

        self.id, self.img, self.text, self.options, self.right_answer, self.link = exercise
        print(self.id)
        self.img = QPixmap(path_to('data/images', self.img))
        self.options = self.options.split(' | ')

        self.img_label = QLabel(self)
        self.img_label.setPixmap(self.img)
        self.img_label.resize(604, 225)
        self.img_label.move(0, 0)

        print(self.options)

        self.radio_button_1 = QRadioButton(self)
        self.radio_button_1.setChecked(True)
        self.radio_button_1.resize(500, 50)
        self.radio_button_1.move(50, 300)
        self.radio_button_1.setText(self.options[0])

        self.radio_button_2 = QRadioButton(self)
        self.radio_button_2.setChecked(True)
        self.radio_button_2.resize(500, 50)
        self.radio_button_2.setText(self.options[1])
        self.radio_button_2.move(50, 350)

        self.radio_button_3 = QRadioButton(self)
        self.radio_button_3.setChecked(True)
        self.radio_button_3.resize(500, 50)
        self.radio_button_3.setText(self.options[2])
        self.radio_button_3.move(50, 400)

        self.commit_answer = QPushButton(self)
        self.commit_answer.resize(200, 50)
        self.commit_answer.move(50, 500)
        self.commit_answer.setText('Ответить')
        self.commit_answer.clicked.connect(self.committing_answer)

    def committing_answer(self):
        self.ans = 1
        if self.radio_button_2.clicked:
            self.ans = 2
        elif self.radio_button_3.clicked:
            self.ans = 3
        if self.ans == self.right_answer:
            self.parent.answers.append((True, self.ans, self.ans))
        else:
            self.parent.answers.append((False, self.ans, self.right_answer))
        self.parent.committed = True


# noinspection PyAttributeOutsideInit
class Results(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 650, 400)
        self.setWindowTitle('Статистика')
        self.setStyleSheet('background-color: #eeeeee')


# noinspection PyAttributeOutsideInit
class ShowStats(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 650, 400)
        self.setWindowTitle('Статистика')
        self.setStyleSheet('background-color: #eeeeee')


# noinspection PyAttributeOutsideInit
class NewStudent(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 650, 400)
        self.setWindowTitle('Создание аккаунта')
        self.setStyleSheet('background-color: #eeeeee')

        self.id_label = QLabel(self)
        self.id_label.setText(f'ID создаваемового аккаунта: {db.get_info("Students", "studentID")[-1][0] + 1}')
        self.id_label.move(20, 30)

        self.password_label = QLabel(self)
        self.password_label.setText(f'Пароль')
        self.password_label.move(150, 130)

        self.password_input = QLineEdit(self)
        self.password_input.move(150, 150)

        self.names_label = QLabel(self)
        self.names_label.setText(f'ФИО')
        self.names_label.move(250, 130)

        self.names_input = QLineEdit(self)
        self.names_input.move(250, 150)

        self.log_up = QPushButton(self)
        self.log_up.resize(200, 50)
        self.log_up.move(220, 220)
        self.log_up.setText('Зарегистрировать')
        self.log_up.clicked.connect(self.save_new_student)

    def save_new_student(self):
        global AUTHED_USER_ID
        try:
            db.add_info('Students', (AUTHED_USER_ID, self.password_input.text(), self.names_input.text()),
                        ('teacherID', 'student_password', 'student_names'))
            print('a new student created successfully')
            self.close()
        except Exception as e:
            print('creation of a new student failed cause of', e)
            QMessageBox.critical(None, 'Ошибка', e)


# noinspection PyAttributeOutsideInit
class ShowStudents(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 650, 400)
        self.setWindowTitle('Просмотр учеников')
        self.setStyleSheet('background-color: #eeeeee')

        self.table = QTableWidget(self)
        self.table.setGeometry(0, 50, 650, 350)
        # self.table.setColumnWidth(100, 100)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Пароль', 'ФИО', ''])

        students = db.get_info('Students', ("studentID", "student_password", "student_names"), 'teacherID',
                               AUTHED_USER_ID)

        self.table.setRowCount(len(students))

        for (i, elem) in zip(range(len(students)), students):
            self.table.setItem(i, 0, QTableWidgetItem(str(elem[0])))
            self.table.setItem(i, 1, QTableWidgetItem(elem[1]))
            self.table.setItem(i, 2, QTableWidgetItem(elem[2]))

            self.btn = QPushButton(self)
            self.btn.setText(f'Задать задание')
            self.btn.clicked.connect(lambda f, idd=elem[0]: self.create_task(idd))

            self.table.setCellWidget(i, 3, self.btn)

        self.table.resizeColumnsToContents()

    def create_task(self, student_id):
        self.new = CreateTask(student_id)
        self.new.show()


class CreateTask(QWidget):
    def __init__(self, student_id):
        self.student_id = student_id
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 650, 400)
        self.setWindowTitle('Задать задание')
        self.setStyleSheet('background-color: #eeeeee')

        self.task_input = QLineEdit(self)
        self.task_input.setGeometry(50, 50, 500, 300)

        self.input_done = QPushButton(self)
        self.input_done.resize(200, 50)
        self.input_done.move(220, 220)
        self.input_done.setText('Отправить')
        self.input_done.clicked.connect(lambda x: save_task(self.student_id, self.task_input.text()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = Database()
    win = AuthWindow()
    win.show()
    sys.exit(app.exec())
