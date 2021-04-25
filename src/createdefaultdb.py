# Jadi kalo py ini di run, bakal ngebuat database baru
# namanya 'dbfix.db' yang udah ada isinya. Jadi gampang
# kalo mau reset databasenya. cukup run sekali doang trs
# jangan dirun lagi nanti malah nambah 10 task baru yg sama

import sqlite3
import datetime
namadb = 'default.db'

def createdb():
    # create a database or connect to one
    conn = sqlite3.connect(namadb)

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
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(c.fetchall())
    print(namadb+" berhasil dibuat.")

def seedb():
    # contoh namadb : 'Task.db'
    conn = sqlite3.connect(namadb)
    c = conn.cursor()

    # fetchall database
    c.execute("SELECT * FROM Task")
    conn.commit()
    tasks = c.fetchall()
    conn.commit()
    print("[DAFTAR TASK]")
    print("(ID) Tanggal - Kode Matkul - Jenis Task - Topik - Status")
    for i,task in enumerate(tasks):
        print(str(i+1)+". "+"(ID: "+str(task[0])+") - "+str(task[1])+" - "+str(task[2])+" - "+str(task[3])+" - "+str(task[4]))
    return tasks

def addTask(tanggal, kodematkul, jenis, topik):
    # parameter harus sudah valid
    task = [tanggal, kodematkul, jenis, topik, 0]
    # open db
    conn = sqlite3.connect(namadb)
    c = conn.cursor()
    c.execute("INSERT INTO Task (Tanggal, KodeMatkul, JenisTask, Topik, Status) VALUES (?,?,?,?,?)", task)
    conn.commit()
    print("[TASK BERHASIL DICATAT]")
    print("(ID: "+str(task[0])+") - "+str(task[1])+" - "+str(task[2])+" - "+str(task[3]))
    
# buat nambahin
createdb()
addTask(datetime.date(2021, 11, 1), 'IF2211', 'Kuis', 'Regex')
addTask(datetime.date(2021, 9, 5), 'IF2230', 'Ujian', 'UTS')
addTask(datetime.date(2021, 4, 30), 'IF2220', 'Tucil', 'Tucil Probstat')
addTask(datetime.date(2021, 6, 6), 'IF2250', 'Tubes', 'Laporan 3')
addTask(datetime.date(2021, 5, 12), 'IF2210', 'Praktikum', 'Praktikum OOP 1')
addTask(datetime.date(2021, 8, 13), 'IF2211', 'Kuis', 'Astar')
addTask(datetime.date(2021, 9, 29), 'IF2220', 'Ujian', 'UAS')
addTask(datetime.date(2021, 5, 17), 'IF2230', 'Tucil', 'Milestone 2')
addTask(datetime.date(2021, 5, 22), 'IF2240', 'Tubes', 'Design Database')
addTask(datetime.date(2021, 2, 21), 'IF2250', 'Praktikum', 'Fungsional Non Fungsional')
print('berhasil ditambahkan')
seedb()