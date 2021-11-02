import sys
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QDialog, QFormLayout, QLineEdit, QInputDialog
from PySide6.QtCore import Slot
from db_worker import db_worker


class GUI:

    def __init__(self):
        self.worker = db_worker()
        self.app = QApplication()
        self.main_window = QMainWindow()
        self.main_window_init()
        self.main_window.show()
        self.app.exec()

    def main_window_init(self):
        v_box = QVBoxLayout()
        v_box.addWidget(my_button('Удаление', self.a_button1))
        v_box.addWidget(my_button('Редактирование', self.a_button2))
        v_box.addWidget(my_button('Добавление', self.a_button3))
        v_box.addWidget(my_button('Первый запрос', self.a_button4))
        v_box.addWidget(my_button('Второй запрос', self.a_button5))
        v_box.addWidget(my_button('Третий запрос', self.a_button6))
        q_widget = QWidget()
        q_widget.setLayout(v_box)
        self.main_window.setCentralWidget(q_widget)

    def a_button6(self):
        text, ok = QInputDialog.getText(self.main_window, "Input dialog", 'Введите значение')
        if ok:
            data = self.worker.third_request(text)
            my_table(["", "", ""], data, self.worker, None, None)
        pass

    def a_button5(self):
        text,ok = QInputDialog.getText(self.main_window,"Input dialog",'Введите значение')
        if ok:
            data = self.worker.second_requset(text)
            my_table(["", "", "", ""], data, self.worker, None, None)
        pass

    def a_button4(self):
        data = self.worker.first_request()
        my_table(["","","",""], data, self.worker, None, None)
        pass

    def a_button3(self):
        name = table_choice(self.worker.get_tables()).exec()
        temp = (self.worker.get_params_colums(name))
        add_row(temp[0], self.worker, name)

    def a_button2(self):
        name = table_choice(self.worker.get_tables()).exec()
        temp = (self.worker.get_params_colums(name))
        my_table(temp[0], temp[1], self.worker, name, mode='change')

    def a_button1(self):
        name = table_choice(self.worker.get_tables()).exec()
        temp = (self.worker.get_params_colums(name))
        my_table(temp[0], temp[1], self.worker, name, mode='delete')


class my_button(QPushButton):
    def __init__(self, text, action):
        super().__init__(text)
        self.clicked.connect(action)


class my_table(QTableWidget):
    def __init__(self, params, items, worker, name, mode):
        self.params = params
        self.name = name
        self.worker = worker
        super().__init__(len(items), len(params))
        self.q_dialog = QDialog()
        q_layout = QVBoxLayout()
        q_layout.addWidget(self)
        self.q_dialog.setLayout(q_layout)
        self.setHorizontalHeaderLabels(params)
        self.horizontalHeader().setStretchLastSection(True)
        for i in range(len(items)):
            for j in range(len(params)):
                to_add = QTableWidgetItem(str(items[i][j]))
                self.setItem(i, j, to_add)
        if mode == 'delete':
            self.itemClicked.connect(self.field_delete)
        if mode == 'change':
            self.itemChanged.connect(self.field_changed)
        q_layout.addWidget(my_button('Закрыть', lambda: (self.q_dialog.close())))
        self.q_dialog.exec()

    def field_changed(self, item):
        print(item.row())
        change = []
        for i in range(len(self.params)):
            if not i == item.column():
                change.append([self.params[i], self.item(item.row(), i).text()])
        self.worker.change_data(change, [self.params[item.column()], item.text()], self.name)

    def field_delete(self, item):
        data = []
        for i in range(len(self.params)):
            data.append([self.params[i], self.item(item.row(), i).text()])
        self.worker.delete_data(data, self.name)
        self.removeRow(item.row())


class table_choice:
    def __init__(self, params):
        self.q_dialog = QDialog()
        q_layout = QVBoxLayout()
        for i in params:
            q_layout.addWidget(costil(i[0], self.q_dialog, self))
        self.q_dialog.setLayout(q_layout)

    def exec(self):
        self.q_dialog.exec()
        return self.result

    def set_res(self, text):
        self.result = text


class costil(QPushButton):
    def __init__(self, text, dialog, i):
        super().__init__(text)
        self.clicked.connect(lambda: (i.set_res(text), dialog.close()))


class add_row():

    def __init__(self, names, worker, table_name):
        self.q_dialog = QDialog()
        q_layout = QFormLayout()
        self.worker = worker
        self.table_name = table_name
        self.q_dialog.setLayout(q_layout)
        self.lines = []
        for name in names:
            line = QLineEdit()
            q_layout.addRow(name, line)
            self.lines.append(line)
        q_layout.addWidget(my_button('Добавить', self.add_row))
        q_layout.addWidget(my_button('Отмена', lambda: (self.q_dialog.close())))
        self.q_dialog.exec()

    def add_row(self):
        list = []
        for line in self.lines:
            if line.text() == '':
                list.append("NULL")
            else:
                list.append(line.text())
        self.worker.add_data(self.table_name, list)
        self.q_dialog.close()
