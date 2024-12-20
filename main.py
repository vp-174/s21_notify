# build/1001-test

from Imports import *
from Audio import *

################# LOCK ##########
import zc.lockfile
import tempfile
#################################

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
        # self.updater = Updater(version)

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

                # filename1 = 'data/01.wav'
                # self.pl.play_wave(filename1)

                time.sleep(5)
                self.event.timeWork()
                timer2 = QTimer()
                timer2.timeout.connect(lambda: self.event.timeWork())
                timer2.start(get_event_period * 60000)

                time.sleep(5)
                self.event.eventNotify()
                timer3 = QTimer()
                timer3.timeout.connect(lambda: self.event.eventNotify())
                timer3.start(1 * 60000) # 1 min

                # time.sleep(5)
                # timer4 = QTimer()
                # timer4.timeout.connect(lambda: self.updater.start())
                # # timer4.start(6 * 60 * 6000) # 6 hours
                # timer4.start(3 * 60000)  # 3 min

            else:
                self.tr.icon.showMessage("Уведомление", "Ошибка авторизации", QSystemTrayIcon.Information, 5000)

        sys.exit(self.app.exec())

    def show_login_window(self):
        '''Вывод окна авторизации'''
        login_dialog = QDialog()
        login_dialog.setFixedSize(240, 190)
        login_dialog.setWindowFlags(Qt.FramelessWindowHint)
        login_dialog.setAttribute(Qt.WA_TranslucentBackground)

        # Создаем виджет для диалога
        dialog_widget = QWidget()


        layout = QVBoxLayout(dialog_widget)

        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Авторизация")
        exit_button = QPushButton("Выйти")

        login_style = '''
            QWidget {
                border-radius: 18px; 
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(200, 205, 255, 255), stop:0.52514 rgba(183, 241, 203, 255));
            }
        
            QLineEdit {
                height: 40px;
                font-size: 14px;
                padding: 0 5 2 5;
                border: 1px solid rgba(200, 205, 255, 255);
                border-radius: 10px;
                background-color: white;
            }

            QPushButton {
                height: 20px;
                padding: 8px;
                background-color: #4CAF50;
                border-radius: 10px;
            }

            QPushButton:hover {
                background-color: #6CBFD4;
            }

            QLabel {
                font-size: 14px;
                color: #000000;
            }
        '''
        dialog_widget.setStyleSheet(login_style)
        username_input.setStyleSheet(login_style)
        password_input.setStyleSheet(login_style)
        login_button.setStyleSheet(login_style)
        exit_button.setStyleSheet(login_style)

        username_input.setPlaceholderText("Логин (edu.21-school.ru)")
        password_input.setPlaceholderText("Пароль")

        def authenticate():
            username = username_input.text()
            password = password_input.text()
            access_token = self.auth.get_access_token(username, password)
            if access_token:
                self.database.save_credentials_to_db(username, password)
                login_dialog.close()

        login_button.clicked.connect(authenticate)
        exit_button.clicked.connect(lambda: sys.exit())

        # l = QLabel("Логин:")
        # p = QLabel("Пароль:")

        # layout.addWidget(l)
        layout.addWidget(username_input)
        # layout.addWidget(p)
        layout.addWidget(password_input)
        layout.addWidget(login_button)
        layout.addWidget(exit_button)

        # l.setStyleSheet(login_style)
        # p.setStyleSheet(login_style)

        # Устанавливаем виджет как центральный виджет диалога
        login_dialog.setLayout(QVBoxLayout())
        login_dialog.layout().addWidget(dialog_widget)

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
        self.message2 = "Дорогой пир!\nЯ буду безумно рад\nтвоей благодарности\nна кофе с печеньками...\n\nкарта (Сбербанк)\n2202 2032 1022 6652"
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
        self.dialog = Calendar()
        self.dialog.setFixedSize(480, 480)
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
        # print("show calendar")

def main():
    # Создание временного файла для блокировки
    lockfile_path = os.path.join(tempfile.gettempdir(), 's21-notify.lock')

    try:
        # Создание блокировки
        lock = zc.lockfile.LockFile(lockfile_path)

        # print("Программа запущена. Нажмите Ctrl+C для выхода.")

        # Основной цикл программы
        app = S21_Notify_App()
        app.run()

    except zc.lockfile.LockError:
        print("Программа уже запущена!")
    except KeyboardInterrupt:
        print("Выход из программы.")
    finally:
        # Освобождение блокировки
        if 'lock' in locals():
            lock.close()
            # Удаление файла блокировки, если он существует
            if os.path.exists(lockfile_path):
                os.remove(lockfile_path)

if __name__ == "__main__":
    main()
