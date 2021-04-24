import sqlite3

# create a database or connect to one
conn = sqlite3.connect('TaskFix.db')

# create cursor
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS Task (
    ID INTEGER PRIMARY KEY, 
    Tanggal DATE,
    KodeMatkul TEXT, 
    JenisTask TEXT, 
    Topik TEXT,
    Status BIT
    );""")

# commit changes
conn.commit()

# close connection
conn.close()