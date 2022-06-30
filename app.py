import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def hh():
    hh = []
    for h in range(24):
        if h < 10:
            hr = '0{}:00'.format(h)
        else:
            hr = '{}:00'.format(h)
        
        hh.append(hr)

    return hh

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
    hhmm = hh_mm()
    if request.method == 'POST':
        hour = request.form['hours']
        v1 = request.form['v1']
        v2 = request.form['v2']
        v3 = request.form['v3']

        if v1 == '' or v2 == '' or v3 == '':
            flash('No se aceptan valores vacios')
            return render_template('create.html', hhmm = hhmm)

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
                    
                    
                    conn.execute('UPDATE voltajes SET v1 =?, v2=?, v3=?'
                                'WHERE hora = ?',
                                    ( v1, v2, v3, hour))
                    conn.commit()
                    conn.close()
                    flash('Registro guardado!')
                    return redirect(url_for('voltaje'))
                
            conn = get_db_connection()
            conn.execute('INSERT INTO voltajes (hora, v1, v2, v3) VALUES(?,?,?,?)',
                            (hour, v1, v2, v3))
            conn.commit()
            conn.close()
            flash('Registro guardado!')
            return redirect(url_for('voltaje'))


    return render_template('create.html', hhmm = hhmm)


@app.route('/refrigeracion')
def refrigeracion():
    conn =  get_db_connection()
    refrigeraci =  conn.execute('SELECT * FROM refrigeracion').fetchall()

    conn.close()
    hr = hh()
    return render_template('refrigeracion.html', refrigeraci=refrigeraci, hr = hr)


@app.route('/createRef', methods=('GET', 'POST'))
def createRef():
    hr = hh()
    if request.method == 'POST':
        hour = request.form['hours']
        fil1 = request.form['fil1']
        flu1 = request.form['flu1']
        inter1 = request.form['inter1']
        fil2 = request.form['fil2']
        flu2 = request.form['flu2']
        inter2 = request.form['inter2']

        if not hour:
            flash('La hora es requerida!')
        else:
            conn = get_db_connection()
            horas =  conn.execute('SELECT hora FROM refrigeracion').fetchall()
            conn.commit()
            conn.close()
            for h in horas:

                if hour == h[0]:
                    conn = get_db_connection()
                    
                    
                    conn.execute('UPDATE refrigeracion SET filtroU1 =?, filtroU2 =?, flujometroU1=?, flujometroU2=?, intercambiadorU1=?,intercambiadorU2=?'
                                'WHERE hora = ?',
                                    ( fil1, fil2, flu1, flu2, inter1, inter2, hour))
                    conn.commit()
                    conn.close()
                    flash('Registro guardado!')
                    return redirect(url_for('refrigeracion'))
                
            conn = get_db_connection()
            conn.execute('INSERT INTO refrigeracion (hora, filtroU1, filtroU2, flujometroU1, flujometroU2, intercambiadorU1,intercambiadorU2) VALUES(?,?,?,?,?,?,?)',
                            (hour, fil1, fil2, flu1, flu2, inter1, inter2))
            conn.commit()
            conn.close()
            flash('Registro guardado!')
            return redirect(url_for('refrigeracion'))


    return render_template('createRef.html', hr = hr)


@app.route('/resetR', methods=('POST',))
def resetR():
    conn = get_db_connection()
    conn.execute('DELETE FROM refrigeracion')
    conn.commit()
    conn.close()
    flash('tabla reiniciada')
    return render_template('refrigeracion.html')

@app.route('/resetV', methods=('POST',))
def resetV():
    conn = get_db_connection()
    conn.execute('DELETE FROM voltajes')
    conn.commit()
    conn.close()
    flash('tabla reiniciada')
    return render_template('voltaje.html')