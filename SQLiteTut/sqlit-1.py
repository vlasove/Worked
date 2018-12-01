import sqlite3

conn = sqlite3.connect('tutorial.db')
c = conn.cursor() # courser to db

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS stuffPlot(unix REAL, datestamp TEXT, keyword TEXT, value REAL)')

def data_entry():
    c.execute("INSERT INTO stuffPlot VALUES(112123, '2016-01-02', 'Python', 6)")
    conn.commit()
    c.close()
    conn.close()

create_table()
data_entry()