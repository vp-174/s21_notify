import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        """Создает подключение к базе данных SQLite."""
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    def create_database(self):
        """Создает таблицы в базе данных."""
        conn = self.connect()
        if conn is None:
            return  # Если подключение не удалось, выходим из метода
        c = conn.cursor()
        # Создание таблиц
        try:
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
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
        finally:
            conn.close()

# Пример использования
if __name__ == "__main__":
    db_manager = DatabaseManager("my_database.db")  # Укажите имя вашей базы данных
    db_manager.create_database()
    print("База данных создана успешно.")