#для тестов
import sys
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import winsound
import configparser
import webbrowser


class CustomDialog(QDialog):
    def __init__(self, message, message2, url):
        super().__init__()
        self.setWindowTitle("Уведомление")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)
        layout = QGridLayout()
        bg = QWidget()
        bg.setStyleSheet("background-image: url('data/msg_bg.png'); background-repeat: no-repeat; background-position: 50%; padding: 0px");
        bg.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(bg, 0, 0, 3, 3)
        message_label = QLabel(message)
        layout.addWidget(message_label, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignHCenter)
        message_label2 = QLabel(message2)
        layout.addWidget(message_label2, 0, 0, 3, 3, alignment=Qt.AlignmentFlag.AlignHCenter)



        msg_style = """
            QLabel {
                    font-size: 18px;
                    font-weight: 700;
                    min-width: 396px;
                    max-width: 422px;
                    margin-top: 10px;
                    margin-left: 0px;
            }

            QPushButton#ok_button {
                min-width: 60px; 
                max-width: 80px; 
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 6px;
                margin-bottom: 54px;
                margin-left: 55px;
            }
            
            QPushButton#ok_button:hover {
                background-color: #6CBFD4;
            }
            
            QPushButton#no_button {
                min-width: 80px; 
                max-width: 100px; 
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 6px;
                margin-bottom: 54px;
                margin-left: 0px;
            }
            
            QPushButton#no_button:hover {
                background-color: #6CBFD4;
            }
            
            QPushButton#cancel_button {
                min-width: 100px; 
                max-width: 120px; 
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 6px;
                margin-bottom: 54px;
                margin-right: 55px;
            }
            
            QPushButton#cancel_button:hover {
                background-color: #6CBFD4;
            }
        """
        message_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        message_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet(msg_style)
        message_label2.setStyleSheet("font-size: 14px; margin-bottom: 20px; font-weight: 500;")
        ok_button = QPushButton("Пойду")
        no_button = QPushButton("Не пойду")
        cancel_button = QPushButton("Решу позже")

        # Установка objectName для кнопок
        ok_button.setObjectName("ok_button")
        no_button.setObjectName("no_button")
        cancel_button.setObjectName("cancel_button")

        ok_button.setStyleSheet(msg_style)
        no_button.setStyleSheet(msg_style)
        cancel_button.setStyleSheet(msg_style)

        ok_button.clicked.connect(lambda: webbrowser.open(url))
        ok_button.clicked.connect(self.close)
        cancel_button.clicked.connect(lambda: self.close())

        layout.addWidget(ok_button, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(no_button, 2, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(cancel_button, 2, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

def show_notification(message, message2):
    # filename2 = 'data/02.wav'
    # winsound.PlaySound(filename2, winsound.SND_FILENAME)
    url = 'https://edu.21-school.ru'
    dialog = CustomDialog(message, message2, url)
    dialog.setFixedSize(422, 315)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)  # Установка флага WindowStaysOnTopHint
    dialog.exec()

app = QApplication(sys.argv)
app_icon = QIcon('data/icon.ico')
app.setWindowIcon(app_icon)
app.setQuitOnLastWindowClosed(False)

show_notification("","расскажем новости, ответим на вопросы,\n поболтаем о том о сём")
