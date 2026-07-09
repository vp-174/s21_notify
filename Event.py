from Imports import *
from Audio import *
from lang import _
from config import data_path

class EventSignals(QObject):
    show_notification = Signal(str, str, int)

class Event:
    MAX_EVENTS_PER_ROW = 3
    WINDOW_WIDTH = 422
    WINDOW_HEIGHT = 315
    WINDOW_MARGIN = 12

    def __init__(self, tr, database=None):
        self.signals = EventSignals()
        self.tr = tr
        self.mutex = QMutex()
        self.mute = 0
        self.database = database or Database()
        self.auth = Auth()
        self.pl = Audio()
        self.signals.show_notification.connect(self.show_event_notify)
        self.active_windows = []
        self.open_event_ids = set()
        self.last_event_time = None

    def is_gnu(self):
        return platform.system() == "Linux"

    def is_win_pl(self):
        return platform.system() == "Windows"

    def get_event(self, access_token):
        '''Получение входящих событий с сервера и его вывод на экран'''
        now = datetime.now()
        from_date = now - timedelta(hours=5)
        to_date = now + relativedelta(months=3)
        from_str = from_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        to_str = to_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        url = f'https://platform.21-school.ru/services/21-school/api/v1/events?from={from_str}&to={to_str}&limit=50&offset=0'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            events = response.json().get("events")

            if events:
                for event in events:
                    event_id = event['id']
                    if event_id in self.open_event_ids:
                        continue

                    if not self.database.event_exists(event_id):
                        self.database.save_event_to_db(event)
                        self.format_event(event)
                        time.sleep(5)

                    elif self.database.get_status(event_id) == 0:
                        self.format_event(event)
                        time.sleep(5)
            return True
        else:
            return False

    def format_event(self, event):
        '''Формирование и показ события'''
        name = self.string_trim(event['name'])
        if not event['description']:
            desc = ""
        else:
            desc = self.string_trim(event['description'])
        loc = self.string_trim(event['location'])

        gmt = self.database.gmt
        date_start = event['startDateTime']
        date_time_obj1 = datetime.strptime(date_start, '%Y-%m-%dT%H:%M:%SZ')
        date_time_obj1 += timedelta(hours=gmt)
        date_start = date_time_obj1.strftime('%d/%m/%Y %H:%M')
        date_end = event['endDateTime']
        date_time_obj2 = datetime.strptime(date_end, '%Y-%m-%dT%H:%M:%SZ')
        date_time_obj2 += timedelta(hours=gmt)
        date_end = date_time_obj2.strftime('%H:%M')

        # Используем сигнал для показа уведомления
        self.signals.show_notification.emit("".upper(), f"{name}\n\n{loc}\n{date_start} - {date_end}", event['id'])

    def string_trim(self, sentence):
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

    def show_event_notify(self, message, message2, event_id):
        '''Вывод окна события с позиционированием в сетке'''
        try:
            if self.is_win_pl():
                self.pl.play_wave(data_path('02.wav'))
            if self.is_gnu():
                self.pl.play_wave_gnu(data_path('02.wav'))
        except Exception as e:
            print(f"Ошибка воспроизведения звука: {e}")

        url = 'https://edu.21-school.ru'
        dialog = CustomDialog(message, message2, url, event_id)

        # Определяем параметры масштабирования и отступов
        if len(self.active_windows) >= 9:
            margin = self.WINDOW_MARGIN / 2
        else:
            margin = self.WINDOW_MARGIN

        # Устанавливаем размер окна
        dialog.setFixedSize(
            int(self.WINDOW_WIDTH),
            int(self.WINDOW_HEIGHT)
        )

        # Важно: устанавливаем атрибуты окна перед показом
        dialog.setWindowFlags(
            Qt.Window |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )
        dialog.setAttribute(Qt.WA_ShowWithoutActivating)

        self.open_event_ids.add(event_id)

        dialog.finished.connect(lambda: self.remove_window(dialog))
        self.active_windows.append(dialog)

        # Позиционируем все окна
        self.arrange_windows()

        # Показываем окно
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    def remove_window(self, window):
        self.open_event_ids.discard(window.event_id)
        if window in self.active_windows:
            self.active_windows.remove(window)
        self.arrange_windows()

    def arrange_windows(self):
        '''Располагаем окна в сетке с центрированием по горизонтали и вертикали'''
        if not self.active_windows:
            return

        screen = QApplication.primaryScreen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # Определяем количество окон в строке и масштабирование
        if len(self.active_windows) > 12:
            events_per_row = 5  # При большом количестве окон - 4 в строке
            margin = self.WINDOW_MARGIN / 3
        elif len(self.active_windows) > 9:
            events_per_row = 4  # При большом количестве окон - 4 в строке
            margin = self.WINDOW_MARGIN / 2
        else:
            events_per_row = self.MAX_EVENTS_PER_ROW
            margin = self.WINDOW_MARGIN

        # Рассчитываем количество строк
        rows = (len(self.active_windows) - 1) // events_per_row + 1

        # Общая высота всех строк с отступами
        window_height = int(self.WINDOW_HEIGHT)
        total_height = rows * window_height + (rows - 1) * margin

        # Начальная позиция Y для центрирования по вертикали
        start_y = (screen_height - total_height) // 2

        # Для каждой строки рассчитываем позиции
        for row in range(rows):
            # Получаем окна текущей строки
            start_idx = row * events_per_row
            end_idx = start_idx + events_per_row
            row_windows = self.active_windows[start_idx:end_idx]

            # Общая ширина всех окон в строке с отступами
            window_width = int(self.WINDOW_WIDTH)
            total_width = len(row_windows) * window_width + (len(row_windows) - 1) * margin

            # Начальная позиция X для центрирования по горизонтали
            start_x = (screen_width - total_width) // 2

            # Позиция Y (каждая новая строка ниже предыдущей)
            y_pos = start_y + row * (window_height + margin)

            # Устанавливаем позиции для окон в строке
            for i, window in enumerate(row_windows):
                x_pos = start_x + i * (window_width + margin)
                window.move(x_pos, y_pos)

    def show_dialog(self, message, message2, event_id):
        '''Фактическое создание и показ диалога'''
        url = 'https://edu.21-school.ru'
        dialog = CustomDialog(message, message2, url, event_id)
        dialog.setFixedSize(422, 315)
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)

        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        dialog_width = dialog.width()
        dialog_height = dialog.height()

        x = (screen_width - dialog_width) // 2
        y = (screen_height - dialog_height) // 2

        dialog.move(x, y)
        dialog.exec()

    def timeWork(self):
        now = datetime.now()
        nowHour = '{:02d}'.format(now.hour)
        nowMin = '{:02d}'.format(now.minute)
        timeCheck = int(str(nowHour) + str(nowMin))

        mute_start_val = self.database.mute_start * 100
        mute_end_val = self.database.mute_end * 100

        self.mutex.lock()
        try:
            if (timeCheck >= mute_end_val and timeCheck <= mute_start_val) or self.mute == -1:
                self.mute = 0
                self.mutex.unlock()
                username, password = self.database.read_credentials_from_db()
                access_token = self.auth.get_access_token(username, password)
                self.get_event(access_token)
                return

            self.mute += 1

            if self.mute == 1:
                self.tr.icon.showMessage(
                    _('mute_title'),
                    _('mute_msg').format(mute_end=self.database.mute_end),
                    QSystemTrayIcon.Information, 10000
                )
            elif self.mute > 1:
                if timeCheck >= mute_end_val - 41 and timeCheck <= mute_end_val + 200:
                    self.mute = -1
        finally:
            try:
                self.mutex.unlock()
            except RuntimeError:
                pass

    def eventNotify(self):
        notify_time = self.database.notify_time
        now = datetime.now()
        nowHour = '{:02d}'.format(now.hour)
        nowMin = '{:02d}'.format(now.minute)
        timeCheck = int(str(nowHour) + str(nowMin))

        try:
            event_time_data = self.database.get_start_event_time(now)

            # Проверяем, что данные получены и список не пустой
            if event_time_data and len(event_time_data) > 0:
                event_time = event_time_data[0]

                # Проверяем условие для показа уведомления
                if (event_time - timeCheck) <= notify_time and (event_time - timeCheck) > -1:
                    # Показываем уведомление в системном трее
                    self.tr.icon.showMessage(
                        _('reminder'),
                        _('reminder_msg'),
                        QSystemTrayIcon.Information,
                        25000
                    )

                    # Воспроизводим звук в отдельном потоке
                    try:
                        if self.is_win_pl():
                            self.pl.play_wave(data_path('01.wav'))
                        elif self.is_gnu():
                            self.pl.play_wave_gnu(data_path('01.wav'))
                    except Exception as e:
                        print(f"Ошибка воспроизведения звука: {e}")

        except Exception as e:
            print(f"Ошибка в eventNotify: {e}")