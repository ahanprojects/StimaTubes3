# NOTE : fungsi udah dicobain semua, sejauh ini bisa semua.

# import dan define
import sqlite3
import datetime
DATABASE_NAME = "default.db"

# fungsi tambahan untuk tes
def seedb(nama):
    # contoh namadb : 'Task.db'
    conn = sqlite3.connect(nama)
    c = conn.cursor()

    # fetchall database
    c.execute("SELECT * FROM Task")
    tasks = c.fetchall()
    conn.commit()

    print("[SEE DATABASE]")
    print("(ID) Tanggal - Kode Matkul - Jenis Task - Topik - Status")
    for i,task in enumerate(tasks):
        print(str(i+1)+". "+"(ID: "+str(task[0])+") - "+str(task[1])+" - "+str(task[2])+" - "+str(task[3])+" - "+str(task[4])+" - "+str(task[5]))
    return tasks

# 1
def addTask(tanggal, kodematkul, jenis, topik):
    # parameter harus sudah valid
    task = [tanggal, kodematkul, jenis, topik, 0]
    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO Task (Tanggal, KodeMatkul, JenisTask, Topik, Status) VALUES (?,?,?,?,?)", task)
    conn.commit()
    print("[TASK BERHASIL DICATAT]")
    print("(ID: "+str(task[0])+") - "+str(task[1])+" - "+str(task[2])+" - "+str(task[3]))


# 2
def seeTaskAll():
    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM Task")
    tasks = c.fetchall()
    conn.commit()
    print("[DAFTAR DEADLINE]")
    print("(ID) Tanggal - Kode Matkul - Jenis Task - Topik")
    for i,task in enumerate(tasks):
        print(str(i+1)+". "+"(ID: "+str(task[0])+") - "+str(task[1])+" - "+str(task[2])+" - "+str(task[3])+" - "+str(task[4]))
    
# berdasarkan waktu
def seeTaskByWaktu(date1=None,date2=None,jumlah_minggu=None, jumlah_hari=None, jenis=None):
    
    if jenis == '':
        jenis = None

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
        c.execute(
        '''
        SELECT * FROM Task WHERE Tanggal BETWEEN ? AND ?
        ''', [start_date,end_date])
    else:
        c.execute(
        '''
        SELECT * FROM Task WHERE JenisTask = ? AND (Tanggal BETWEEN ? AND ?)
        ''', [jenis,start_date,end_date])

    tasks = c.fetchall()
    conn.commit()
    print("[DAFTAR DEADLINE]")
    print("(ID) Tanggal - Kode Matkul - Jenis Task - Topik - Status")
    for i,task in enumerate(tasks):
        print(str(i+1)+". "+"(ID: "+str(task[0])+") - "+str(task[1])+" - "+str(task[2])+" - "+str(task[3])+" - "+str(task[4]))
    print()

# 3
def showDeadline(kodematkul):
    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # cari nama kodematkul pada database
    c.execute("SELECT * FROM Task WHERE KodeMatkul = ? AND (JenisTask = ? OR JenisTask = ?)", [kodematkul,'Tucil','Tubes'])
    tasks = c.fetchall()
    conn.commit()
    # print deadlinenya
    for task in tasks:
        print(task[2]+" - "+task[1])

# 4
def updateTask(ID, newDate):
    # open database
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # cari task ada atau ngga
    c.execute("SELECT * FROM Task WHERE ID = ?", [ID])
    ada = c.fetchall()
    conn.commit()

    if len(ada) == 0: # berarti tidak ada task
        print("Task tidak ditemukan.")
    else:
        # terus update
        c.execute("UPDATE Task SET Tanggal = ? WHERE ID = ?", [newDate, ID])
        conn.commit()
        print("Task ID: "+str(ID)+" berhasil di-update.")

# 5
def markTask(ID):
    # open database
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # cari task ada atau ngga
    c.execute("SELECT * FROM Task WHERE ID = ?", [ID])
    ada = c.fetchall()
    conn.commit()

    if len(ada) == 0: # berarti tidak ada task
        print("Task tidak ditemukan.")
    else:
        # terus update
        c.execute("UPDATE Task SET Status = ? WHERE ID = ?", [1, ID])
        conn.commit()
        print("Berhasil menandai task.")

# 6 : help. command : "apa yang bisa assistant lakukan?"
def help():
    out = '''
[Fitur]
1. Menambahkan task baru
    contoh : 
        "Tubes IF221 String Matching pada 14/04/2021"
2. Melihat daftar task
    contoh : 
        "Apa saja deadline yang ada ?"
        "Apa saja deadline antara 03/04/2021 sampai 15/04/2021 ?"
        "Deadline 3 minggu kedepan apa saja ?"
        "Deadline 1 hari kedepan apa saja ?"
3. Menampilkan deadline suatu task
    contoh : 
        "Deadline tugas IF221 itu kapan ?"
4. Memperbaharui task
    contoh : 
        "Deadline task 2 diundur menjadi 28/04/2021"
5. Menandai task yang sudah dikerjakan
    contoh : 
        "Saya sudah mengerjakan task 3"
6. Menampilkan help
    contoh :
        "Apa yang bisa assistant lakukan ?"

[Daftar Kata Penting]
1. Kuis
2. Ujian
3. Tucil
4. Tubes
5. Praktikum
    '''
    print(out)
# 7 : definisi kata penting

# 8 : pesan error : "Apakah mayones sebuah instrumen?", "Maaf pesan tidak dikenali"

# program utama buat ngetes fitur
def main():

    print("Database awal")
    seedb(DATABASE_NAME)    # lihat db awal

    print("Tambah task.")
    # addTask(datetime.date(2021, 5, 10), 'NewKode', 'Kuis', 'New tugas') # nambahin tugas baru
    
    print("See Task All")
    seeTaskAll() # lihat semua task

    print("See task by date.")
    seeTaskByWaktu(date1=datetime.date(2021,4,1), date2=datetime.date(2021,8,30)) # lihat task dari april sampe agustus
    
    print("See kuis 100 hari.")
    seeTaskByWaktu(jumlah_hari=100, jenis='Kuis') # melihat jadwal kuis 4 minggu dari today
    
    print("Show deadline.")
    showDeadline('IF2211') # nampilin deadline

    print("Update tanggal task 2.")
    updateTask(2,datetime.date(2023,1,1)) # update tanggal

    print("Mark task 3.")
    markTask(3)

    print("Database setelahnya.")
    seedb(DATABASE_NAME)

    help()