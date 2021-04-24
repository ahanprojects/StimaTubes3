import sqlite3
import datetime as dt
DATABASE_NAME = 'TaskTest.db'
# semua task
def seeTaskAll():
    pass

# berdasarkan waktu
def seeTaskByWaktu(date1=None,date2=None,jumlah_minggu=None, jumlah_hari=None, jenis=None):
    
    # berdasarkan periode
    if date1 is not None and date2 is not None:
        start_date = date1
        end_date = date2
    
    # berdasarkan minggu
    elif jumlah_minggu is not None:
        start_date = dt.date.today()
        end_date = start_date + dt.timedelta(days=7*jumlah_minggu)

    # berdasarkan hari
    elif jumlah_hari is not None:
        start_date = dt.date.today()
        end_date = start_date + dt.timedelta(days=jumlah_hari)

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
    


def seeTaskToday(jenis=None):
    pass

