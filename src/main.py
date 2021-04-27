import re
import string

# ================================= DB FUNCTIONS =================================
# Fungsi manipulasi database

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
    task = [tanggal, kodematkul.upper(), jenis.capitalize(), topik.capitalize(), 0]
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
    c.execute("SELECT * FROM Task WHERE Status = 0")
    tasks = c.fetchall()
    conn.commit()
    print("[DAFTAR DEADLINE]")
    print("(ID) Tanggal - Kode Matkul - Jenis Task - Topik")
    for i,task in enumerate(tasks):
        print(str(i+1)+". "+"(ID: "+str(task[0])+") - "+str(task[1])+" - "+str(task[2])+" - "+str(task[3])+" - "+str(task[4]))
    
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
        return
    print("[DAFTAR DEADLINE]")
    print("(ID) Tanggal - Kode Matkul - Jenis Task - Topik - Status")
    for i,task in enumerate(tasks):
        print(str(i+1)+". "+"(ID: "+str(task[0])+") - "+str(task[1])+" - "+str(task[2])+" - "+str(task[3])+" - "+str(task[4]))
    print()

# 3
def showDeadline(kodematkul):
    kodematkul = kodematkul.upper()
    # open db
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    # cari nama kodematkul pada database
    c.execute("SELECT * FROM Task WHERE KodeMatkul = ? AND (JenisTask = ? OR JenisTask = ?)", [kodematkul,'Tucil','Tubes'])
    tasks = c.fetchall()
    conn.commit()

    if len(tasks) == 0:
        print("Tidak ada tugas "+kodematkul)
        return
    # print deadlinenya
    for task in tasks:
        print(task[2]+" - "+task[1]+" - "+task[3])

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
        print("Task ID: "+str(ID)+" tidak ditemukan.")
    else:
        # terus update
        c.execute("UPDATE Task SET Status = 1 WHERE ID = ?", [ID])
        conn.commit()
        print("Berhasil menandai Task, ID: "+str(ID))

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

