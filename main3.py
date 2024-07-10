import sys
import requests
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import winsound
import configparser

def save_token_to_file(token):
    config = configparser.ConfigParser()
    config['AUTH'] = {'token': token}
    with open('data.ini', 'w') as configfile:
        config.write(configfile)

def read_token_from_file():
    config = configparser.ConfigParser()
    config.read('data.ini')
    if 'AUTH' in config:
        return config['AUTH'].get('token')
    else:
        return None

def show_login_dialog():
    dialog = QDialog()
    dialog.setWindowTitle("Аутентификация")
    layout = QVBoxLayout()
    username_label = QLabel("Логин:")
    username_edit = QLineEdit()
    password_label = QLabel("Пароль:")
    password_edit = QLineEdit()
    save_button = QPushButton("Сохранить")

    layout.addWidget(username_label)
    layout.addWidget(username_edit)
    layout.addWidget(password_label)
    layout.addWidget(password_edit)
    layout.addWidget(save_button)

    dialog.setLayout(layout)

    save_button.clicked.connect(lambda: save_credentials(username_edit.text(), password_edit.text(), dialog))

    dialog.exec()

def save_credentials(username, password, dialog):
    access_token = get_access_token(username, password)
    if access_token:
        save_token_to_file(access_token)
        dialog.accept()
    else:
        QMessageBox.warning(None, "Ошибка", "Неверный логин или пароль")
        dialog.reject()

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
        return response.json().get("access_token")
    else:
        return None

def check_auth_and_notify():
    try:
        access_token = read_token_from_file()
        if not access_token:
            show_login_dialog()
            access_token = read_token_from_file()

        if access_token and check_auth(access_token):
            filename = 'data/01.wav'
            winsound.PlaySound(filename, winsound.SND_FILENAME)
            tray_icon.showMessage("Уведомление", "Успешная авторизация", QSystemTrayIcon.Information, 1000)
    except Exception as e:
        print(f"Error: {e}")

def check_auth(access_token):
    url = 'https://edu-api.21-school.ru/services/21-school/api/v1/events?from=2024-01-23T00%3A00%3A00Z&to=2024-01-24T00%3A00%3A00Z&type=TEST&limit=50&offset=0'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.json().get("events"))  # здесь приходит event
        return True
    else:
        return False

def exit_action():
    print("Exiting the application")
    app.quit()

def show_notification(message):
    notification = QMessageBox()
    notification.setWindowTitle("Уведомление")
    notification.setText(message)
    notification.setStandardButtons(QMessageBox.Ok)
    notification.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray_icon = QSystemTrayIcon(QIcon("data/icon.png"), app)
    tray_icon.setToolTip("Статус вашего приложения")
    menu = QMenu()
    exit_action = QAction("Выход", triggered=exit_action)
    menu.addAction(exit_action)
    tray_icon.setContextMenu(menu)
    tray_icon.show()

    timer = QTimer()
    timer.timeout.connect(check_auth_and_notify)
    timer.start(10000)  # Проверка авторизации каждые 3 минуты

    sys.exit(app.exec())