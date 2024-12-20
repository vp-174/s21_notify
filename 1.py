# 1я версия без ооп
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

class DonateDialog(QDialog):
    def __init__(self, message2, url):
        super().__init__()
        self.setWindowTitle("Уведомление")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)

        # image_label = QLabel()
        # pixmap = QPixmap('data/donat_qr.jpg')  # Путь к вашему изображению
        # pixmap.scaledToWidth(128)
        # image_label.setPixmap(pixmap)
        # image_label.setFixedSize(64, 64)
        # image_label.setAlignment(Qt.AlignCenter)

        layout = QGridLayout()
        bg = QWidget()
        bg.setStyleSheet("background-image: url('data/msg_bg.png'); background-repeat: no-repeat; background-position: 50%; padding: 0px");
        bg.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(bg, 0, 0, 3, 3)
        image_label = QWidget()
        # image_label.setStyleSheet("background-image: url('data/donat_qr.png'); background-repeat: no-repeat; background-position: 50%; margin: 25 158 0 0");
        # message_label = QLabel(message)
        # layout.addWidget(message_label, 0, 0, 0, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(image_label, 0, 0, 3, 3)
        message_label2 = QLabel(message2)
        layout.addWidget(message_label2, 1, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        msg_style = """
            QLabel#msg2 {
                font-size: 13px;
                margin: 0 33 19 0;
            }
            
            QWidget#qrcode {
                background-image: url('data/donat_qr.png');
                background-repeat: no-repeat;
                background-position: 50%; 
                margin: 65 150 0 0;
            }

            QPushButton#ok_button {
                min-width: 100px; 
                max-width: 120px; 
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
        # message_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        message_label2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # message_label.setStyleSheet(msg_style)
        ok_button = QPushButton("Написать")
        cancel_button = QPushButton("Закрыть")

        # Установка objectName
        image_label.setObjectName("qrcode")
        message_label2.setObjectName("msg2")
        ok_button.setObjectName("ok_button")
        cancel_button.setObjectName("cancel_button")

        message_label2.setStyleSheet(msg_style)
        image_label.setStyleSheet(msg_style)
        ok_button.setStyleSheet(msg_style)
        cancel_button.setStyleSheet(msg_style)
        ok_button.clicked.connect(lambda: webbrowser.open(url))
        ok_button.clicked.connect(self.close)
        cancel_button.clicked.connect(lambda: self.close())
        layout.addWidget(ok_button, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(cancel_button, 2, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

def show_donate():
    # filename2 = 'data/02.wav'
    # winsound.PlaySound(filename2, winsound.SND_FILENAME)
    url = 'https://rocketchat-student.21-school.ru/direct/66aa06b74e1904d388492898?msg=wetPQemmMd7LZa8ak'
    message2 = "Дорогой пир!\nЯ буду безумно рад\nтвоей благодарности\nна кофе с печеньками.\n\nкарта (Сбербанк)\n2202 2032 1022 6652"
    dialog = DonateDialog(message2, url)
    dialog.setFixedSize(422, 315)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)  # Установка флага WindowStaysOnTopHint
    dialog.exec()

app = QApplication(sys.argv)
app_icon = QIcon('data/icon.ico')
app.setWindowIcon(app_icon)
app.setQuitOnLastWindowClosed(False)
show_donate()
