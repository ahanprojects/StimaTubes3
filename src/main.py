import re
import string
from kmp import KMPSearch
# ================================= DB FUNCTIONS =================================
# Fungsi manipulasi database

# NOTE : fungsi udah dicobain semua, sejauh ini bisa semua.

# import dan define
import sqlite3
import datetime
import os
c = os.path.dirname(os.path.realpath(__file__))
par = os.path.split(c)[0]
DATABASE_NAME = "../test/default.db"
print("Database :" + DATABASE_NAME)

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
    task = [tanggal, kodematkul.upper(), jenis.capitalize(), topik.capitalize(), 0]
    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # caritahu apakah task sudah ada
    c.execute("SELECT * FROM Task WHERE Tanggal = ? AND KodeMatkul = ? AND JenisTask = ? AND  Topik = ? AND Status = ?", task)
    ta = c.fetchall()
    conn.commit()
    if len(ta) != 0:
        return "Task sudah pernah dicatat, ID : "+str(ta[0][0])

    c.execute("INSERT INTO Task (Tanggal, KodeMatkul, JenisTask, Topik, Status) VALUES (?,?,?,?,?)", task)
    conn.commit()

    # caritahu id
    c.execute("SELECT * FROM Task WHERE Tanggal = ? AND KodeMatkul = ? AND JenisTask = ? AND  Topik = ? AND Status = ?", task)
    t = c.fetchall()
    print(t)
    conn.commit()
    # print
    tgl = str(datetime.datetime.strptime(t[0][1], "%Y-%m-%d").strftime("%d-%m-%Y"))
    print("[TASK BERHASIL DICATAT]")
    print("(ID: "+str(t[0][0])+") - "+str(tgl)+" - "+str(t[0][2])+" - "+str(t[0][3])+" - "+str(t[0][4]))

    # ret
    ret = ("[TASK BERHASIL DICATAT]<br>")
    ret += ("(ID: "+str(t[0][0])+") - "+str(t[0][1])+" - "+str(t[0][2])+" - "+str(t[0][3])+" - "+str(t[0][4]))
    return ret


# 2
def seeTaskAll():
    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM Task WHERE Status = 0")
    tasks = c.fetchall()
    conn.commit()

    # print
    print("[DAFTAR DEADLINE]")
    print("(ID) Tanggal - Kode Matkul - Jenis Task - Topik")
    for i,task in enumerate(tasks):
        tgl = datetime.datetime.strptime(task[1], "%Y-%m-%d").strftime("%d-%m-%Y")
        print(str(i+1)+". "+"(ID: "+str(task[0])+") - "+str(tgl)+" - "+str(task[2])+" - "+str(task[3])+" - "+str(task[4]))
    
    # ret
    ret = "[DAFTAR DEADLINE]"
    ret += "<br>(ID) Tanggal - Kode Matkul - Jenis Task - Topik"
    for i,task in enumerate(tasks):
        tgl = datetime.datetime.strptime(task[1], "%Y-%m-%d").strftime("%d-%m-%Y")
        ret += '<br>'+(str(i+1)+". "+"(ID: "+str(task[0])+") - "+str(tgl)+" - "+str(task[2])+" - "+str(task[3])+" - "+str(task[4]))
    return ret

# berdasarkan waktu
def seeTaskByWaktu(date1=None,date2=None,jumlah_minggu=None, jumlah_hari=None, jenis=None):
    
    jenis = jenis.capitalize()
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
    if len(tasks) == 0:
        print("Tidak ada.")
        return "Tidak ada."
    
    # print
    print("[DAFTAR DEADLINE]")
    print("(ID) Tanggal - Kode Matkul - Jenis Task - Topik")
    for i,task in enumerate(tasks):
        tgl = datetime.datetime.strptime(task[1], "%Y-%m-%d").strftime("%d-%m-%Y")
        print(str(i+1)+". "+"(ID: "+str(task[0])+") - "+str(tgl)+" - "+str(task[2])+" - "+str(task[3])+" - "+str(task[4]))
    print()

    # ret
    ret = "[DAFTAR DEADLINE]"
    ret += "<br>(ID) Tanggal - Kode Matkul - Jenis Task - Topik"
    for i,task in enumerate(tasks):
        tgl = datetime.datetime.strptime(task[1], "%Y-%m-%d").strftime("%d-%m-%Y")
        ret += '<br>'+(str(i+1)+". "+"(ID: "+str(task[0])+") - "+str(tgl)+" - "+str(task[2])+" - "+str(task[3])+" - "+str(task[4]))
    return ret

