# from Imports import *
from config import *
import requests
import platform
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QProgressDialog, QApplication, QMessageBox
import sys
import os
import json
import win32api

################# LOCK ##########
# import zc.lockfile
#################################

from io import BytesIO
import shutil
import tempfile
import zipfile
import psutil

class Updater:
    def __init__(self):
        self.current_version = self.get_current_version()
        self.archive_version = None
        self.update_info = self.load_update_info()

    def get_current_version(self):
        exe_path = 'C:\\Program Files (x86)\\s21-notify\\s21-notify.exe'
        if os.path.exists(exe_path):
            info = win32api.GetFileVersionInfo(exe_path, '\\')
            # print(info)
            version = info['FileVersionLS']
            # print(version)
            return f"1.0.0.{version}"
        return None
    def load_update_info(self):
        try:
            response = requests.get('https://fr-space.ru/update_info.json')
            response.raise_for_status()  # Проверка на ошибки HTTP
            return response.json()
        except requests.RequestException as e:
            QMessageBox.critical(None, 'Ошибка', f'Не удалось загрузить информацию об обновлении: {e}')
            return None

    def get_latest_archive_url(self):
        return self.update_info['winUrl'] if self.update_info else None

    def get_latest_version(self):
        return self.update_info['version'] if self.update_info else None

    def compare_versions(self):
        self.archive_version = self.get_latest_version()  # Получаем последнюю версию из JSON
        return self.archive_version != self.current_version  # Сравниваем с текущей версией

    def update_program(self, url):
        self.dialog = UpdateDialog(url)
        self.dialog.show()
        self.dialog.thread.finished_signal.connect(self.run_program)  # Подключаем сигнал

    # def MesBoxUpdated(self):
    #     reply2 = QMessageBox.question(None, 'Обновление',
    #                                   f'Обновление завершено успешно. Запустить программу?',
    #                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    #     if reply2 == QMessageBox.Yes:
    #         self.run_program()

    def run_program(self):
        if platform.system() == "Windows":
            os.startfile('C:\\Program Files (x86)\\s21-notify\\s21-notify.exe')
        elif platform.system() == "Linux":
            os.system('s21-notify')

    def start(self):
        self.current_version = self.get_current_version()
        self.update_info = self.load_update_info()
        url = self.get_latest_archive_url()
        if url is None:
            return  # Выход, если информация не была загружена
        if self.compare_versions():
            reply = QMessageBox.question(None, 'Обновление',
                                         f'Вышла новая версия {self.archive_version}. Обновить сейчас?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.update_program(url)

class UpdateThread(QThread):
    progress_signal = Signal(int, str)
    finished_signal = Signal()  # Новый сигнал для уведомления о завершении

    def __init__(self, url):
        super().__init__()  # Передаем None по умолчанию
        self.url = url  # Сохраняем URL как атрибут экземпляра

    def run(self):
        steps = ['Скачивание файла', 'Распаковка файла', 'Остановка программы', 'Копирование файла', 'Очистка']
        for i, step in enumerate(steps):
            self.progress_signal.emit(i + 1, step)
            if step == 'Скачивание файла':
                zip_data = requests.get(self.url).content
            elif step == 'Распаковка файла':
                temp_dir = tempfile.mkdtemp()
                with zipfile.ZipFile(BytesIO(zip_data), 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            elif step == 'Остановка программы':
                if platform.system() == "Windows":
                    for proc in psutil.process_iter():
                        try:
                            if proc.name() == 's21-notify.exe':
                                proc.terminate()
                        except Exception as e:
                            print(e)
                            proc.terminate()
                elif platform.system() == "Linux":
                    os.system('pkill s21-notify')
            elif step == 'Копирование файла':
                if platform.system() == "Windows":
                    try:
                        exe_file = os.path.join(temp_dir, 's21-notify.exe')
                        shutil.copy2(exe_file, 'C:\\Program Files (x86)\\s21-notify\\s21-notify.exe')
                    except Exception as e:
                        print(f'Ошибка при копировании файла: {e}')
                elif platform.system() == "Linux":
                    exe_file = os.path.join(temp_dir, 's21-notify')
                    shutil.copy2(exe_file, '/usr/local/bin/s21-notify')
            elif step == 'Очистка':
                shutil.rmtree(temp_dir)

        self.finished_signal.emit()  # Уведомляем о завершении

class UpdateDialog(QProgressDialog):
    def __init__(self, url):
        super().__init__()
        self.setModal(True)
        self.setRange(0, 5)
        self.setWindowTitle('Обновление')
        self.thread = UpdateThread(url)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.finished_signal.connect(self.close)  # Закрываем диалог при завершении
        self.thread.start()

    def update_progress(self, value, text):
        self.setLabelText(text)
        self.setValue(value)

if __name__ == '__main__':
    # main()
    app = QApplication(sys.argv)
    app_icon = QIcon('data/icon.ico')
    app.setWindowIcon(app_icon)
    updater = Updater()
    updater.start()
    timer = QTimer()
    timer.timeout.connect(lambda: updater.start())
    # timer4.start(6 * 60 * 6000) # 6 hours
    timer.start(30 * 60000)  # 3 min
    # sys.exit(app.exec())
    app.exec()