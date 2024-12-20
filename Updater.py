# from Imports import *
from config import *
import requests
import platform
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QProgressDialog, QApplication, QMessageBox
import sys
import os
################# LOCK ##########
import zc.lockfile
#################################

from io import BytesIO
import shutil
import tempfile
import zipfile
import psutil

class Updater:
    def __init__(self, version):
        self.version = version
        self.archive_version = None

    def get_latest_archive_url(self):
        return 'https://fr-space.ru/s21notify-build1002.zip'

    def get_archive_name(self, url):
        return url.split('/')[-1]

    def compare_versions(self, archive_name):
        self.archive_version = archive_name[:-4][-9:]  # обрезаем .zip и берем последние 8 символов
        return self.archive_version != self.version[-9:]

    def update_program(self, url):
        self.dialog = UpdateDialog(url)
        self.dialog.show()
        QTimer.singleShot(6000, self.MesBoxUpdated)
        # QMessageBox.information(None, 'Обновление завершено', 'Программа успешно обновлена!')

    def MesBoxUpdated(self):
        reply2 = QMessageBox.question(None, 'Обновление',
                                      f'Обновление завершено успешно. Запустить програму?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply2 == QMessageBox.Yes:
            self.run_program()

    def run_program(self):
        if platform.system() == "Windows":
            os.startfile('C:\\Program Files (x86)\\s21-notify\\s21-notify.exe')
        elif platform.system() == "Linux":
            os.system('s21-notify')


    def start(self):
        url = self.get_latest_archive_url()
        archive_name = self.get_archive_name(url)
        if self.compare_versions(archive_name):
            # archive_version = archive_name[:-4][-9:]  # обрезаем .zip и берем последние 8 символов
            reply = QMessageBox.question(None, 'Обновление',
                                         f'Вышла новая версия {self.archive_version}. Обновить сейчас?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.update_program(url)
        # else:
        #     QMessageBox.information(None, 'Обновление не требуется', 'Вы используете последнюю версию приложения!')
        #     sys.exit()

class UpdateThread(QThread):
    progress_signal = Signal(int, str)

    def __init__(self, url):
        super().__init__()
        self.url = url

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
                    # Use Linux-specific command to stop the program
                    os.system('pkill s21-notify')
            elif step == 'Копирование файла':
                if platform.system() == "Windows":
                    try:
                        exe_file = os.path.join(temp_dir, 's21-notify.exe')
                        shutil.copy2(exe_file, 'C:\\Program Files (x86)\\s21-notify\\s21-notify.exe')
                    except Exception as e:
                        if platform.system() == "Windows":
                            for proc in psutil.process_iter():
                                try:
                                    if proc.name() == 's21-notify.exe':
                                        proc.terminate()
                                except Exception as e:
                                    print(e)
                                    proc.terminate()
                        elif platform.system() == "Linux":
                            # Use Linux-specific command to stop the program
                            os.system('pkill s21-notify')
                elif platform.system() == "Linux":
                    # Use Linux-specific command to copy the EXE file
                    exe_file = os.path.join(temp_dir, 's21-notify')
                    shutil.copy2(exe_file, '/usr/local/bin/s21-notify')
            elif step == 'Очистка':
                shutil.rmtree(temp_dir)

class UpdateDialog(QProgressDialog):
    def __init__(self, url):
        super().__init__()
        self.setModal(True)
        self.setRange(0, 5)
        self.setWindowTitle('Обновление')
        self.setLabelText('Обновление...')
        self.thread = UpdateThread(url)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.start()

    def update_progress(self, value, text):
        self.setLabelText(text)
        self.setValue(value)

# def main():
#     # Создание временного файла для блокировки
#     lockfile_path = os.path.join(tempfile.gettempdir(), 's21-updater.lock')
#
#     try:
#         # Создание блокировки
#         lock = zc.lockfile.LockFile(lockfile_path)
#
#         # Основной цикл программы
#         app = QApplication(sys.argv)
#         app_icon = QIcon('data/icon.ico')
#         app.setWindowIcon(app_icon)
#
#         updater = Updater(version)
#
#         updater.start()
#         timer = QTimer()
#         timer.timeout.connect(lambda: updater.start())
#         # timer4.start(6 * 60 * 6000) # 6 hours
#         timer.start(3 * 60000)  # 3 min
#
#     except zc.lockfile.LockError:
#         print("Программа уже запущена!")
#     except KeyboardInterrupt:
#         print("Выход из программы.")
#     finally:
#         # Освобождение блокировки
#         if 'lock' in locals():
#             lock.close()
#             # Удаление файла блокировки, если он существует
#             if os.path.exists(lockfile_path):
#                 os.remove(lockfile_path)

if __name__ == '__main__':
    # main()
    app = QApplication(sys.argv)
    app_icon = QIcon('data/icon.ico')
    app.setWindowIcon(app_icon)

    updater = Updater(version)

    updater.start()
    timer = QTimer()
    timer.timeout.connect(lambda: updater.start())
    # timer4.start(6 * 60 * 6000) # 6 hours
    timer.start(3 * 60000)  # 3 min

    sys.exit(app.exec())