# 3
def showDeadline(kodematkul,tipe):
    # tipe = tugas, tucil, tubes
    tipe = tipe.capitalize()
    kodematkul = kodematkul.upper()
    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # cari nama kodematkul pada database
    if tipe == "Tugas":
        c.execute("SELECT * FROM Task WHERE KodeMatkul = ? AND (JenisTask = ? OR JenisTask = ?)", [kodematkul,'Tucil','Tubes'])
        tasks = c.fetchall()
        conn.commit()
    elif tipe == "Tucil" or tipe == "Tubes":
        c.execute("SELECT * FROM Task WHERE KodeMatkul = ? AND JenisTask = ?", [kodematkul,tipe])
        tasks = c.fetchall()
        conn.commit()
    else:
        return "Error. tipe not tugas, tucil, or tubes"

    if len(tasks) == 0:
        print("Tidak ada "+str(tipe)+" "+str(kodematkul))
        return ("Tidak ada "+str(tipe)+" "+str(kodematkul))
    # print deadlinenya
    ret = ''
    for task in tasks:
        ret += '<br>'+(task[3] + " "+task[2]+" : "+str(datetime.datetime.strptime(task[1], "%Y-%m-%d").strftime("%d-%m-%Y")))
    return ret

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
        print("Task ID: "+str(ID)+" tidak ditemukan.")
        return ("Task ID: "+str(ID)+" tidak ditemukan.")
    else:
        # terus update
        c.execute("UPDATE Task SET Tanggal = ? WHERE ID = ?", [newDate, ID])
        conn.commit()
        print("Task ID: "+str(ID)+" berhasil di-update.")
        return ("Task ID: "+str(ID)+" berhasil di-update.")

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
        print("Task ID: "+str(ID)+" tidak ditemukan.")
        return ("Task ID: "+str(ID)+" tidak ditemukan.")
    else:
        # terus update
        c.execute("UPDATE Task SET Status = 1 WHERE ID = ?", [ID])
        conn.commit()
        print("Berhasil menandai Task, ID: "+str(ID))
        return ("Berhasil menandai Task, ID: "+str(ID))

# 6 : help. command : "apa yang bisa assistant lakukan?"
def help():
    out = '''
<pre>
[Fitur]
1. Menambahkan task baru
    contoh : 
        "Tubes IF2221 String Matching pada
         14-04-2021"
2. Melihat daftar task
    contoh : 
        "Apa saja deadline yang ada ?"
        "Apa saja deadline antara 03-04-2021
         sampai 15-04-2021 ?"
        "Deadline 3 minggu kedepan apa saja ?"
        "Deadline 1 hari kedepan apa saja ?"
3. Menampilkan deadline suatu task
    contoh : 
        "Deadline tugas IF221 itu kapan ?"
4. Memperbaharui task
    contoh : 
        "Deadline task 2 diundur menjadi
         28-04-2021"
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

[Catatan]
- Tanggal ditulis dengan format DD-MM-YYYY
- Kode Mata Kuliah terdiri dari 2 huruf dan 4 angka
    contoh : IF2211
</pre>
    '''
    print(out)
    return out
# 7 : definisi kata penting
# 8 : pesan error : "Apakah mayones sebuah instrumen?", "Maaf pesan tidak dikenali"

# ================================= REGEX =================================
# hapus spasi berlebih, ubah jadi lower case
def cleanQuery(query):
    query = query.lower()
    query = re.sub(r'\s{2,}', ' ', query)
    return query

# cari tanggal pada string
def cariTanggal(query):
    tanggal = re.findall('[0-9]{2}-[0-9]{2}-[0-9]{4}', query)
    if tanggal is not None:
        return tanggal
    return []

def cariAngkaSelainTanggal(query):
    arrnum = re.findall(r'[0-9]+[-].+|([0-9._]+)+', query)
    if arrnum == []:
        return [-999]
    if arrnum is not None:
        return arrnum
    return [-999]
    

def cariKodeMatkul(query):
    arrkode = re.findall(r'[A-Za-z]{2}[0-9]{4}', query)
    if arrkode is not None:
        return arrkode
    return []
