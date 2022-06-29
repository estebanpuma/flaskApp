import sqlite3

connection = sqlite3.connect('database.db')

print('se conecto')

with open('schema.sql') as f:
    print('abrio')
    connection.executescript(f.read())

print('leyo')
cur = connection.cursor()


connection.commit()
connection.close()