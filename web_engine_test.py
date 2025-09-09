import sys
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtWidgets import (QMainWindow, QApplication,
                               QMessageBox, QDialog, QVBoxLayout,
                               QPushButton, QLabel)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import (QWebEnginePage, QWebEngineProfile,
                                     QWebEngineSettings, QWebEnginePermission)


class GeolocationPermissionDialog(QDialog):
    def __init__(self, site, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Доступ к геолокации")
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout()
        message = QLabel(f"Сайт {site} хочет получить доступ к вашей геопозиции.")
        layout.addWidget(message)

        btn_box = QHBoxLayout()
        self.btn_allow = QPushButton("Разрешить")
        self.btn_deny = QPushButton("Запретить")
        self.btn_remember = QPushButton("Запомнить выбор")

        btn_box.addWidget(self.btn_allow)
        btn_box.addWidget(self.btn_deny)
        btn_box.addWidget(self.btn_remember)

        layout.addLayout(btn_box)
        self.setLayout(layout)


class WebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.permission_granted = False

    def acceptNavigationRequest(self, url, type_, isMainFrame):
        # Разрешаем навигацию по HTTPS для корректной работы геолокации
        if url.scheme() == 'https':
            return True
        return super().acceptNavigationRequest(url, type_, isMainFrame)

    def permissionRequested(self, request):
        if request.permission() == QWebEnginePermission.Geolocation:
            url = request.origin().toString()

            dialog = GeolocationPermissionDialog(url)
            dialog.btn_allow.clicked.connect(lambda: self.handle_permission(request, True))
            dialog.btn_deny.clicked.connect(lambda: self.handle_permission(request, False))
            dialog.btn_remember.clicked.connect(lambda: self.remember_choice(request, True))

            dialog.exec()
        else:
            request.deny()

    def handle_permission(self, request, granted):
        if granted:
            request.grant()
            self.permission_granted = True
        else:
            request.deny()

    def remember_choice(self, request, granted):
        profile = QWebEngineProfile.defaultProfile()
        profile.setPermission(request.origin(), QWebEnginePermission.Geolocation,
                              QWebEnginePermission.PermissionGrantedByUser if granted
                              else QWebEnginePermission.PermissionDeniedByUser)
        self.handle_permission(request, granted)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Настройка профиля WebEngine
        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)
        profile.setHttpCacheType(QWebEngineProfile.MemoryHttpCache)

        # 2. Создаем и настраиваем WebEngineView
        self.browser = QWebEngineView()
        self.browser.setPage(WebEnginePage(profile, self.browser))

        # 3. Включаем все необходимые настройки
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.AllowGeolocationOnInsecureOrigins, True)

        # 4. Загружаем тестовую страницу для проверки геолокации
        test_url = "https://test.fr-space.ru"  # Тестовая страница геолокации
        self.browser.setUrl(QUrl(test_url))

        # 5. Настройка главного окна
        self.setCentralWidget(self.browser)
        self.setWindowTitle("Тест геолокации")
        self.resize(800, 600)

        # 6. Проверка через 5 секунд
        QTimer.singleShot(5000, self.check_geolocation_status)

    def check_geolocation_status(self):
        # Проверяем, была ли предоставлена геолокация
        page = self.browser.page()
        if hasattr(page, 'permission_granted') and page.permission_granted:
            print("Доступ к геолокации предоставлен")
        else:
            print("Доступ к геолокации не предоставлен")
            QMessageBox.warning(self, "Ошибка",
                                "Геолокация не работает. Проверьте:\n"
                                "1. Разрешения браузера\n"
                                "2. Системные настройки геолокации\n"
                                "3. Подключение к интернету")

        # Navbar
        # navbar = QToolBar()
        # self.addToolBar(navbar)
        #
        # back_btn = QAction('Назад', self)
        # back_btn.triggered.connect(self.browser.back)
        # navbar.addAction(back_btn)
        #
        # forward_btn = QAction('Вперёд', self)
        # forward_btn.triggered.connect(self.browser.forward)
        # navbar.addAction(forward_btn)
        #
        # reload_btn = QAction('Перезагрузить', self)
        # reload_btn.triggered.connect(self.browser.reload)
        # navbar.addAction(reload_btn)
        #
        # home_btn = QAction('Главная', self)
        # home_btn.triggered.connect(self.navigate_home)
        # navbar.addAction(home_btn)
        #
        # self.url_bar = QLineEdit()
        # self.url_bar.returnPressed.connect(self.navigate_to_url)
        # navbar.addWidget(self.url_bar)

        # self.browser.urlChanged.connect(self.update_url)

    # def navigate_home(self):
    #     self.browser.setUrl(QUrl('https://test.fr-space.ru'))
    #
    # def navigate_to_url(self):
    #     url = self.url_bar.text()
    #     if not url.startswith('https'):
    #         url = 'https://' + url
    #     self.browser.setUrl(QUrl(url))
    #
    # def update_url(self, q):
    #     self.url_bar.setText(q.toString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
