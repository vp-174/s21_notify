# build/0001

import sys
import requests
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import winsound

access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ5V29landCTmxROWtQVEpFZnFpVzRrc181Mk1KTWkwUHl2RHNKNlgzdlFZIn0.eyJleHAiOjE3MjA1NTc5ODQsImlhdCI6MTcyMDUyMTk4NCwianRpIjoiOTZlZDU3MmItYWZiMy00YzczLWI3ZTgtMjY1YTM4ZDRhNDFhIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnNiZXJjbGFzcy5ydS9hdXRoL3JlYWxtcy9FZHVQb3dlcktleWNsb2FrIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjIzYzBlN2MxLWY0ZTQtNDNlNC05ZTRjLTFiOGI3OGE3ODZlMCIsInR5cCI6IkJlYXJlciIsImF6cCI6InMyMS1vcGVuLWFwaSIsInNlc3Npb25fc3RhdGUiOiJlYjgwN2EyOC0wMjZhLTQwMTktOGRhMS0wMjgxMmEzYmY4M2QiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vZWR1LjIxLXNjaG9vbC5ydSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1lZHVwb3dlcmtleWNsb2FrIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1c2VyX2lkIjoiMDJiODk3NWQtNGE3OC00ZWE0LWExZDktNjg3Mzk4NWU3MmI4IiwibmFtZSI6Ikdlb2ZmcmV5IEFubmljZSIsImF1dGhfdHlwZV9jb2RlIjoiZGVmYXVsdCIsInByZWZlcnJlZF91c2VybmFtZSI6Imdlb2ZmcmVhQHN0dWRlbnQuMjEtc2Nob29sLnJ1IiwiZ2l2ZW5fbmFtZSI6Ikdlb2ZmcmV5IiwiZmFtaWx5X25hbWUiOiJBbm5pY2UiLCJlbWFpbCI6Imdlb2ZmcmVhQHN0dWRlbnQuMjEtc2Nob29sLnJ1In0.Cg3UvMDLeUGO1pGkJ71GQU2kEmAZt2Rtklm7gPoWYvdB3R-CncJPeAbAwcdH3p7jZ2Zn7iWkJKiKXP8VKMDwIy9wYJkLcdTT4n_X2TyFj3PIRecvsLVLKnpkxYb8qHaQGUHHs4nj_01Vq5Go39S23oZfVk5swewkMd2lQk-5Y7hSf7CL98S4QFy1wln_p3KdrsbG5yd8SkX_DXXkqAzgmiG-4eGjot0_mnluoQJ1Zm9Wl8NoQn6tArutUugQHlprMPOLyC4ahWRdUvLauL3tCArN3uBzh6kZrJABLVC0GgDITsFTLJokyDpGG4-9PMUVbE3CDdTlWpC4ZA4iyeeanA"
# def get_access_token(username, password):
#     url = 'https://auth.sberclass.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/token'
#     payload = {
#         "username": username,
#         "password": password,
#         "grant_type": "password",
#         "client_id": "s21-open-api"
#     }
#     response = requests.post(url, data=payload)
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     else:
#         return None

def check_auth_and_notify():
    try:
        if access_token and check_auth(access_token):
            filename = 'data/01.wav'
            winsound.PlaySound(filename, winsound.SND_FILENAME)
            show_notification("Успешная авторизация")
    except Exception as e:
        print(f"Error: {e}")

def check_auth(access_token):
    url1 = 'https://edu-api.21-school.ru/services/21-school/api/v1/events?from=2024-01-23T00%3A00%3A00Z&to=2024-01-24T00%3A00%3A00Z&type=TEST&limit=50&offset=0'
    url2 = 'https://edu-api.21-school.ru/services/21-school/api/v1/events?from=2024-07-09T00%3A00%3A00Z&to=2024-07-11T00%3A00%3A00Z&limit=50&offset=0'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url2, headers=headers)
    if response.status_code == 200:
        print(response.json().get("events")) # здесь приходит event
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
    # username = "geoffrea@student.21-school.ru"
    # password = "Afcnth19"
    # access_token = get_access_token(username, password)
    # print(f"{access_token}")

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