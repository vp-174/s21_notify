# build/0005
# username = "geoffrea@student.21-school.ru"
# password = ""

from config import *
from create_database import *
import sys
import time
import sqlite3
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

version = "build/0005"
mute = 0
key = "s21"

create_database()

def copy_to_clipboard(text):
    '''Копирование email в бумфер обмена'''
    pyperclip.copy(text)
    tray_icon.showMessage("Уведомление", "E-mail скопирован в буфер обмена", QSystemTrayIcon.Information, 5000)
def encrypt_password(password):
    '''Шифрование пароля перед сохранением'''
    global key
    encrypted_password = base64.b64encode((password + key).encode()).decode()
    return encrypted_password
def decrypt_password(encrypted_password):
    '''Дешифровка пароля при чтении'''
    global key
    decrypted_password = base64.b64decode(encrypted_password.encode()).decode()
    decrypted_password = decrypted_password.replace(key, '')
    return decrypted_password

class CustomDialog(QDialog):
    '''Класс окна события'''
    def __init__(self, message, message2, url, event_id):
        super().__init__()
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

        # Обработчик нажатия кнопки "Подробнее"
        ok_button.clicked.connect(lambda: self.on_ok_button_clicked(url))

        cancel_button.clicked.connect(self.close)
        layout.addWidget(ok_button, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(cancel_button, 2, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(layout)

    def on_ok_button_clicked(self, url):
        mark_event_as_viewed(self.event_id)  # Отметьте событие как просмотренное
        webbrowser.open(url)  # Откройте URL
        self.close()  # Закройте диалог
class DonateDialog(QDialog):
    '''Класса окна доната'''
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
    '''Обработка сообщений события. Вывод определенного числа символов и добавление трех точек в конце'''
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

def show_notification(message, message2, event_id):
    '''Вывод окна события'''
    filename2 = 'data/02.wav'
    winsound.PlaySound(filename2, winsound.SND_FILENAME)
    url = 'https://edu.21-school.ru'
    dialog = CustomDialog(message, message2, url, event_id)  # Передаем event_id
    dialog.setFixedSize(342, 235)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)  # Установка флага WindowStaysOnTopHint
    dialog.exec()

def show_donate():
    '''Вывод кона доната'''
    url = 'https://rocketchat-student.21-school.ru/direct/66aa06b74e1904d388492898?msg=wetPQemmMd7LZa8ak'
    message2 = "Мой милый пир!\nЯ буду безумно рад,\nесли скинешь немного\n монет на энергетик...\n\nкарта (Сбербанк)\n2202 2032 1022 6652"
    dialog = DonateDialog(message2, url)
    dialog.setFixedSize(342, 235)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)  # Установка флага WindowStaysOnTopHint
    dialog.exec()

def timeWork():
    '''Показ окна события по времени (+ режим тишины)'''
    global mute
    now = datetime.now()
    now += timedelta(hours=0)
    nowHour = '{:02d}'.format(now.hour)  # Форматируем часы с ведущими нулями
    nowMin = '{:02d}'.format(now.minute)  # Форматируем минуты с ведущими нулями
    timeCheck = int(str(nowHour) + str(nowMin))  # Объединяем часы и минуты в одно число
    # print(nowHour)
    # print(nowMin)
    # print(f"mute: {mute}")
    print(f"timeCheck: {timeCheck}")
    if (timeCheck >= 900 and timeCheck <= 2300) or mute == -1:
        mute = 0
        username, password = read_credentials_from_db()
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
    '''Вывод окна авторизации'''
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
            save_credentials_to_db(username, password)
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
    '''Получение токена'''
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

def save_credentials_to_db(username, password):
    '''Сохранение шифрованных учетных данных в БД'''
    conn = DATA_BASE()
    c = conn.cursor()

    # Шифрование пароля
    encrypted_password = encrypt_password(password)

    # Вставка учетных данных в таблицу user
    c.execute('''
        INSERT INTO credentials (login, password) VALUES (?, ?)
    ''', (username, encrypted_password))

    conn.commit()
    conn.close()


