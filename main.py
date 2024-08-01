# build/0003
# username = "geoffrea@student.21-school.ru"
# password = ""

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
import base64
import pyperclip

version = "build/0003"
mute = 0
key = "s21"

def copy_to_clipboard(text):
    pyperclip.copy(text)
    tray_icon.showMessage("Уведомление", "E-mail скопирован в буфер", QSystemTrayIcon.Information, 5000)

# Шифрование пароля перед сохранением
def encrypt_password(password):
    global key
    encrypted_password = base64.b64encode((password + key).encode()).decode()
    return encrypted_password

# Дешифровка пароля при чтении
def decrypt_password(encrypted_password):
    global key
    decrypted_password = base64.b64decode(encrypted_password.encode()).decode()
    decrypted_password = decrypted_password.replace(key, '')
    return decrypted_password

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
                    min-width: 316px;
                    max-width: 342px;
                    margin-top: 10px;
                    margin-left: 0px;
            }

            QPushButton {
                min-width: 100px; 
                max-width: 120px; 
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 6px;
                margin-bottom: 14px;
                margin-left: 15px;
                margin-right: 15px;
            }

            QPushButton:hover {
                background-color: #6CBFD4;
            }
        """
        message_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        message_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet(msg_style)
        message_label2.setStyleSheet("font-size: 14px; margin-bottom: 20px; font-weight: 500;")
        ok_button = QPushButton("Подробнее")
        cancel_button = QPushButton("Закрыть")
        ok_button.setStyleSheet(msg_style)
        cancel_button.setStyleSheet(msg_style)
        ok_button.clicked.connect(lambda: webbrowser.open(url))
        ok_button.clicked.connect(self.close)
        cancel_button.clicked.connect(lambda: self.close())
        layout.addWidget(ok_button, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(cancel_button, 2, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

class DonateDialog(QDialog):
    def __init__(self, message, url):
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
        image_label = QWidget()
        image_label.setStyleSheet("background-image: url('data/donat_qr.png'); background-repeat: no-repeat; background-position: 50%; margin: 25 158 0 0");
        layout.addWidget(image_label, 0, 0, 3, 3)
        message_label = QLabel(message)
        layout.addWidget(message_label, 1, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        msg_style = """
            QLabel {
                    font-size: 18px;
                    font-weight: 700;
                    min-width: 316px;
                    max-width: 342px;
                    margin-top: 10px;
                    margin-left: 0px;
            }

            QPushButton {
                min-width: 100px; 
                max-width: 150px; 
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 6px;
                margin-bottom: 14px;
                margin-left: 15px;
                margin-right: 15px;
            }

            QPushButton:hover {
                background-color: #6CBFD4;
            }
        """
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        message_label.setStyleSheet("font-size: 14px; margin-bottom: 10px; font-weight: 500;")
        ok_button = QPushButton("abasecode@gmail.com")
        cancel_button = QPushButton("Закрыть")
        ok_button.setStyleSheet(msg_style)
        cancel_button.setStyleSheet(msg_style)
        # ok_button.clicked.connect(lambda: webbrowser.open(url))
        ok_button.clicked.connect(lambda: copy_to_clipboard("abasecode@gmail.com"))
        # ok_button.clicked.connect(self.close)
        cancel_button.clicked.connect(lambda: self.close())
        layout.addWidget(ok_button, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(cancel_button, 2, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

def process_string(sentence):
    words = sentence.split()
    new_sentence = ""
    word_count = 0
    for word in words:
        if len(word) > 1:  # Проверяем, что слово содержит более одной буквы
            word_count += 1
            if word_count % 3 == 0:  # Перенос строки после каждого третьего слова
                new_sentence += word + "\n"
            else:
                new_sentence += word + " "
        else:
            new_sentence += word + " "

    if len(new_sentence) > 43:  # Проверяем длину предложения
        new_sentence = new_sentence[:43] + "..."  # Обрезаем и добавляем три точки в конце

    return new_sentence

def show_notification(message, message2):
    filename2 = 'data/02.wav'
    winsound.PlaySound(filename2, winsound.SND_FILENAME)
    url = 'https://edu.21-school.ru'
    dialog = CustomDialog(message, message2, url)
    dialog.setFixedSize(342, 235)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)  # Установка флага WindowStaysOnTopHint
    dialog.exec()

def show_donate():
    # filename2 = 'data/02.wav'
    # winsound.PlaySound(filename2, winsound.SND_FILENAME)
    url = 'https://rocketchat-student.21-school.ru/direct/66aa06b74e1904d388492898?msg=wetPQemmMd7LZa8ak'
    message2 = "Мой милый пир!\nЯ буду безумно рад,\nесли скинешь немного\n монет на энергетик...\n\nкарта (Сбербанк)\n2202 2032 1022 6652"
    dialog = DonateDialog(message2, url)
    dialog.setFixedSize(342, 235)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)  # Установка флага WindowStaysOnTopHint
    dialog.exec()

# def timeWork(access_token):
#     global mute
#     now = datetime.now()
#     now += timedelta(hours=0)
#     nowHour = now.hour
#     nowMin = now.minute
#     timeCheck = int(str(nowHour) + str(nowMin))
#     # print(nowHour)
#     # print(nowMin)
#     print(timeCheck)
#     if timeCheck >= 1625 and timeCheck <= 1636:
#         #mute = 0
#         check_notify(access_token)
#     else:
#         mute += 1
#         # print(mute)
#         if mute == 1:
#             tray_icon.showMessage("Включен режим тишины", "Уведомления о событиях\n отключены до 9:00 утра", QSystemTrayIcon.Information, 10000)
#         elif mute > 1:
#             print(f"[ MUTE MODE ]")
#             if timeCheck > 1642:
#                 mute = 0

def timeWork():
    global mute
    now = datetime.now()
    now += timedelta(hours=0)
    nowHour = '{:02d}'.format(now.hour)  # Форматируем часы с ведущими нулями
    nowMin = '{:02d}'.format(now.minute)  # Форматируем минуты с ведущими нулями
    timeCheck = int(str(nowHour) + str(nowMin))  # Объединяем часы и минуты в одно число
    # print(nowHour)
    # print(nowMin)
    print(f"mute: {mute}")
    print(f"timeCheck: {timeCheck}")
    if (timeCheck >= 900 and timeCheck <= 2300) or mute == -1:
        mute = 0
        username, password = read_credentials_from_file()
        access_token = get_access_token(username, password)
        check_notify(access_token)
    else:
        mute += 1
        # print(mute)
    if mute == 1:
        tray_icon.showMessage("Включен режим тишины", "Уведомления о событиях\n отключены до 9:00 утра", QSystemTrayIcon.Information, 10000)
    elif mute > 1:
        print(f"[ MUTE MODE ]")
        if timeCheck >= 859 and timeCheck <= 1100:
            mute = -1

def show_login_window():
    global key
    login_dialog = QDialog()
    login_dialog.setWindowTitle("Авторизация")
    login_dialog.setWindowFlags(Qt.FramelessWindowHint)
    layout = QVBoxLayout()
    username_input = QLineEdit()
    password_input = QLineEdit()
    password_input.setEchoMode(QLineEdit.Password)
    login_button = QPushButton("Авторизация")
    exit_button = QPushButton("Выйти")

    def authenticate():
        global key
        username = username_input.text()
        password = password_input.text()
        access_token = get_access_token(username, password)
        if access_token:
            save_credentials_to_file(username, password)
            login_dialog.close()

    login_button.clicked.connect(authenticate)
    exit_button.clicked.connect(lambda: sys.exit())

    layout.addWidget(QLabel("Логин:"))
    layout.addWidget(username_input)
    layout.addWidget(QLabel("Пароль:"))
    layout.addWidget(password_input)
    layout.addWidget(login_button)
    layout.addWidget(exit_button)
    login_dialog.setLayout(layout)
    login_dialog.exec()

def get_access_token(username, password):
    url = 'https://auth.sberclass.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/token'
    payload = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "client_id": "s21-open-api"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        # time.sleep(3)
        # tray_icon.showMessage("Уведомление", "Токен получен", QSystemTrayIcon.Information, 5000)
        # filename1 = 'data/01.wav'
        # winsound.PlaySound(filename1, winsound.SND_FILENAME)
        return response.json().get("access_token")
    else:
        return None

# def save_credentials_to_file(username, password):
#     config = configparser.ConfigParser()
#     config['AUTH'] = {'username': username, 'password': password}
#     with open('data.ini', 'w') as configfile:
#         config.write(configfile)
#
# def read_credentials_from_file():
#     config = configparser.ConfigParser()
#     config.read('data.ini')
#     if 'AUTH' in config:
#         return config['AUTH'].get('username'), config['AUTH'].get('password')
#     else:
#         return None, None

# Сохранение шифрованных учетных данных в файл
def save_credentials_to_file(username, password):
    config = configparser.ConfigParser()
    encrypted_password = encrypt_password(password)
    config['AUTH'] = {'username': username, 'password': encrypted_password}
    with open('data.ini', 'w') as configfile:
        config.write(configfile)

# Чтение и расшифровка учетных данных из файла
def read_credentials_from_file():
    config = configparser.ConfigParser()
    config.read('data.ini')
    if 'AUTH' in config:
        username = config['AUTH'].get('username')
        encrypted_password = config['AUTH'].get('password')
        password = decrypt_password(encrypted_password)
        return username, password
    else:
        return None, None

def check_auth(access_token):
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
    now = datetime.now()
    from_date = now - timedelta(hours=5)
    to_date = now + relativedelta(months=3)
    from_str = from_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    to_str = to_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    url = f'https://edu-api.21-school.ru/services/21-school/api/v1/events?from={from_str}&to={to_str}&limit=50&offset=0'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"check_notify - code 200")
        events = response.json().get("events")
        # print(events)
        if events:
            print(f"check_notify - events OK")
            for event in events:
                name = process_string(event.get('name'))
                desc = process_string(event.get('description'))
                loc = process_string(event.get('location'))
                date_start = event.get('startDateTime')
                date_time_obj1 = datetime.strptime(date_start, '%Y-%m-%dT%H:%M:%SZ')
                date_time_obj1 += timedelta(hours=5)
                date_start = date_time_obj1.strftime('%d/%m/%Y %H:%M')
                date_end = event.get('endDateTime')
                date_time_obj2 = datetime.strptime(date_end, '%Y-%m-%dT%H:%M:%SZ')
                date_time_obj2 += timedelta(hours=5)
                date_end = date_time_obj2.strftime('%H:%M')
                show_notification("".upper(), f"{name}\n\n{loc}\n{date_start} - {date_end}")
                time.sleep(5)
        else:
            print("events empty")
        return True
    else:
        return False

def exit_action():
    sys.exit()

def settings_action():
    print("Настройки приложения")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_icon = QIcon('data/icon.ico')
    app.setWindowIcon(app_icon)
    app.setQuitOnLastWindowClosed(False)
    tray_icon = QSystemTrayIcon(QIcon("data/icon.png"), app)
    tray_icon.setToolTip(f"S21 Notify {version}\nУведомление о новых событиях")
    menu = QMenu()
    vers_action = QAction("build/0002")
    vers_action.setEnabled(False)
    settings_action = QAction("Настройки", triggered=settings_action)
    donate_action = QAction("Задонатить", triggered=show_donate)
    settings_action.setEnabled(False)
    exit_action = QAction("Выход", triggered=exit_action)
    menu.addAction(vers_action)
    menu.addAction(settings_action)
    menu.addAction(donate_action)
    menu.addAction(exit_action)
    tray_icon.setContextMenu(menu)
    tray_icon.show()

    while not read_credentials_from_file()[0]:
        show_login_window()

    if not read_credentials_from_file()[0]:
        show_login_window()
    else:
        username, password = read_credentials_from_file()
        access_token = get_access_token(username, password)

        # def update_token():
        #     username, password = read_credentials_from_file()
        #     new_access_token = get_access_token(username, password)
        #     if new_access_token:
        #         access_token = new_access_token
        #         tray_icon.showMessage("Уведомление", "Токен обновлен", QSystemTrayIcon.Information, 5000)
        #
        # # Создание таймера для обновления токена каждые 6 часов
        # timer1 = QTimer()
        # timer1.timeout.connect(update_token)
        # timer1.start(6 * 3600 * 1000)  # 6 часов в миллисекундах

        if check_auth(access_token):
            time.sleep(5)
            tray_icon.showMessage("Уведомление", "Успешная авторизация", QSystemTrayIcon.Information, 5000)
            filename1 = 'data/01.wav'
            winsound.PlaySound(filename1, winsound.SND_FILENAME)
            time.sleep(10)
            timeWork()
            timer2 = QTimer()
            timer2.timeout.connect(lambda: timeWork())
            timer2.start(60 * 60000)
        else:
            tray_icon.showMessage("Уведомление", "Ошибка авторизации", QSystemTrayIcon.Information, 5000)

    sys.exit(app.exec())