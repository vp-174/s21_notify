# build/1001
# username = "geoffrea@student.21-school.ru"
# password = ""

from Imports import *
from Audio import *

# if platform.system() == 'Linux':
#     # Отключение вывода ошибок
#     sys.stderr = open(os.devnull, 'w')

class S21_Notify_App(Tray):
    def __init__(self):
        # self.version = "build/oop/0001"
        self.app = QApplication(sys.argv)
        self.app_icon = QIcon('data/icon.ico')
        self.app.setWindowIcon(self.app_icon)
        self.app.setQuitOnLastWindowClosed(False)

        self.tray_icon = QSystemTrayIcon(QIcon("data/icon.png"), self.app)
        self.tray_icon.setToolTip(f"S21 Notify {version}\nУведомление о новых событиях")

        self.encription = Encryption()
        self.database = Database()
        self.auth = Auth()
        self.tr = Tray(self.tray_icon)
        self.event = Event(self.tr)
        self.pl = Audio()
        # self.auth = Auth()

    def run(self):
        self.tray_menu()

        while not self.database.read_credentials_from_db()[0]:
            self.show_login_window()

        if not self.database.read_credentials_from_db()[0]:
            self.show_login_window()
        else:
            username, password = self.database.read_credentials_from_db()
            access_token = self.auth.get_access_token(username, password)

            if self.auth.check_auth(access_token):
                time.sleep(5)
                self.tr.icon.showMessage("Уведомление", "Успешная авторизация", QSystemTrayIcon.Information, 5000)

                filename1 = 'data/01.wav'
                self.pl.play_wave(filename1)

                time.sleep(10)
                self.event.timeWork()
                timer2 = QTimer()
                timer2.timeout.connect(lambda: self.event.timeWork())
                timer2.start(get_event_period * 60000)
            else:
                self.tr.icon.showMessage("Уведомление", "Ошибка авторизации", QSystemTrayIcon.Information, 5000)

        sys.exit(self.app.exec())

    def show_login_window(self):
        '''Вывод окна авторизации'''
        login_dialog = QDialog()
        login_dialog.setFixedSize(360, 240)
        # login_dialog.setAttribute(Qt.WA_TranslucentBackground)
        login_dialog.setWindowFlags(Qt.FramelessWindowHint)
        layout = QVBoxLayout()
        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Авторизация")
        exit_button = QPushButton("Выйти")
        login_style = '''
            QLineEdit {
                font-size: 22px;
                padding: 0 5 2 5;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                
            }
            
            QPushButton {
                height: 20px;
                padding: 8px;
                background-color: #4CAF50;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #6CBFD4;
            }
            
            QLabel {
                font-size: 14px;
                color: #000000;
                border-radius: 10px;
            }
            
        '''
        username_input.setStyleSheet(login_style)
        password_input.setStyleSheet(login_style)
        login_button.setStyleSheet(login_style)
        exit_button.setStyleSheet(login_style)
        def authenticate():
            username = username_input.text()
            password = password_input.text()
            access_token = self.auth.get_access_token(username, password)
            if access_token:
                self.database.save_credentials_to_db(username, password)
                login_dialog.close()

        login_button.clicked.connect(authenticate)
        exit_button.clicked.connect(lambda: sys.exit())

        l = QLabel("Логин:")
        p = QLabel("Пароль:")


        layout.addWidget(l)
        layout.addWidget(username_input)
        layout.addWidget(p)
        layout.addWidget(password_input)
        layout.addWidget(login_button)
        layout.addWidget(exit_button)

        l.setStyleSheet(login_style)
        p.setStyleSheet(login_style)

        login_dialog.setLayout(layout)

        # Получение размеров экрана
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Получение размеров окна
        dialog_width = login_dialog.width()
        dialog_height = login_dialog.height()

        # Вычисление позиции для центрирования окна
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2

        # Установка позиции окна
        login_dialog.move(x, y)

        login_dialog.exec()

    def exit_action_func(self):
        sys.exit()

    def settings_action_func(self):
        print("Настройки приложения")

    def show_donate(self):
        '''Вывод окна доната'''
        self.url = 'https://rocketchat-student.21-school.ru/direct/66aa06b74e1904d388492898?msg=wetPQemmMd7LZa8ak'
        self.message2 = "Мой милый пир!\nЯ буду безумно рад\nтвоей благодарности\nна кофе с печеньками...\n\nкарта (Сбербанк)\n2202 2032 1022 6652"
        self.dialog = DonateDialog(self.message2, self.url, self.tr)
        self.dialog.setFixedSize(422, 315)
        self.dialog.setWindowFlags(self.dialog.windowFlags() | Qt.WindowStaysOnTopHint)  # Установка флага WindowStaysOnTopHint

        # Получение размеров экрана
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Получение размеров окна
        dialog_width = self.dialog.width()
        dialog_height = self.dialog.height()

        # Вычисление позиции для центрирования окна
        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2

        # Установка позиции окна
        self.dialog.move(x, y)

        self.dialog.exec()

    def show_calendar(self):
        print("show calendar")

if __name__ == "__main__":
    app = S21_Notify_App()
    app.run()