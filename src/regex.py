import re
import string

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
print(x)

kataPentingJenis = ["Kuis", "Ujian", "Tucil", "Tubes", "Praktikum"]

# perhitungkan lower upper case ini gaperlu btw cuman nyatet doang
# kataygseringkeluar = ["deadline", "minggu", "hari", "sampai", "task", "menjadi", "selesai"]
def cleanQuery(x): 
    query = x
    # print("lowercase == uppercase")
    query = query.lower()
    query = re.sub(r'\s{2,}', ' ', query)
    return query

def cariTanggal(x):
    tanggal = re.findall('[0-9]{2}-[0-9]{2}-[0-9]{4}', x)
    if tanggal is not None:
        return tanggal
    return []


    
query = str(input("masukkan input :"))
newquery = cleanQuery(query)
tanggal = cariTanggal(newquery)
print(newquery)
print(tanggal)
