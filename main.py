import sys
import requests
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import winsound
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
        if access_token and check_auth(access_token):
            filename = 'data/01.wav'
            winsound.PlaySound(filename, winsound.SND_FILENAME)
            show_notification("Успешная авторизация")
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
        return True
    else:
        return False

def show_notification(message):
    notification = QMessageBox()
    notification.setWindowTitle("Уведомление")
    notification.setText(message)
    notification.setStandardButtons(QMessageBox.Ok)
    notification.exec()

def exit_action():
    print("Exiting the application")
    app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Запретить завершение приложения при закрытии последнего окна
    app.setQuitOnLastWindowClosed(False)

    # Аутентификация
    username = "geoffrea@student.21-school.ru"
    password = "Afcnth19"
    access_token = get_access_token(username, password)
    print(f"{access_token}")

    tray_icon = QSystemTrayIcon(QIcon("data/icon.png"), app)
    tray_icon.setToolTip("Статус вашего приложения")

    menu = QMenu()
    exit_action = QAction("Выход", triggered=exit_action)
    menu.addAction(exit_action)
    tray_icon.setContextMenu(menu)
    tray_icon.show()

    timer = QTimer()
    timer.timeout.connect(check_auth_and_notify)
    timer.start(10000)  # Проверка авторизации каждые 10 секунд

    sys.exit(app.exec())