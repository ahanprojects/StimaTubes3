import sqlite3

DATABASE_NAME = "Course.db"

def addtoDatabase(title,desc,price,filepath,author,email):
    # create a database or connect to one
    conn = sqlite3.connect(DATABASE_NAME)
    # create cursor
    c = conn.cursor()
    # insert into query
    c.execute("""INSERT INTO course (Title, Description, Price, File, Author, Email) VALUES ("{}", "{}", "{}", "{}", "{}", "{}");""".format(title,desc,price,filepath,author,email))

    # commit changes
    conn.commit()

    # close connection
    conn.close()

def checkisTitleValid(titlename, email):
    # create a database or connect to one
    conn = sqlite3.connect(DATABASE_NAME)
    # create cursor
    c = conn.cursor()   

    c.execute("SELECT * FROM course WHERE Title is '{}';".format(titlename))
    records = c.fetchall()
    if(len(records) > 0):
        return False
    else:
        return True

def showDatainTerminal():
    # create a database or connect to one
    conn = sqlite3.connect(DATABASE_NAME)
    # create cursor
    c = conn.cursor()   

    c.execute("SELECT * FROM course")
    records = c.fetchall()
    for item in records:
        print(item)
    return records

# return True if nothing is null, else false
def checkNull(title,desc,price,filepath):
    if(len(title) == 0):
        # messagebox.showinfo("Null entry","Title is empty")
        return False,0
    
    if(len(desc) == 0):
        # messagebox.showinfo("Null entry","Description is empty")
        return False,1
    
    try:
        if(len(price) == 0):
            # messagebox.showinfo("Null entry","Price is empty")
            return False,2
        price = int(price)
    except ValueError:
            # messagebox.showinfo("Invalid price","Price should be number")
            return False,3

    if(len(filepath) == 0 ):
        # messagebox.showinfo("Null entry","Please upload a material file")
        return False,4

    # else
    return True,5
