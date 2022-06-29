import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from importlib_metadata import method_cache

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def hh_mm():
    hhmm = []
    for hh in range(24):
        if hh < 10:
            h = '0{}'.format(hh)
        else:
            h = hh
        
        
        hhmm.append('{}:00'.format(h))
        hhmm.append('{}:30'.format(h))
    
    return hhmm

app = Flask(__name__)
app.config['SECRET_KEY'] = "SUPERSECRET"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voltaje')
def voltaje():
    conn =  get_db_connection()
    voltajes =  conn.execute('SELECT * FROM voltajes').fetchall()

    horas =  conn.execute('SELECT hora FROM voltajes').fetchall()

    conn.close()
    hhmm = hh_mm()
    return render_template('voltaje.html', voltajes = voltajes, hhmm = hhmm, horas=horas)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        hour = request.form['hours']
        v1 = request.form['v1']
        v2 = request.form['v2']
        v3 = request.form['v3']

   
        if not hour:
            flash('La hora es requerida!')
        else:
            conn = get_db_connection()
            horas =  conn.execute('SELECT hora FROM voltajes').fetchall()
            conn.commit()
            conn.close()
            for h in horas:

                if hour == h[0]:
                    conn = get_db_connection()
                    flash('Registro guardado!')
                    
                    conn.execute('UPDATE voltajes SET v1 =?, v2=?, v3=?'
                                'WHERE hora = ?',
                                    ( v1, v2, v3, hour))
                    conn.commit()
                    conn.close()
                    return redirect(url_for('voltaje'))
                
            conn = get_db_connection()
            conn.execute('INSERT INTO voltajes (hora, v1, v2, v3) VALUES(?,?,?,?)',
                            (hour, v1, v2, v3))
            conn.commit()
            conn.close()
            return redirect(url_for('voltaje'))


    hhmm = hh_mm()


    return render_template('create.html', hhmm = hhmm)