from Imports import *

class Database:
    def __init__(self, db_name=base_sql, encr=Encryption()):
        self.db_name = db_name
        self.encr = encr
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

    def mark_event_as_viewed(self, event_id):
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

    def event_exists(self, event_id):
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

    def get_viewed_status(self,event_id):
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