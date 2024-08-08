import sqlite3
from config import *
def create_database():
   conn = DATA_BASE()
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