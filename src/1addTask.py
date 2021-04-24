import sqlite3

DATABASE_NAME = "Task.db"

def seedb(nama):
    # contoh namadb : 'Task.db'
    conn = sqlite3.connect(nama)
    c = conn.cursor()

    # fetchall database
    c.execute("SELECT * FROM Task")
    conn.commit()
    arrdb = c.fetchall()
    conn.commit()
    for a in arrdb:
        print(a)
    return arrdb

def addTask(tanggal, kodematkul, jenis, topik):
    # parameter harus sudah valid
    tuple = [tanggal, kodematkul, jenis, topik, 0]
    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO Task (Tanggal, KodeMatkul, JenisTask, Topik, Status) VALUES (?,?,?,?,?)", tuple)
    conn.commit()
    print("Task berhasil ditambahkan.")

def main():
    import datetime as dt
    # lihat list task yg ada
    seedb(DATABASE_NAME)

    # fungsi addTask
    # addTask(dt.date(2021, 11, 1), 'IF2211', 'Kuis', 'Regex')
    # addTask(dt.date(2021, 9, 5), 'IF2230', 'Ujian', 'UTS')
    # addTask(dt.date(2021, 4, 30), 'IF2220', 'Tucil', 'Tucil Probstat')
    # addTask(dt.date(2021, 6, 6), 'IF2250', 'Tubes', 'Laporan 3')
    # addTask(dt.date(2021, 5, 12), 'IF2210', 'Praktikum', 'Praktikum OOP 1')
    # addTask(dt.date(2021, 8, 13), 'IF2211', 'Kuis', 'Astar')
    # addTask(dt.date(2021, 9, 29), 'IF2220', 'Ujian', 'UAS')
    # addTask(dt.date(2021, 12, 17), 'IF2230', 'Tucil', 'Milestone 2')
    # addTask(dt.date(2021, 10, 22), 'IF2240', 'Tubes', 'Design Database')
    # addTask(dt.date(2021, 2, 21), 'IF2250', 'Praktikum', 'Fungsional Non Fungsional')
    seedb(DATABASE_NAME)

main()  
