from Imports import *
from Audio import *

class EventSignals(QObject):
    show_notification = Signal(str, str, int)

class Event(Tray):
    def __init__(self, tr):
        super().__init__(tr.icon)
        self.signals = EventSignals()
        self.tr = tr
        self.mute = 0
        self.database = Database()
        self.auth = Auth()
        self.pl = Audio()
        self.signals.show_notification.connect(self._show_event_notify)

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
        url = f'https://edu-api.21-school.ru/services/21-school/api/v1/events?from={from_str}&to={to_str}&limit=50&offset=0'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print(f"get_event - code 200")
            events = response.json().get("events")

            if events:
                # print(f"get_event - events OK")
                for event in events:
                    # Проверяем, существует ли событие в базе данных
                    if not self.database.event_exists(event['id']):  # уникальный идентификатор 'id'
                        # Сохраните событие в базу данных
                        self.database.save_event_to_db(event)

                        # Показать событие
                        self.format_event(event)

                        time.sleep(5)

                    elif self.database.event_exists(event['id']) and self.database.get_status(event['id']) == 0:
                        #print(f"Событие с ID {event['id']} уже существует, но не просмотрено")

                        # Показать событие
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

        date_start = event['startDateTime']
        date_time_obj1 = datetime.strptime(date_start, '%Y-%m-%dT%H:%M:%SZ')
        date_time_obj1 += timedelta(hours=5)
        date_start = date_time_obj1.strftime('%d/%m/%Y %H:%M')
        date_end = event['endDateTime']
        date_time_obj2 = datetime.strptime(date_end, '%Y-%m-%dT%H:%M:%SZ')
        date_time_obj2 += timedelta(hours=5)
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
        '''Вывод окна события (теперь вызывается через сигнал)'''
        try:
            if self.is_win_pl():
                self.pl.play_wave('data/02.wav')
            if self.is_gnu():
                self.pl.play_wave_gnu('data/02.wav')
        except Exception as e:
            pass

        # GUI операции должны выполняться в главном потоке
        QTimer.singleShot(0, lambda: self._show_dialog(message, message2, event_id))

    def _show_event_notify(self, message, message2, event_id):
        '''Вывод окна события (вызывается через сигнал в главном потоке)'''
        # Воспроизведение звука теперь не блокирует GUI
        try:
            if self.is_win_pl():
                self.pl.play_wave('data/02.wav')
            if self.is_gnu():
                self.pl.play_wave_gnu('data/02.wav')
        except Exception as e:
            print(f"Ошибка воспроизведения звука: {e}")

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

    def _show_dialog(self, message, message2, event_id):
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
        '''Показ окна события по времени (+ режим тишины)'''
        now = datetime.now()
        now += timedelta(hours=0)
        nowHour = '{:02d}'.format(now.hour)  # Форматируем часы с ведущими нулями
        nowMin = '{:02d}'.format(now.minute)  # Форматируем минуты с ведущими нулями
        timeCheck = int(str(nowHour) + str(nowMin))  # Объединяем часы и минуты в одно число
        # print(f"mute: {mute}")
        #print(f"timeCheck: {timeCheck}")
        if (timeCheck >= 900 and timeCheck <= 2300) or self.mute == -1:
            self.mute = 0
            username, password = self.database.read_credentials_from_db()
            access_token = self.auth.get_access_token(username, password)
            self.get_event(access_token)
        else:
            self.mute += 1
            # print(mute)
        if self.mute == 1:
            self.tr.icon.showMessage("Включен режим тишины", "Уведомления о новых событиях\n отключены до 9:00 утра", QSystemTrayIcon.Information, 10000)
        elif self.mute > 1:
            #print(f"[ MUTE MODE ]")
            if timeCheck >= 859 and timeCheck <= 1100:
                self.mute = -1

    def eventNotify(self):
        '''Показ окна события по времени (+ режим тишины)'''
        notify_time = 1  # За сколько минут до события показывать уведомление
        now = datetime.now()
        now += timedelta(hours=0)
        nowHour = '{:02d}'.format(now.hour)
        nowMin = '{:02d}'.format(now.minute)
        timeCheck = int(str(nowHour) + str(nowMin))

        try:
            # Получаем время ближайшего события
            event_time_data = self.database.get_start_event_time(now)

            # Проверяем, что данные получены и список не пустой
            if event_time_data and len(event_time_data) > 0:
                event_time = event_time_data[0]

                # Проверяем условие для показа уведомления
                if (event_time - timeCheck) <= notify_time and (event_time - timeCheck) > -1:
                    # Показываем уведомление в системном трее
                    self.tr.icon.showMessage(
                        "Напоминание",
                        "Ближайшее событие сейчас уже начнётся",
                        QSystemTrayIcon.Information,
                        25000
                    )

                    # Воспроизводим звук в отдельном потоке
                    try:
                        if self.is_win_pl():
                            self.pl.play_wave('data/01.wav')
                        elif self.is_gnu():
                            self.pl.play_wave_gnu('data/01.wav')
                    except Exception as e:
                        print(f"Ошибка воспроизведения звука: {e}")

        except Exception as e:
            print(f"Ошибка в eventNotify: {e}")