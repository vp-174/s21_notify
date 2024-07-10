import sys
import time
from datetime import datetime, timedelta
import requests
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import winsound
import configparser
import webbrowser

def show_login_window():
    # Окно для ввода логина и пароля
    login_dialog = QDialog()
    login_dialog.setWindowTitle("Авторизация")
    layout = QVBoxLayout()
    username_input = QLineEdit()
    password_input = QLineEdit()
    login_button = QPushButton("Авторизация")

    def authenticate():
        username = username_input.text()
        password = password_input.text()
        access_token = get_access_token(username, password)
        if access_token:
            save_token_to_file(access_token)
            login_dialog.close()

    login_button.clicked.connect(authenticate)

    layout.addWidget(QLabel("Логин:"))
    layout.addWidget(username_input)
    layout.addWidget(QLabel("Пароль:"))
    layout.addWidget(password_input)
    layout.addWidget(login_button)

    login_dialog.setLayout(layout)
    login_dialog.exec()

def get_access_token(username, password):
    # Отправка запроса на получение токена
    url = 'https://auth.sberclass.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/token'
    payload = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "client_id": "s21-open-api"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None

def save_token_to_file(token):
    # Сохранение токена в файл
    config = configparser.ConfigParser()
    config['AUTH'] = {'token': token}
    with open('data.ini', 'w') as configfile:
        config.write(configfile)

def read_token_from_file():
    # Чтение токена из файла
    config = configparser.ConfigParser()
    config.read('data.ini')
    if 'AUTH' in config:
        return config['AUTH'].get('token')
    else:
        return None

def check_auth():
    # Проверка авторизации и уведомление
    access_token = read_token_from_file()
    url = 'https://edu-api.21-school.ru/services/21-school/api/v1/events?from=2024-01-23T00%3A00%3A00Z&to=2024-01-24T00%3A00%3A00Z&type=TEST&limit=50&offset=0'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False

def check_notify(access_token):
    # Проверка авторизации на сервере
    url = 'https://edu-api.21-school.ru/services/21-school/api/v1/events?from=2024-07-09T00%3A00%3A00Z&to=2024-07-16T00%3A00%3A00Z&limit=50&offset=0'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json().get("events")
        print(events)

        # name = events[0].get('name')
        # desc = events[0].get('description')
        # loc = events[0].get('location')
        #
        # date_start = events[0].get('startDateTime')
        # date_time_obj1 = datetime.strptime(date_start, '%Y-%m-%dT%H:%M:%S')
        # # добавляем 5 часов
        # date_time_obj1 += timedelta(hours=5)
        # # преобразуем обратно в строку
        # date_start = date_time_obj1.strftime('%d/%m/%Y %H:%M')
        #
        # date_end = events[0].get('endDateTime')
        # date_time_obj2 = datetime.strptime(date_end, '%Y-%m-%dT%H:%M:%S')
        # # добавляем 5 часов
        # date_time_obj2 += timedelta(hours=5)
        # # преобразуем обратно в строку
        # date_end = date_time_obj2.strftime('%H:%M')

        for event in events:
            name = event.get('name')
            desc = event.get('description')
            loc = event.get('location')

            date_start = event.get('startDateTime')
            date_time_obj1 = datetime.strptime(date_start, '%Y-%m-%dT%H:%M:%S')
            # добавляем 5 часов
            date_time_obj1 += timedelta(hours=5)
            # преобразуем обратно в строку
            date_start = date_time_obj1.strftime('%d/%m/%Y %H:%M')

            date_end = event.get('endDateTime')
            date_time_obj2 = datetime.strptime(date_end, '%Y-%m-%dT%H:%M:%S')
            # добавляем 5 часов
            date_time_obj2 += timedelta(hours=5)
            # преобразуем обратно в строку
            date_end = date_time_obj2.strftime('%H:%M')

            show_notification("Доступны новые события".upper(), f"{name}\n\n{loc}\n{date_start} - {date_end}")
            time.sleep(5)

        # if events:
        #     show_notification("Доступны новые события".upper(), f"{name}\n\n{loc}\n{date_start} - {date_end}")
        return True
    else:
        return False


