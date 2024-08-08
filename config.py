import sqlite3

def DATA_BASE():
    db = sqlite3.connect('data/events.db')
    return db