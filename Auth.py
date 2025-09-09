from Imports import *

class Auth:
    '''Класс получения токена и проверки авторизации'''
    # def __init__(self):
    #     pass
    def get_access_token(self, username, password):
        '''Получение токена'''
        url = 'https://auth.sberclass.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/token'
        payload = {
            "Content-Type": "application/x-www-form-urlencoded",
            "client_id": "s21-open-api",
            "username": username,
            "password": password,
            "grant_type": "password"
        }
        print(username, password)
        try:
            response = requests.post(url, data=payload)
            print(response.text)
            if response.status_code == 200:
                # time.sleep(3)
                # tray_icon.showMessage("Уведомление", "Токен получен", QSystemTrayIcon.Information, 5000)
                # filename1 = 'data/01.wav'
                # winsound.PlaySound(filename1, winsound.SND_FILENAME)
                return response.json().get("access_token")
            else:
                return None
        except requests.exceptions.RequestException as e:
            return None

    def check_auth(self, access_token):
        '''Проверка авторизации'''
        url = 'https://platform.21-school.ru/services/21-school/api/v1/events?from=2024-01-23T00%3A00%3A00Z&to=2024-01-24T00%3A00%3A00Z&type=TEST&limit=50&offset=0'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            return False