def read_credentials_from_db():
    '''Чтение и расшифровка учетных данных из БД'''
    conn = DATA_BASE()
    c = conn.cursor()

    c.execute('SELECT login, password FROM credentials')
    credentials = c.fetchall()

    if credentials:
        username, encrypted_password = credentials[0]  # Предполагаем, что берем только первую запись
        password = decrypt_password(encrypted_password)
        conn.close()
        return username, password
    else:
        return None, None


def check_auth(access_token):
    '''Проверка авторизации'''
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
    '''Получение входящих событий с сервера и его вывод на экран'''
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
        # print(f"check_notify - code 200")
        events = response.json().get("events")

        if events:
            # print(f"check_notify - events OK")
            for event in events:
                # Проверяем, существует ли событие в базе данных
                if not event_exists(event['id']):  # Предполагается, что у события есть уникальный идентификатор 'id'
                    # Сохраните событие в базу данных
                    save_event_to_db(event)

                    # Показать событие
                    show_event(event)

                    # show_notification("".upper(), f"{name}\n\n{loc}\n{date_start} - {date_end}", event['id'])
                    time.sleep(5)

                elif event_exists(event['id']) and get_viewed_status(event['id']) == 0:
                    print(f"Событие с ID {event['id']} уже существует, но не просмотренно")

                    # Показать событие
                    show_event(event)

                    # show_notification("".upper(), f"{name}\n\n{loc}\n{date_start} - {date_end}", event['id'])
                    time.sleep(5)
                else:
                    print(f"Событие с ID {event['id']} уже существует в базе данных.")
        else:
            print("events empty")
        return True
    else:
        return False
def save_event_to_db(event):
    '''Сохранение события в БД'''
    conn = DATA_BASE()
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (name, description, location, start_time, end_time, event_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (event['name'], event['description'], event['location'], event['startDateTime'], event['endDateTime'], event['id']))
    conn.commit()
    conn.close()
def mark_event_as_viewed(event_id):
    '''Пометка события просмотренным'''
    conn = DATA_BASE()
    c = conn.cursor()
    c.execute('''
        UPDATE events
        SET viewed = 1
        WHERE event_id = ?
    ''', (event_id,))
    conn.commit()
    conn.close()
def event_exists(event_id):
    '''Проверка существования события в БД'''
    conn = DATA_BASE()
    c = conn.cursor()
    c.execute('''
        SELECT COUNT(*) FROM events
        WHERE event_id = ?
    ''', (event_id,))
    exists = c.fetchone()[0] > 0
    conn.close()
    return exists
def get_viewed_status(event_id):
    '''Статус события (просомтренно или нет)'''
    conn = DATA_BASE()
    c = conn.cursor()
    c.execute('''
        SELECT viewed FROM events
        WHERE event_id = ?
    ''', (event_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]  # Возвращаем значение viewed
    return None  # Если событие не найдено
def show_event(event):
    '''Формирование и показ события'''
    name = process_string(event['name'])
    if not event['description']:
        desc = ""
    else:
        desc = process_string(event['description'])
    loc = process_string(event['location'])

    date_start = event['startDateTime']
    date_time_obj1 = datetime.strptime(date_start, '%Y-%m-%dT%H:%M:%SZ')
    date_time_obj1 += timedelta(hours=5)
    date_start = date_time_obj1.strftime('%d/%m/%Y %H:%M')
    date_end = event['endDateTime']
    date_time_obj2 = datetime.strptime(date_end, '%Y-%m-%dT%H:%M:%SZ')
    date_time_obj2 += timedelta(hours=5)
    date_end = date_time_obj2.strftime('%H:%M')

    show_notification("".upper(), f"{name}\n\n{loc}\n{date_start} - {date_end}", event['id'])

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
    vers_action = QAction(version)
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

    while not read_credentials_from_db()[0]:
        show_login_window()

    if not read_credentials_from_db()[0]:
        show_login_window()
    else:
        username, password = read_credentials_from_db()
        access_token = get_access_token(username, password)

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