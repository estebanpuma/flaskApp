import sqlite3

connection = sqlite3.connect('database.db')

print('se conecto')

with open('schema.sql') as f:
    print('abrio')
    connection.executescript(f.read())

print('leyo')
cur = connection.cursor()

cur.execute('INSERT INTO voltajes (hora, v1, v2, v3) VALUES(?,?,?,?)',
            ('00:00', 210, 220, 222)
            )


connection.commit()
connection.close()