# def show_notification(message):
#     url = 'https://edu.21-school.ru'
#
#
#     # Всплывающее окно с уведомлением
#     notification = QMessageBox()
#     notification.setWindowTitle("Уведомление")
#
#     notification.setWindowFlags(Qt.FramelessWindowHint)  # Устанавливаем флаг, чтобы убрать заголовок окна
#     notification.setAttribute(Qt.WA_TranslucentBackground)
#     notification.wsize = QGuiApplication.primaryScreen().availableGeometry().size()
#     notification.wWidth = 120
#     notification.wHeight = 80
#     notification.setText(message)
#
#     # Настройка root-фона главного окна
#     palette = QPalette()
#     palette.setBrush(QPalette.Window, QColor(Qt.transparent))
#
#     notification.setPalette(palette)
#
#     pixmap = QPixmap("data/msg_bg.png")  # Путь к вашему изображению
#     notification.setAutoFillBackground(True)
#
#     # Изменяем текст кнопки на "Перейти"
#     ok_button = notification.addButton("Перейти", QMessageBox.AcceptRole)
#     cancel_button = notification.addButton(QMessageBox.Cancel)
#
#     # Устанавливаем стиль кнопок
#     ok_button.setStyleSheet("background-color: #4CAF50; color: white; border: 2px solid #4CAF50; border-radius: 5px; padding: 3px;")
#     cancel_button.setStyleSheet("background-color: #4CAF50; color: white; border: 2px solid #4CAF50; border-radius: 5px; padding: 3px;")
#
#     notification.exec()
#
#     # При нажатии на кнопку "Перейти" открываем указанный URL
#     if notification.clickedButton() == ok_button:
#         webbrowser.open(url)

class CustomDialog(QDialog):
    def __init__(self, message, message2, url):
        super().__init__()

        self.setWindowTitle("Уведомление")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove window frame
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setAutoFillBackground(True)
        # self.setStyleSheet("background-image: url('data/msg_bg.png');")

        # layout = QVBoxLayout()
        layout = QGridLayout()
        bg = QWidget()
        bg.setStyleSheet("background-image: url('data/msg_bg2.png') no-repeat center center fixed; padding: 0px")
        bg.setContentsMargins(0, 0, 0, 0)

        # Add background image
        layout.addWidget(bg,0,0,3,3)

        # Add message text
        message_label = QLabel(message)
        layout.addWidget(message_label,0,0,0,2, alignment=Qt.AlignmentFlag.AlignHCenter)
        message_label2 = QLabel(message2)
        layout.addWidget(message_label2,1,0,1,2, alignment=Qt.AlignmentFlag.AlignHCenter)

        msg_style = """
            QLabel {
                    font-size: 18px;
                    font-weight: 700;
                    min-width: 316px;
                    max-width: 342px;
                    margin-top: 10px;
                    margin-left: 20px;
                }
                
            QPushButton {
                min-width: 100px; 
                max-width: 120px; 
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 6px;
                margin-bottom: 20px;
                margin-left: 2px;
            }
            
            QPushButton:hover {
                background-color: #6CBFD4;
            }
        """
        message_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        message_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet(msg_style)
        message_label2.setStyleSheet("font-size: 14px; margin-bottom: 20px")

        # Add "Перейти" button
        ok_button = QPushButton("Подробнее")
        cancel_button = QPushButton("Закрыть")

        # ok_button.setStyleSheet("min-width: 100px; max-width: 120px; background-color: #4CAF50; color: white; border: 2px solid #4CAF50; border-radius: 5px; padding: 3px;")
        # cancel_button.setStyleSheet("min-width: 100px; max-width: 120px; background-color: #4CAF50; color: white; border: 2px solid #4CAF50; border-radius: 5px; padding: 3px;")
        ok_button.setStyleSheet(msg_style)
        cancel_button.setStyleSheet(msg_style)

        ok_button.clicked.connect(lambda: webbrowser.open(url))
        cancel_button.clicked.connect(lambda: self.close())

        # layout.addWidget(layoutH)
        layout.addWidget(ok_button,2,0, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(cancel_button,2,1, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)


def show_notification(message, message2):
    filename2 = 'data/02.wav'
    winsound.PlaySound(filename2, winsound.SND_FILENAME)
    url = 'https://edu.21-school.ru'
    # image_path = "data/msg_bg.png"  # Path to your image

    dialog = CustomDialog(message, message2, url)
    dialog.setFixedSize(342, 235)  # Set window size
    dialog.exec()

def exit_action():
    # Выход из приложения
    print("Выход из приложения")
    app.quit()

def settings_action():
    # Выход из приложения
    print("Настройки приложения")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    tray_icon = QSystemTrayIcon(QIcon("data/icon.png"), app)
    tray_icon.setToolTip("Жду новые события")
    menu = QMenu()
    exit_action = QAction("Выход", triggered=exit_action)
    settings_action = QAction("Настройки", triggered=settings_action)
    menu.addAction(exit_action)
    menu.addAction(settings_action)
    tray_icon.setContextMenu(menu)
    tray_icon.show()

    if not read_token_from_file():
        show_login_window()
    else:
        if check_auth():
            tray_icon.showMessage("Уведомление", "Успешная авторизация", QSystemTrayIcon.Information, 5000)
            filename1 = 'data/01.wav'
            winsound.PlaySound(filename1, winsound.SND_FILENAME)
            access_token = read_token_from_file()
            timer = QTimer()
            timer.timeout.connect(lambda: check_notify(access_token))
            timer.start(5000)  # Проверка авторизации каждые 15 сек
        else:
            tray_icon.showMessage("Уведомление", "Ошибка авторизации", QSystemTrayIcon.Information, 5000)

    sys.exit(app.exec())