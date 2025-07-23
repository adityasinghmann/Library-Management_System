import sqlite3

conn = sqlite3.connect('library.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    issued BOOLEAN DEFAULT 0
)
''')

conn.commit()
conn.close()
print("Database initialized!")