import sqlite3
import time
import datetime
import random

conn = sqlite3.connect('tutorial.db')
c = conn.cursor() # courser to db

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS stuffPlot(unix REAL, datestamp TEXT, keyword TEXT, value REAL)')

def data_entry():
    c.execute("INSERT INTO stuffPlot VALUES(112123, '2016-01-02', 'Python', 6)")
    conn.commit()
    c.close()
    conn.close()


def dynamic_data_entry():
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    keyword = 'Python'
    value = random.randrange(0,10)
    c.execute("INSERT INTO stuffPlot (unix, dateSTAMP, keyword, value) VALUES(?, ?, ?,?)", 
    (unix, date, keyword, value))
    conn.commit()

def read_from_db():
    c.execute("SELECT * FROM stuffPlot WHERE  value = 3 AND keyword ='Python'")
    data = c.fetchall()
    for row in data:
        print(row)

create_table()

""" for i in range(10):
    dynamic_data_entry()
    time.sleep(1)

c.close()
conn.close() """


read_from_db()
#create_table()
#data_entry()