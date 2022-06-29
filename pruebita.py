import sqlite3
from time import process_time_ns

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

conn =  get_db_connection()
voltajes =  conn.execute('SELECT * FROM voltajes').fetchall()

horas =  conn.execute('SELECT hora FROM voltajes').fetchall()

print('El objeto: ')
print(horas)


print('las individuakes')
for h in horas:
    print(h[0])