# ================================= FUNGSI REGEX =================================
def rAddTask(query, run):
    # harus punya empat komponen : tanggal, kode matkul, jenis (kata penting), topik
    # ide : setelah kode pasti topik, ditulis terurut.

    global kataPenting 
    # cari tanggal
    arrtgl = cariTanggal(query)
    if len(arrtgl) != 1:
        # misal gaada tanggal, atau tanggal ada lebih dari 1, berarti bukan addtask
        return

    # cari jenis
    bool_jenis = False
    for kata in kataPenting:
        if KMPSearch(kata,query):
            bool_jenis = True
            jenis = kata
            break
    if not bool_jenis:
        return

    arrkode = cariKodeMatkul(query)
    if len(arrkode) != 1:
        return
    kode = arrkode[0]

    # topik ditulis setelah kode matkul, misal : IF2210 bab 2 sampai 3
    arr_query = query.split()
    for i,kata in enumerate(arr_query):
        if kata == kode:
            idx_kode = i
            break

    if arr_query[len(arr_query)-1] == arrtgl[0]:    # kalau tanggal ditulis diakhir
        if arr_query[len(arr_query)-2].lower() not in ['pada','tanggal']:
            arr_topik = arr_query[idx_kode+1:len(arr_query)-1]
        else: # ada kata pada atau tanggal
            arr_topik = arr_query[idx_kode+1:len(arr_query)-2]
    else:   
        arr_topik = arr_query[idx_kode+1:len(arr_query)]
    topik = ' '.join(arr_topik)
    if topik == '':
        return

    # return
    date = datetime.datetime.strptime(arrtgl[0], '%d-%m-%Y').date()
    global isRun
    isRun = True
    
    if run == False:
        return
    else:
        return addTask(date, kode, jenis, topik)



def rSeeTask(query):
    # periksa bakal make fungsi seeAll, berdasarkan minggu atau hari dll.
    # disini kalau wajib kata 'deadline', command "3 minggu lagi ada kuis apa?" gajalan, jadi ga wajib sementara
    global kataPenting, isRun

    # cari apakah ada jenis
    jenis = ''
    for kata in kataPenting:
        if KMPSearch(kata,query):
            jenis = kata
            break

    # Kasus khusus : kalo gaada 'deadline', wajib : angka, (minggu/hari), jenis
    if not KMPSearch("deadline",query):       
        if jenis == '':
            return
        else:
            arr_jml_wkt = cariAngkaSelainTanggal(query)
            jml_wkt = int(arr_jml_wkt[0])
            if jml_wkt == -999:
                return
            else:
                if KMPSearch('minggu',query):
                    isRun = True
                    return seeTaskByWaktu(jumlah_minggu=jml_wkt, jenis=jenis)
                elif KMPSearch('hari',query):
                    isRun = True
                    return seeTaskByWaktu(jumlah_hari=jml_wkt, jenis=jenis)
                else:
                    return

    # deadline wajib, jenis optional
    # cari tanggal
    arrtgl = cariTanggal(query)

    # Pakai yang periode
    if len(arrtgl) == 2:    
        date1 = datetime.datetime.strptime(arrtgl[0], '%d-%m-%Y').date()
        date2 = datetime.datetime.strptime(arrtgl[1], '%d-%m-%Y').date()
        isRun = True
        return seeTaskByWaktu(date1=date1, date2=date2, jenis=jenis)
    
    arr_jml_wkt = cariAngkaSelainTanggal(query)
    # print("arrjml",arr_jml_wkt)
    jml_wkt = int(arr_jml_wkt[0])
    if not jml_wkt == -999:

        # jika ada kata minggu
        if KMPSearch('minggu',query):
            isRun = True
            return seeTaskByWaktu(jumlah_minggu=jml_wkt, jenis=jenis)

        if KMPSearch('hari',query):
            try:
                isRun = True
                return seeTaskByWaktu(jumlah_hari=jml_wkt, jenis=jenis)
            except:
                pass

    # Pakai yang seeAll atau hari ini
    # asumsi : kalau ada kata sejauh dan sampai, pake seeTaskAll
    if len(arrtgl) == 0:
        isRun = True
        if KMPSearch('hari ini',query) and not KMPSearch('sampai',query) and not KMPSearch('sejauh',query):
            return seeTaskByWaktu(jumlah_hari=0, jenis=jenis)
        
        elif KMPSearch('besok',query) and jml_wkt == -999:
            return seeTaskByWaktu(jumlah_hari=1, jenis=jenis)

        else: # hanya ada kata 'deadline'
            return seeTaskAll()
    return "Kata kunci kurang."

