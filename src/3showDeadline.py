#  Hanya berlaku untuk task yang bersifat Tugas atau memiliki tenggat waktu
# Misalnya: “Deadline tugas IF2211 itu kapan?” kata penting : ['Tucil','Tubes']
import sqlite3
DATABASE_NAME = "TaskTest.db"

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

def main():
    seedb(DATABASE_NAME)
    print("Deadline")
    print("Deadline")
    showDeadline('IF2221')    

main()