import datetime

a = datetime.datetime.strptime("2008-12-20", "%Y-%m-%d").strftime("%d-%m-%Y")
print(str(a))