import sqlite3

DATABASE_NAME = "TaskTest.db"

def seedb(nama):
    # contoh namadb : 'Task.db'
    conn = sqlite3.connect(nama)
    c = conn.cursor()

    # fetchall database
    c.execute("SELECT * FROM task")
    conn.commit()
    arrdb = c.fetchall()
    conn.commit()
    for i in range(len(arrdb)):
        print(arrdb[i])
    return arrdb

def updateTask(ID, newDate):
    # contoh namadb : 'Task.db'
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # c.execute("UPDATE Task SET Tanggal = {}".format(str(newDate)) + " WHERE ID = {}".format(ID))
    c.execute("UPDATE Task SET Tanggal = ? WHERE ID = ?", [newDate, ID])
    conn.commit()
    print("Task berhasil di Update")

def main():
    import datetime as dt
    # lihat list task yg ada
    seedb(DATABASE_NAME)
    # input task baru
    tgl = dt.date(2023, 3, 4)
    # fungsi addTask
    updateTask(1, tgl)
    # lihat list task yg baru
    seedb(DATABASE_NAME)
main()

