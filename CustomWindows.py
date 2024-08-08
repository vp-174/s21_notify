from Imports import *

class CustomDialog(QDialog):
    '''Класс окна события'''
    def __init__(self, message, message2, url, event_id):
        super().__init__()
        self.database = Database()
        self.event_id = event_id  # Сохраняем идентификатор события
        self.setWindowTitle("Уведомление")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)
        layout = QGridLayout()
        bg = QWidget()
        bg.setStyleSheet("background-image: url('data/msg_bg.png'); background-repeat: no-repeat; background-position: 50%; padding: 0px")
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
        message_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        message_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet(msg_style)
        message_label2.setStyleSheet("font-size: 14px; margin-bottom: 20px; font-weight: 500;")
        ok_button = QPushButton("Подробнее")
        cancel_button = QPushButton("Закрыть")

        # Установка objectName
        ok_button.setObjectName("ok_button")
        cancel_button.setObjectName("cancel_button")

        ok_button.setStyleSheet(msg_style)
        cancel_button.setStyleSheet(msg_style)

        # Обработчик нажатия кнопки "Подробнее"
        ok_button.clicked.connect(lambda: self.on_ok_button_clicked(url))

        cancel_button.clicked.connect(self.close)
        layout.addWidget(ok_button, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(cancel_button, 2, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

    def on_ok_button_clicked(self, url):
        self.database.mark_event_as_viewed(self.event_id)  # Отметьте событие как просмотренное
        webbrowser.open(url)  # Откройте URL
        self.close()  # Закройте диалог

class DonateDialog(QDialog):
    '''Класса окна доната'''
    def __init__(self, message, url, tr):
        super().__init__()
        self.classTray = tr
        self.setWindowTitle("Уведомление")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)

        layout = QGridLayout()
        bg = QWidget()
        bg.setStyleSheet("background-image: url('data/msg_bg.png'); background-repeat: no-repeat; background-position: 50%; padding: 0px");
        bg.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(bg, 0, 0, 3, 3)
        image_label = QWidget()
        image_label.setStyleSheet("background-image: url('data/donat_qr.png'); background-repeat: no-repeat; background-position: 50%; margin: 25 158 0 0");
        layout.addWidget(image_label, 0, 0, 3, 3)
        message_label = QLabel(message)
        layout.addWidget(message_label, 1, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        msg_style = """
            QLabel#msg {
                font-size: 13px;
                margin: 0 50 19 0;
            }

            QWidget#qrcode {
                background-image: url('data/donat_qr.png');
                background-repeat: no-repeat;
                background-position: 50%; 
                margin: 65 150 0 0;
            }

            QPushButton#ok_button {
                min-width: 100px; 
                max-width: 150px; 
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
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ok_button = QPushButton("abasecode@gmail.com")
        cancel_button = QPushButton("Закрыть")

        # Установка objectName
        image_label.setObjectName("qrcode")
        message_label.setObjectName("msg")
        ok_button.setObjectName("ok_button")
        cancel_button.setObjectName("cancel_button")

        image_label.setStyleSheet(msg_style)
        message_label.setStyleSheet(msg_style)
        ok_button.setStyleSheet(msg_style)
        cancel_button.setStyleSheet(msg_style)
        # ok_button.clicked.connect(lambda: webbrowser.open(url))
        ok_button.clicked.connect(lambda: self.copy_mail_to_clipboard("abasecode@gmail.com"))
        # ok_button.clicked.connect(self.close)
        cancel_button.clicked.connect(lambda: self.close())
        layout.addWidget(ok_button, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(cancel_button, 2, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

    def copy_mail_to_clipboard(self, text):
        '''Копирование email в бумфер обмена'''
        pyperclip.copy(text)
        self.classTray.icon.showMessage("Уведомление", "E-mail скопирован в буфер обмена", QSystemTrayIcon.Information, 5000)
        # self.show_message("Уведомление", "E-mail скопирован в буфер обмена")