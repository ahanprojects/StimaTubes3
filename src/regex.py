import re
import string
from dbfunction import *

# txt = "The rain in Spain"
# x = re.search("^The.*Spain$", txt)
# print(x)
# kataPentingJenis = ["Kuis", "Ujian", "Tucil", "Tubes", "Praktikum"]
# perhitungkan lower upper case ini gaperlu btw cuman nyatet doang
# kataygseringkeluar = ["deadline", "minggu", "hari", "sampai", "task", "menjadi", "selesai"]

# ========================= KMP ==============================
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

# ============================================

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

# =============== FUNGSI REGEX =========================
def rAddTask(query):
    # harus punya empat komponen : tanggal, kode matkul, jenis (kata penting), topik
    # ide : kode, jenis, topik ditulis terurut. tanggal ga harus.

    kataPenting = ["kuis", "ujian", "tucil", "tubes", "praktikum"]
    query = cleanQuery(query)

    # cari tanggal
    arrtgl = cariTanggal(query)
    if len(arrtgl) != 1:
        # misal gaada tanggal, atau tanggal ada lebih dari 1, berarti bukan addtask
        print("tanggal not valid")
        return

    # cari jenis
    bool_jenis = False
    for kata in kataPenting:
        if KMPSearch(kata,query):
            bool_jenis = True
            jenis = kata
            break
    if not bool_jenis:
        print("jenis not found")
        return

    arr_query = query.split()
    # jika setelah jenis gaada tulisan lagi, ga valid
    for i,kata in enumerate(arr_query):
        if kata == jenis:
            idx_jenis = i

    if jenis == arr_query[len(arr_query)-1]:    # Jika jenis merupakan kata terakhir pada text
        print("Kode matkul not found.")
        return
    else:
        idx_kode = idx_jenis+1
        kode = arr_query[idx_kode]
    
    # topik
    if arr_query[len(arr_query)-1] == arrtgl[0]:    # kalau tanggal ditulis diakhir
        if arr_query[len(arr_query)-2].lower() not in ['pada','tanggal']:
            arr_topik = arr_query[idx_kode+1:len(arr_query)-2]
        else: # ada kata pada atau tanggal
            arr_topik = arr_query[idx_kode+1:len(arr_query)-3]
    else:   
        arr_topik = arr_query[idx_kode+1:len(arr_query)-1]
    topik = ' '.join(arr_topik)
    if topik == '':
        print("gaada topik")
        return

    # return
    ret = [arrtgl[0], kode, jenis, topik]
    print(ret)
    # addTask(arrtgl[0], kode, jenis, topik)


def rSeeTask(query):
    # periksa bakal make fungsi seeAll, berdasarkan minggu atau hari dll.

    kataPenting = ["kuis", "ujian", "tucil", "tubes", "praktikum"]
    query = cleanQuery(query)

    # cari kata "deadline"
    if not KMPSearch("deadline",query):
        print("Tidak ada kata deadline.")
        return
    else:
        print("Kata deadline ditemukan.")

    # cari apakah ada jenis
    jenis = ''
    for kata in kataPenting:
        if KMPSearch(kata,query):
            jenis = kata
            break

    # cari tanggal
    arrtgl = cariTanggal(query)

    # Pakai yang periode
    if len(arrtgl) == 2:    
        seeTaskByWaktu(date1=arrtgl[0], date2=arrtgl[1], jenis=jenis)
        return

    arr_query = query.split()

    # jika ada kata minggu
    if KMPSearch('minggu',query):
        # cari minggu adalah kata ke berapa pada query
        for i,kata in enumerate(arr_query):
            if kata == 'minggu':
                id_jumlah_minggu = i - 1
                break
        print("kata minggu ditemukan", arr_query[id_jumlah_minggu])
        seeTaskByWaktu(jumlah_minggu=int(arr_query[id_jumlah_minggu]), jenis=jenis)
        return
    
    if KMPSearch('hari',query):
        # cari hari adalah kata ke berapa pada query
        for i,kata in enumerate(arr_query):
            if kata == 'hari':
                id_jumlah_hari = i - 1
                break
        print("kata hari ditemukan", arr_query[id_jumlah_hari])
        seeTaskByWaktu(jumlah_hari=int(arr_query[id_jumlah_hari]), jenis=jenis)
        return

    # Pakai yang seeAll atau hari ini
    # asumsi : kalau ada kata sejauh dan sampai, pake seeTaskAll
    if len(arrtgl) == 0:
        if KMPSearch('hari ini',query) and not KMPSearch('sampai',query) and not KMPSearch('sejauh',query):
            seeTaskByWaktu(jumlah_hari=0, jenis=jenis)
        else:
            seeTaskAll()
        return
    return

def rShowDeadline(query):
    # hanya untuk tugas (tubes, tucil)
    # cari kata "deadline"
    if not KMPSearch("deadline",query):
        print("Tidak ada kata deadline.")
        return
    else:
        print("Kata deadline ditemukan.")
    
    # cari kata tugas, tubes, atau tucil
    if not KMPSearch('tugas',query) and not KMPSearch('tubes',query) and not KMPSearch('tucil',query):
        print('tidak ada kata tugas')
        return
    
    arr_query = query.split()
    # cari kode matkul
    for i,kata in enumerate(arr_query):
        if kata == 'tubes' or kata == 'tucil':
            id_kode = i + 1
            break

    showDeadline(arr_query[id_kode])

def rUpdateTask(query):
    # cari kata "deadline"
    if not KMPSearch("deadline",query):
        print("Tidak ada kata deadline.")
        return
    else:
        print("Kata deadline ditemukan.")

    arrtgl = cariTanggal(query)
    if len(arrtgl) != 1:
        # misal gaada tanggal, atau tanggal ada lebih dari 1, berarti bukan addtask
        print("tanggal not valid")
        return
    # diundur, diubah, diganti ?
    # menjadi, ke ?

    # cari kata "task"
    if not KMPSearch("task",query):
        print("Tidak ada kata task.")
        return
    else:
        print("Kata task ditemukan.")

    # cari id task
    arr_query = query.split()
    # cari kode matkul
    for i,kata in enumerate(arr_query):
        if kata == 'task':
            id = i + 1
            break
    updateTask(id,arrtgl[0])

def rMarkTask(query):
    # Saya sudah selesai mengerjakan task ID
    # cari kata "sudah"
    kataSinyal = ['udah','kerja','mengerja','selesai']
    adaSinyal = False
    for kata in kataSinyal:
        if KMPSearch(kata,query):
            print("Kata "+kata+" ditemukan.")
            adaSinyal = True
    if not adaSinyal:
        print("Kata sinyal tidak ditemukan")

    # cari kata "task"
    if not KMPSearch("task",query):
        print("Tidak ada kata task.")
        return
    else:
        print("Kata task ditemukan.")

    # cari id task
    arr_query = query.split()
    # cari kode matkul
    for i,kata in enumerate(arr_query):
        if kata == 'task':
            id = i + 1
            break
    markTask(id)

def rHelp():
    pass