import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QWidget, QStackedWidget, QHBoxLayout, QApplication, QAction, qApp


class Widget2():
    def stack2UI(self):
        self.stack2 = QWidget()
        self.button = QPushButton('add in conf')
        self.line = QLineEdit()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.push_me)
        self.button.setToolTip("don't push")
        self.stack2.setLayout(self.layout)

    def push_me(self):

        temp = self.line.text()
        p = self.leftlist.currentItem()
        temp1 = p.text()
        self.all_map[temp1] = temp
        self.line.clear()
        for i,j in self.all_map.items():
            print(i,j)

class Widget1():
    def stack1UI(self):
        self.stack1 = QWidget()
        self.boxes = QComboBox()
        self.add_but = QPushButton('add in conf')

        self.boxes.addItems(['hourly', 'daily', 'weekly', 'monthly', 'yearly'])
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.boxes)
        self.layout1.addWidget(self.add_but)
        self.add_but.clicked.connect(self.push_me1)
        self.stack1.setLayout(self.layout1)

    def push_me1(self):
        temp = self.boxes.currentText()
        p = self.leftlist.currentItem()
        temp1 = p.text()
        self.all_map[temp1] = temp
        self.line.clear()
        for i, j in self.all_map.items():
            print(i, j)

class Manager(QWidget, Widget2, Widget1):
    def __init__(self):
        super().__init__()
        self.all_map = dict()
        hbox1 = QHBoxLayout()
        self.ladel_name = QLabel('путь до файла с логами')
        self.main_name = QLineEdit()
        self.ladel_name1 = QLabel('имя файла')
        self.names1 = QLineEdit()

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.ladel_name1)
        hbox2.addWidget(self.names1)
        self.end_button = QPushButton('проверка сгенерированного файла')
        self.Left_Bar()
        self.names1.hide()
        self.ladel_name1.hide()
        self.stack2UI()
        self.stack1UI()
        self.Stack = QStackedWidget()
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        hbox1.addWidget(self.ladel_name)
        hbox1.addWidget(self.main_name)
        self.vbox.addLayout(hbox1)
        self.vbox.addLayout(hbox2)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)
        self.vbox.addLayout(hbox)
        self.vbox.addWidget(self.end_button)
        self.setLayout(self.vbox)
        self.Stack.setCurrentIndex(0)
        self.leftlist.currentRowChanged.connect(self.display)  # отображение одного из виджетов из стеквиджет
        self.end_button.clicked.connect(self.check_all)
        self.setGeometry(10, 10, 700, 500)
        self.setWindowTitle('devops manager')
        self.show()


    def check_all(self):
        self.leftlist.hide()
        self.Stack.hide()
        self.write_button = QPushButton('write')
        self.main_name.hide()
        self.ladel_name.hide()
        self.end_button.hide()
        self.names1.show()
        self.ladel_name1.show()
        self.tttt = QTextEdit()

        temp_main_name = self.main_name.text()
        self.all_text = temp_main_name + ' {\n'
        for i,j in self.all_map.items():
            if i == 'check time':
                self.all_text += j
                self.all_text += '\n'
            else:
                self.all_text += i;
                self.all_text += ' '
                self.all_text += j;
                self.all_text += '\n'
        self.all_text += '}'
        self.tttt.setText(self.all_text)

        self.vbox.addWidget(self.tttt)
        self.vbox.addWidget(self.write_button)
        self.write_button.clicked.connect(self.write_in_file)

    def write_in_file(self):
        ptr = os.getcwd()
        names = self.names1.text()
        path = os.path.join(ptr, names)
        print(path)
        f = open(path, 'w')
        f.write(self.all_text)
        f.close()
        sys.exit()
    def description(self, str_list):
        if str_list == 'rotate':
            self.leftlist.setToolTip('указывает сколько старых логов нужно хранить, в параметрах передается количество')
        elif str_list == 'create':
            self.leftlist.setToolTip('указывает, что необходимо создать пустой лог файл после перемещения старого')
        elif str_list == 'dateext':
            self.leftlist.setToolTip('добавляет дату ротации перед заголовком старого лога')
        elif str_list == 'compress':
            self.leftlist.setToolTip('указывает, что лог необходимо сжимать')
        elif str_list == 'delaycompress':
            self.leftlist.setToolTip('не сжимать последний и предпоследний журнал')
        elif str_list == 'extension':
            self.leftlist.setToolTip(' сохранять оригинальный лог файл после ротации, если у него указанное расширение')
        elif str_list == 'mail':
            self.leftlist.setToolTip('отправлять Email после завершения ротации')
        elif str_list == 'maxage':
            self.leftlist.setToolTip('выполнять ротацию журналов, если они старше, чем указано')
        elif str_list == 'missingok':
            self.leftlist.setToolTip('не выдавать ошибки, если лог файла не существует')
        elif str_list == 'olddir':
            self.leftlist.setToolTip('перемещать старые логи в отдельную папку')
        elif str_list == 'start':
            self.leftlist.setToolTip('номер, с которого будет начата нумерация старых логов')
        elif str_list == 'size':
            self.leftlist.setToolTip('размер лога, когда он будет перемещен')
        else:
            self.leftlist.setToolTip('')


    def display(self, i):
        self.Stack.setCurrentIndex(i)  # возврат текущего индекса из списка левого меню
        if i == 0:
            self.Stack.setCurrentIndex(0)
        else:
            self.Stack.setCurrentIndex(1)
        p = self.leftlist.currentItem()
        self.description(p.text())

    def Left_Bar(self):
        self.leftlist = QListWidget()
        self.leftlist.insertItem(0, 'check time')
        self.leftlist.insertItem(1, 'rotate')
        self.leftlist.insertItem(2, 'create')
        self.leftlist.insertItem(3, 'dateext')
        self.leftlist.insertItem(4, 'compress')
        self.leftlist.insertItem(5, 'extension')
        self.leftlist.insertItem(6, 'delaycompress')
        self.leftlist.insertItem(7, 'mail')
        self.leftlist.insertItem(8, 'missingok')
        self.leftlist.insertItem(9, 'olddir')
        self.leftlist.insertItem(10, 'start')
        self.leftlist.insertItem(11, 'size')
        self.leftlist.insertItem(12, 'maxage')

        self.leftlist.setCurrentRow(0)



def main():
    app = QApplication(sys.argv)
    ex = Manager()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()