# import dan define
import sqlite3
import datetime
DATABASE_NAME = "Task.db"

# fungsi tambahan untuk tes
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

# 1
def addTask(tanggal, kodematkul, jenis, topik):
    # parameter harus sudah valid
    tuple = [tanggal, kodematkul, jenis, topik, 0]
    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO Task (Tanggal, KodeMatkul, JenisTask, Topik, Status) VALUES (?,?,?,?,?)", tuple)
    conn.commit()
    print("Task berhasil ditambahkan.")

# 2
def seeTaskAll():
    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    ret = c.execute("SELECT * FROM Task")
    conn.commit()
    for r in ret:
        print(r)
        
# berdasarkan waktu
def seeTaskByWaktu(date1=None,date2=None,jumlah_minggu=None, jumlah_hari=None, jenis=None):
    
    # berdasarkan periode
    if date1 is not None and date2 is not None:
        start_date = date1
        end_date = date2
    
    # berdasarkan minggu
    elif jumlah_minggu is not None:
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=7*jumlah_minggu)

    # berdasarkan hari
    elif jumlah_hari is not None:
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=jumlah_hari)

    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    if jenis is None:
        ret = c.execute(
        '''
        SELECT * FROM Task WHERE Tanggal BETWEEN ? AND ?
        ''', [start_date,end_date])
    else:
        ret = c.execute(
        '''
        SELECT * FROM Task WHERE JenisTask = ? AND Tanggal BETWEEN ? AND ?
        ''', [jenis,start_date,end_date])

    conn.commit()
    for r in ret:
        print(r)

# 3
# Hanya berlaku untuk task yang bersifat Tugas atau memiliki tenggat waktu
# Misalnya: “Deadline tugas IF2211 itu kapan?” kata penting : ['Tucil','Tubes']
def showDeadline(kodematkul):
    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # cari nama kodematkul pada database
    ret = c.execute("SELECT * FROM Task WHERE KodeMatkul = ? AND JenisTask = ? OR JenisTask = ?", [kodematkul,'Tucil','Tubes'])
    conn.commit()
    # print deadlinenya
    for tupl in ret:
        print(tupl)

# 4
def updateTask(ID, newDate):
    # contoh namadb : 'Task.db'
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # c.execute("UPDATE Task SET Tanggal = {}".format(str(newDate)) + " WHERE ID = {}".format(ID))
    c.execute("UPDATE Task SET Tanggal = ? WHERE ID = ?", [newDate, ID])
    conn.commit()
    print("Task berhasil di Update")

# 5
def markTask(ID):
    # open database
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # cari task ada atau ngga
    ada = c.execute("SELECT * FROM Task WHERE ID = ?", ID)
    conn.commit()

    if len(ada) == 0: # berarti tidak ada task
        print("Task tidak ditemukan.")
    else:
        # terus update
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("UPDATE Task SET Status = ? WHERE ID = ?", [1, ID])
        conn.commit()
        print("Berhasil menandai task.")

# 6 : help

# 7 : definisi kata penting

# 8 : pesan error