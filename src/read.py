# SQLITE3
def readsql():
    import sqlite3 as sql

    conn = sql.connect(":memory:")
    c = conn.cursor()


    # bikin tabel film
    # asumsi rating sampe 5
    c.execute("""
    CREATE TABLE IF NOT EXISTS task (
    id INTEGER PRIMARY KEY, tanggal TEXT,
    kodematkul TEXT, jenis TEXT, topik TEXT)
    """)
    conn.commit()

    # insert to db
    data = [
        ("Doraemon Stand By Me",4,2014,2,50000,'poster/doraemon.jpg'),
        ("Naruto the Movie",5,2015,3,50000,'poster/naruto.jpg'),
        ("Nanti Kita Cerita Tentang Hari Ini",3,2019,2,50000,'poster/nktchi.jpg'),
        ("Straight Outta Compton",4,2015,2,50000,'poster/nwa.jpg'),
        ("Parasite",1,2019,54,50000,'poster/parasite.jpg'),
        ("Dua Garis Biru",2,2019,32,50000,'poster/duagb.jpg'),
        ("Imperfect",4,2019,12,50000,'poster/imperfect.jpg'),
        ("Raya The Last Dragon",0,2021,2,50000,'poster/raya.jpg'),
        ("Rush Hour 3",5,2007,61,50000,'poster/rushhour3.jpg'),
        ("Spongebob The Movie",3,2021,11,50000,'poster/spongebob.jpg'),
        ("Unfriended",2,2018,9,50000,'poster/unfriended.jpg'),
        ("Sang Pemimpi",4,2009,13,50000,"poster/sangpemimpi.jpg"),
        ("Black Panther",4,2018,27,50000,"poster/blackpanther.jpg"),
        ("Midsommar",1,2019,29,50000,"poster/midsommar.jpg"),
        ("Luca",5,2021,2,50000,"poster/luca.jpg"),
        ("Ip Man 4",3,2019,21,50000,"poster/ipman4.jpg"),
        ("Bohemian Rhapsody",3,2018,43,50000,"poster/bohemian.jpg"),
        ("Joker",3,2019,49,50000,"poster/joker.jpg"),
        ("Boyhood",5,2014,22,50000,"poster/boyhood.jpg"),
        ("21 Jumpstreet",5,2012,69,50000,"poster/21js.jpg")
    ]

    # insert
    c.executemany("INSERT INTO task VALUES (?,?,?,?,?,?)", data)


    # fetchall database
    c.execute("SELECT * FROM task")
    arrdb = c.fetchall()
    conn.commit()

    db = []
    key = ['id','tanggal','kodematkul','jenis','topik']
    for data in arrdb:
        db.append(dict(zip(key, data)))
    return db

def readcsv():
    import csv
    csv_file = open('dbfilm.csv')
    csv = csv.reader(csv_file, delimiter=',')
    db = []
    key = ['id','tanggal','kodematkul','jenis','topik']
    for data in csv:
        db.append(dict(zip(key, data)))
    return db