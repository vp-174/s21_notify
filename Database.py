from Imports import *

class Database:
    def __init__(self, db_name=base_sql, encr=Encryption()):
        self.db_name = db_name
        self.encr = encr
        self.gmt = 5 # корректировка времени
        self.create_database()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_database(self):
        conn = self.connect()
        c = conn.cursor()

        # Создание таблицы credentials
        c.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY,
                login TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
       ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                location TEXT,
                start_time TEXT,
                end_time TEXT,
                viewed INTEGER DEFAULT 0,
                event_id INTEGER
            )
       ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                val INTEGER DEFAULT 0
            )        
        ''')

        # Вставка значений в таблицу settings
        c.execute('INSERT OR IGNORE INTO settings (name, val) VALUES (?, ?)', ('sound', 1))
        c.execute('INSERT OR IGNORE INTO settings (name, val) VALUES (?, ?)', ('push', 1))

        conn.commit()
        conn.close()

    def save_credentials_to_db(self, username, password):
        '''Сохранение шифрованных учетных данных в БД'''
        conn = self.connect()
        c = conn.cursor()

        # Шифрование пароля
        encrypted_password = self.encr.encrypt(password)

        # Вставка учетных данных в таблицу user
        c.execute('''
            INSERT INTO credentials (login, password) VALUES (?, ?)
        ''', (username, encrypted_password))

        conn.commit()
        conn.close()

    def read_credentials_from_db(self):
        '''Чтение и расшифровка учетных данных из БД'''
        conn = self.connect()
        c = conn.cursor()

        c.execute('SELECT login, password FROM credentials')
        credentials = c.fetchall()

        if credentials:
            username, encrypted_password = credentials[0]  # Берем только первую запись
            password = self.encr.decrypt(encrypted_password)
            conn.close()
            return username, password
        else:
            return None, None

    def save_event_to_db(self, event):
        '''Сохранение события в БД'''
        conn = self.connect()
        c = conn.cursor()
        c.execute('''
            INSERT INTO events (name, description, location, start_time, end_time, event_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (event['name'], event['description'], event['location'], event['startDateTime'], event['endDateTime'],
              event['id']))
        conn.commit()
        conn.close()

    def mark_event_as_ok(self, event_id):
        '''Пометка события просмотренным'''
        # print(f"{event_id} :: 1")
        conn = self.connect()
        c = conn.cursor()
        c.execute('''
            UPDATE events
            SET viewed = 1
            WHERE event_id = ?
        ''', (event_id,))
        conn.commit()
        conn.close()

    def mark_event_as_no(self, event_id):
        '''Пометка события просмотренным'''
        # print(f"{event_id} :: 1")
        conn = self.connect()
        c = conn.cursor()
        c.execute('''
            UPDATE events
            SET viewed = 2
            WHERE event_id = ?
        ''', (event_id,))
        conn.commit()
        conn.close()

    def event_exists(self, event_id) -> bool:
        '''Проверка существования события в БД'''
        conn = self.connect()
        c = conn.cursor()
        c.execute('''
            SELECT COUNT(*) FROM events
            WHERE event_id = ?
        ''', (event_id,))
        exists = c.fetchone()[0] > 0
        conn.close()
        return exists

    def get_event_from_date(self, date):
        '''Получение событий из БД по дате'''
        conn = self.connect()
        c = conn.cursor()

        # Преобразуем дату в нужный формат
        date_str = date.strftime('%Y-%m-%d')

        # Запрос событий по дате
        c.execute('''
            SELECT name, description, start_time, end_time, location
            FROM events
            WHERE DATE(start_time) = ? AND viewed = 1
        ''', (date_str,))

        events = c.fetchall()
        conn.close()

        # Формируем словарь с событиями
        event_list = []
        for idx, (name, description, start_time, end_time, location) in enumerate(events, start=1):
            # Форматируем время
            start_time_formatted = self.format_time(start_time)
            end_time_formatted = self.format_time(end_time)
            time_range = f"{start_time_formatted}-{end_time_formatted}"

            event_detail = f"<b>{idx}.</b> {name}, {time_range} ({location})"
            event_list.append(event_detail)

        # Возвращаем события в формате, который вы указали
        if event_list:
            return {date: event_list}
        else:
            return {date: []}  # Если событий нет, возвращаем пустой список

    def get_events_from_today(self):
        '''Получение событий из БД начиная с сегодняшней даты'''
        conn = self.connect()
        c = conn.cursor()

        # Получаем сегодняшнюю дату в формате ISO 8601
        # Получаем сегодняшнюю дату с текущим временем, но с нулями для секунд и микросекунд
        now = datetime.now() - timedelta(hours=self.gmt)
        today_iso = now.replace(second=0, microsecond=0).isoformat() + 'Z'  # Приводим к формату ISO 8601 с указанием часового пояса
        print(today_iso)

        # Запрос всех уникальных дат событий начиная с сегодняшней даты
        c.execute('''
            SELECT DISTINCT DATE(start_time) FROM events
            WHERE start_time >= ? AND viewed = 1
        ''', (today_iso,))
        unique_dates = c.fetchall()

        # Формируем словарь с событиями
        events_dict = {}

        for date_tuple in unique_dates:
            event_date = date_tuple[0]  # Извлекаем дату из кортежа
            date_obj = datetime.strptime(event_date, '%Y-%m-%d')  # Преобразуем строку в datetime

            # Получаем события для этой даты
            events = self.get_event_from_date(date_obj)
            # Объединяем события в общий словарь
            events_dict.update(events)

        conn.close()
        return events_dict

    def get_start_event_time(self, date) -> str:
        '''Получение всех start_time событий для заданной даты с viewed = 1'''
        conn = self.connect()
        c = conn.cursor()

        # Преобразуем дату в строку в формате 'YYYY-MM-DD'
        date_str = date.strftime('%Y-%m-%d')

        # Запрос всех start_time событий для заданной даты
        c.execute('''
            SELECT start_time FROM events
            WHERE DATE(start_time) = ? AND viewed = 1
        ''', (date_str,))

        start_times = c.fetchall()  # Получаем все start_time событий

        # Формируем список с start_time
        start_time_list = [int(self.format_time(time_tuple[0]).replace(':','')) for time_tuple in start_times]

        conn.close()
        return start_time_list

    # def get_all_event_dates(self):
    #     '''Получение всех уникальных дат событий из БД'''
    #     conn = self.connect()
    #     c = conn.cursor()
    #     c.execute('''
    #         SELECT DISTINCT DATE(start_time) FROM events WHERE viewed = 1
    #     ''')
    #     dates = c.fetchall()
    #     conn.close()
    #
    #     # Преобразуем список к типу datetime
    #     return [datetime.strptime(date[0], '%Y-%m-%d') for date in dates]

    def get_all_event_dates(self):
        '''Получение всех уникальных дат событий из БД, где start_time больше текущего времени'''
        conn = self.connect()
        c = conn.cursor()

        # Получаем текущее время
        now = datetime.now()

        # Запрос всех уникальных дат событий, где start_time больше текущего времени и viewed = 1
        c.execute('''
            SELECT DISTINCT DATE(start_time) FROM events 
            WHERE start_time > ? AND viewed = 1
        ''', (now,))

        dates = c.fetchall()
        conn.close()

        # Преобразуем список к типу datetime
        return [datetime.strptime(date[0], '%Y-%m-%d') for date in dates]

    def get_status(self,event_id):
        '''Статус события (просомтренно или нет)'''
        conn = self.connect()
        c = conn.cursor()
        c.execute('''
            SELECT viewed FROM events
            WHERE event_id = ?
        ''', (event_id,))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]  # Возвращаем значение viewed
        return None  # Если событие не найдено

    def format_time(self, time_str):
        '''Форматирование времени из формата ISO в нужный формат с корректировкой на +5 часов'''
        # Преобразуем строку времени в объект datetime
        dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        # Добавляем 5 часов
        dt += timedelta(hours=self.gmt)
        return dt.strftime('%H:%M')