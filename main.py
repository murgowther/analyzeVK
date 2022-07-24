from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
import requests
import json
import os
import time
from all_modules import main
from FriendsGraph.friends_graph import main_friends
import all_analitic
import io

from auth_data import token



class PageWindow(QtWidgets.QMainWindow):

    gotoSignal = QtCore.pyqtSignal(str)
    def goto(self, name):
        self.gotoSignal.emit(name)

class MainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setWindowIcon(QtGui.QIcon('source/favicon.ico'))
        self.initUI()
        self.setWindowTitle("Досье")
        self.setObjectName("MainWindow")
    def initUI(self):
        self.UiComponents()

    def UiComponents(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-image:url(source/stars.jpg)")
        self.centralwidget.setFixedSize(1280, 826)
        #лого
        self.mainlogo = QtWidgets.QLabel(self.centralwidget)
        self.mainlogo.setPixmap(QtGui.QPixmap("source/1.png"))
        self.mainlogo.setObjectName("mainlogo")
        self.mainlogo.setGeometry(QtCore.QRect(20, 50, 180, 170))

        self.label1 = QtWidgets.QLabel("Анализ данных", self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(215, 65, 490, 80))
        self.label1.setStyleSheet("color: white;\n"
                                   "font: 38pt \"Trebuchet MS\";\n"
                                   )
        self.label2 = QtWidgets.QLabel("«ДОСЬЕ»", self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(280, 150, 490, 60))
        self.label2.setStyleSheet("color: white;\n"
                                  "font: 36pt \"Trebuchet MS\";\n"
                                  )
        # шарик
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(765, 230, 380, 380))
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.path = 'source/Планета1.gif'
        self.gif = QtGui.QMovie(self.path)  # !!!
        self.label.setMovie(self.gif)
        self.gif.start()
        #Кнопка
        self.searchButton = QtWidgets.QPushButton("Анализировать", self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(230, 520, 300, 50))
        self.searchButton.setStyleSheet("color: white;\n"
                                        "font: 25pt \"Trebuchet MS\";\n"
                                        )
        self.searchButton.clicked.connect(
            self.make_handleButton("Analyze")
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "Analyze":
                self.goto("Analyze")

        return handleButton


class Analyze(PageWindow):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setWindowIcon(QtGui.QIcon('source/favicon.ico'))
        self.initUI()
        self.setWindowTitle("Анализ")
        self.setObjectName("Analyze")
    def initUI(self):
        self.UiComponents()

    def UiComponents(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-image:url(source/stars.jpg)")
        self.centralwidget.setFixedSize(1280, 826)
        self.label1 = QtWidgets.QLabel("Введите id страницы:", self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(40, 20, 250, 30))
        self.label1.setStyleSheet("color: white;\n"
                                  "font: 12pt \"Trebuchet MS\";\n"
                                  )
        self.input_id = QtWidgets.QLineEdit(self.centralwidget)
        self.input_id.setGeometry(QtCore.QRect(300, 19, 200, 30))
        self.input_id.setStyleSheet(
                                    "font: 14pt \"Trebuchet MS\";\n"
                                    "color: white;")
        self.label2 = QtWidgets.QLabel("Введите id страницы (цифры):", self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(40, 60, 250, 30))
        self.label2.setStyleSheet("color: white;\n"
                                  "font: 12pt \"Trebuchet MS\";\n"
                                  )
        self.input_id2 = QtWidgets.QLineEdit(self.centralwidget)
        self.input_id2.setGeometry(QtCore.QRect(300, 59, 200, 30))
        self.input_id2.setStyleSheet(
            "font: 14pt \"Trebuchet MS\";\n"
            "color: white;")
        self.searchButton = QtWidgets.QPushButton("Поиск", self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(520, 40, 180, 35))
        self.searchButton.setStyleSheet("color: white;\n"
                                        "font: 18pt \"Trebuchet MS\";\n"
                                        )
        self.searchButton.clicked.connect(self.zabor)
        self.label3 = QtWidgets.QLabel("Название группы:", self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(710, 20, 250, 30))
        self.label3.setStyleSheet("color: white;\n"
                                  "font: 12pt \"Trebuchet MS\";\n"
                                  )
        self.label4 = QtWidgets.QLabel("Запрещённые слова \n в группах:", self.centralwidget)
        self.label4.setGeometry(QtCore.QRect(710, 50, 250, 38))
        self.label4.setStyleSheet("color: white;\n"
                                  "font: 12pt \"Trebuchet MS\";\n"
                                  )
        self.label5 = QtWidgets.QLabel("Запрещённые слова \n в комм-ях:", self.centralwidget)
        self.label5.setGeometry(QtCore.QRect(710, 100, 250, 38))
        self.label5.setStyleSheet("color: white;\n"
                                  "font: 12pt \"Trebuchet MS\";\n"
                                  )

        self.input_result = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.input_result.setGeometry(QtCore.QRect(50, 110, 580, 690))
        self.input_result.setStyleSheet(
                                    "font: 18pt \"Trebuchet MS\";\n"
                                    "color: white;\n")
        self.input_result2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.input_result2.setGeometry(QtCore.QRect(670, 210, 570, 590))
        self.input_result2.setStyleSheet(
            "font: 20pt \"Trebuchet MS\";\n"
            "color: white;\n")
        self.aButton = QtWidgets.QPushButton("Анализировать", self.centralwidget)
        self.aButton.setGeometry(QtCore.QRect(850, 150, 270, 45))
        self.aButton.setStyleSheet("color: white;\n"
                                        "font: 18pt \"Trebuchet MS\";\n"
                                        )
        self.aButton.clicked.connect(self.analyze)
        self.input_id3 = QtWidgets.QLineEdit(self.centralwidget)
        self.input_id3.setGeometry(QtCore.QRect(900, 19, 200, 30))
        self.input_id3.setStyleSheet(
            "font: 14pt \"Trebuchet MS\";\n"
            "color: white;")
        self.input_id4 = QtWidgets.QLineEdit(self.centralwidget)
        self.input_id4.setGeometry(QtCore.QRect(900, 59, 200, 30))
        self.input_id4.setStyleSheet(
            "font: 14pt \"Trebuchet MS\";\n"
            "color: white;")
        self.input_id5 = QtWidgets.QLineEdit(self.centralwidget)
        self.input_id5.setGeometry(QtCore.QRect(900, 99, 200, 30))
        self.input_id5.setStyleSheet(
            "font: 14pt \"Trebuchet MS\";\n"
            "color: white;")
    def zabor(self):
        self.id = self.input_id.text()
        self.zifr = self.input_id2.text()
        main(self.id, self.zifr)
        main_friends(self.id)
        self.input_result.setPlainText("===Основная информация===")
        with open(f"{self.id}/main_Info_{self.id}.txt", 'r', encoding="utf-8") as f:
            # считываем сразу весь файл
            data = f.read()
            self.input_result.appendPlainText(data)
        self.input_result.appendPlainText("===Существующие посты===")
        with open(f"{self.id}/exist_posts_{self.id}.txt") as f:
            l = f.read().splitlines()
        for i in l:
            with io.open(f"{self.id}/text_comment{i}_{self.id}.txt", encoding='utf-8') as f:
                data = f.read()
                self.input_result.appendPlainText(data)
        self.input_result.appendPlainText("===Перечень групп===")
        with open(f"{self.id}/groups_{self.id}.txt", 'r', encoding="utf-8") as f:
            # считываем сразу весь файл
            data = f.read()
            self.input_result.appendPlainText(data)

    def analyze(self):
        self.group = self.input_id3.text()
        self.slovo = self.input_id4.text()
        self.comm = self.input_id5.text()
        all_analitic.main(self.group, self.slovo, self.comm)
        with open(f"{self.id}/Rezult_{self.id}.txt", 'r', encoding="utf-8") as f:
            # считываем сразу весь файл
            data = f.read()
            self.input_result2.appendPlainText(data)
        self.input_result2.appendPlainText("============")
        with open(f"{self.id}/Rezult_comment_{self.id}.txt", 'r', encoding="utf-8") as f:
            # считываем сразу весь файл
            data = f.read()
            self.input_result2.appendPlainText(data)



class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1280, 826)
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.m_pages = {}
        self.register(MainWindow(), "main")
        self.register(Analyze(), "Analyze")
        self.goto("main")

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