def rShowDeadline(query):
    # hanya untuk tugas (tubes, tucil)
    global isRun

    # cari kata "deadline"
    if not KMPSearch("deadline",query):
        return

    # cari kata tugas, tubes, atau tucil
    if KMPSearch('tugas',query):
        tipe = 'tugas'
    elif KMPSearch('tubes',query):
        tipe = 'tubes'
    elif KMPSearch('tucil',query):
        tipe = 'tucil'
    else:
        return
    
    # cari kode matkul
    arrkode = cariKodeMatkul(query)
    if len(arrkode) != 1:
        return
    kode = arrkode[0]

    isRun = True
    return showDeadline(kode,tipe)

def rUpdateTask(query):
    # cari kata "deadline"
    if not KMPSearch("deadline",query):
        return

    arrtgl = cariTanggal(query)
    if len(arrtgl) != 1:
        # misal gaada tanggal, atau tanggal ada lebih dari 1, berarti bukan addtask
        return
    # diundur, diubah, diganti ?
    # menjadi, ke ?

    # cari kata "task"
    if not KMPSearch("task",query):
        return

    # cari id task
    id_task = cariAngkaSelainTanggal(query)

    date = datetime.datetime.strptime(arrtgl[0], '%d-%m-%Y').date()
    global isRun
    isRun = True
    return updateTask(int(id_task[0]),date)

def rMarkTask(query):
    # Saya sudah selesai mengerjakan task ID
    # cari kata "sudah" dll
    kataSinyal = ['udah','kerja','mengerja','selesai']
    adaSinyal = False
    for kata in kataSinyal:
        if KMPSearch(kata,query):
            adaSinyal = True
    if not adaSinyal:
        return

    # cari kata "task"
    if not KMPSearch("task",query):
        return

    # cari id task
    id_task = cariAngkaSelainTanggal(query)

    global isRun
    isRun = True
    return markTask(int(id_task[0]))

def rHelp(query):
    global kataPenting
    kataSinyal = ['help','apa saja','apain','lakukan']
    adaSinyal = False
    for kata in kataSinyal:
        if KMPSearch(kata,query):
            adaSinyal = True
    if not adaSinyal:
        return

    if KMPSearch("deadline",query):
        return
    # gaboleh ada kataPenting, tanggal, kode matkul
    for kata in kataPenting:
        if KMPSearch(kata,query):
            return

    arrkode = cariKodeMatkul(query)
    if arrkode != []:
        return
    arrtgl = cariTanggal(query)
    if arrtgl != []:
        return
        
    global isRun
    isRun = True
    return help()

# ================================= MAIN PROGRAM =================================
kataPenting = ["kuis", "ujian", "tucil", "tubes", "praktikum"]
isRun = False   # ada fungsi yg ke run atau ngga
'''
Kata wajib tiap soal :
1. addTask : tanggal, kode, jenis, topik
2. seeTask : deadline.
    optional : jenis
    a. byDate : 2 date
    b. byMinggu : minggu
    c. byHari : hari
    d. byToday : hari ini, not sampai, not sejauh
    e. seeAll : -
3. showDeadline : deadline, pilih satu : tugas, tubes, tucil
4. updateTask : deadline, 1 date, task
5. markTask : kataSinyal, task
6. help : kataSinyal
'''
def main(query):
    
    global isRun
    isRun = False
    query = cleanQuery(query)

    rAddTask(query, False)
    if isRun:
        return rAddTask(query, True)

    rShowDeadline(query)
    if isRun:
        return rShowDeadline(query)
    
    rUpdateTask(query)     
    if isRun:
        return rUpdateTask(query) 

    rMarkTask(query)
    if isRun:
        return rMarkTask(query)

    rHelp(query)
    if isRun:
        return rHelp(query)

    rHelp(query)   
    if isRun:
        return rHelp(query)

    rSeeTask(query)
    if isRun:
        return rSeeTask(query)

    if not isRun:
        return "Maaf, pesan tidak dikenali atau format salah, ketik help untuk bantuan."
    return