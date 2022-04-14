import sqlite3

conn = sqlite3.connect("./attendance.db")

cursor = conn.cursor()
sql_query = """ CREATE TABLE student (
    id BLOB,
    name text NOT NULL,
    rollNo BLOB NOT NULL,
    standard integer NOT NULL,
    section text
)"""
cursor.execute(sql_query)
cursor.close
cursor = conn.cursor()
cursor.execute('CREATE TABLE Class (id BLOB,Name TEXT,standard integer,Time TEXT,Date TEXT)')
cursor.close
conn.commit() 