# ================================= KMP =================================
def KMPSearch(pattern, text):
    # diclean query dulu dua-duanya
    pattern = cleanQuery(pattern)
    text = cleanQuery(text)
    M = len(pattern)
    N = len(text)

    # create lps[] that will hold the longest prefix suffix
    # values for patterntern
    lps = [0]*M
    j = 0 # index for pattern[]

    # Preprocess the patterntern (calculate lps[] array)
    computeLPSArray(pattern, M, lps)

    i = 0 # index for text[]
    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == M:
            # print ("Found pattern at index " + str(i-j))
            j = lps[j-1]
            return True

        # mismatch after j matches
        elif i < N and pattern[j] != text[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1

    return False

def computeLPSArray(pattern, M, lps):
    len = 0 # length of the previous longest prefix suffix

    lps[0] # lps[0] is always 0
    i = 1

    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pattern[i]== pattern[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar
            # to search step.
            if len != 0:
                len = lps[len-1]

                # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i += 1


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

# ================================= FUNGSI REGEX =================================
def rAddTask(query):
    # harus punya empat komponen : tanggal, kode matkul, jenis (kata penting), topik
    # ide : kode, jenis, topik ditulis terurut. tanggal ga harus.

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

    arr_query = query.split()
    # jika setelah jenis gaada tulisan lagi, ga valid
    for i,kata in enumerate(arr_query):
        if kata == jenis:
            idx_jenis = i

    if jenis == arr_query[len(arr_query)-1]:    # Jika jenis merupakan kata terakhir pada text
        return
    else:
        idx_kode = idx_jenis+1
        kode = arr_query[idx_kode]
    
    # topik
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
    addTask(date, kode, jenis, topik)
    global isRun
    isRun = True


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

    # cari kata "deadline"
    if jenis == '':
        if not KMPSearch("deadline",query):
            return

    # cari tanggal
    arrtgl = cariTanggal(query)

    # Pakai yang periode
    if len(arrtgl) == 2:    
        date1 = datetime.datetime.strptime(arrtgl[0], '%d-%m-%Y').date()
        date2 = datetime.datetime.strptime(arrtgl[1], '%d-%m-%Y').date()
        seeTaskByWaktu(date1=date1, date2=date2, jenis=jenis)
        isRun = True
        return

    arr_query = query.split()

    # jika ada kata minggu
    if KMPSearch('minggu',query):
        # cari minggu adalah kata ke berapa pada query
        for i,kata in enumerate(arr_query):
            if kata == 'minggu':
                id_jumlah_minggu = i - 1
                break
        seeTaskByWaktu(jumlah_minggu=int(arr_query[id_jumlah_minggu]), jenis=jenis)
        isRun = True
        return
    
    if KMPSearch('hari',query):
        # cari hari adalah kata ke berapa pada query
        for i,kata in enumerate(arr_query):
            if kata == 'hari':
                id_jumlah_hari = i - 1
                break
        
        try:
            seeTaskByWaktu(jumlah_hari=int(arr_query[id_jumlah_hari]), jenis=jenis)
            isRun = True
            return
        except:
            pass

    # Pakai yang seeAll atau hari ini
    # asumsi : kalau ada kata sejauh dan sampai, pake seeTaskAll
    if len(arrtgl) == 0:
        if KMPSearch('hari ini',query) and not KMPSearch('sampai',query) and not KMPSearch('sejauh',query):
            seeTaskByWaktu(jumlah_hari=0, jenis=jenis)
        else:
            seeTaskAll()
        isRun = True
        return
    return

def rShowDeadline(query):
    # hanya untuk tugas (tubes, tucil)
    global isRun

    # cari kata "deadline"
    if not KMPSearch("deadline",query):
        return

    # cari kata tugas, tubes, atau tucil
    if not KMPSearch('tugas',query) and not KMPSearch('tubes',query) and not KMPSearch('tucil',query):
        return
    
    arr_query = query.split()
    # cari kode matkul
    for i,kata in enumerate(arr_query):
        if kata == 'tubes' or kata == 'tucil' or kata == 'tugas':
            id_kode = i + 1
            break

    showDeadline(arr_query[id_kode])
    isRun = True

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
    arr_query = query.split()
    # cari kode matkul
    for i,kata in enumerate(arr_query):
        if kata == 'task':
            id = i + 1
            break
    date = datetime.datetime.strptime(arrtgl[0], '%d-%m-%Y').date()
    updateTask(int(arr_query[id]),date)
    global isRun
    isRun = True

def rMarkTask(query):
    # Saya sudah selesai mengerjakan task ID
    # cari kata "sudah"
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
    arr_query = query.split()
    # cari kode matkul
    for i,kata in enumerate(arr_query):
        if kata == 'task':
            id = i + 1
            break
    markTask(int(arr_query[id]))
    global isRun
    isRun = True

def rHelp(query):
    kataSinyal = ['help','bisa','apain','lakukan']
    adaSinyal = False
    for kata in kataSinyal:
        if KMPSearch(kata,query):
            adaSinyal = True
    if not adaSinyal:
        return
    help()
    global isRun
    isRun = True

# ================================= MAIN PROGRAM =================================
kataPenting = ["kuis", "ujian", "tucil", "tubes", "praktikum"]
isRun = False   # ada fungsi yg ke run atau nggas
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
3. showDeadline : deadline, tugas, tubes, tucil
4. updateTask : deadline, 1 date, task
5. markTask : kataSinyal, task
6. help : ?
'''
def main():
    global isRun
    while True:
        isRun = False
        q = str(input("\nQuery : "))
        query = cleanQuery(q)
        rAddTask(query)
        rShowDeadline(query)
        rUpdateTask(query)
        rMarkTask(query)
        rHelp(query)
        rSeeTask(query)
        if not isRun:
            print("Maaf, pesan tidak dikenali.")
    
main()