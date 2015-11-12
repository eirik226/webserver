# -*- coding: utf-8 -*-
# imports
import sqlite3
from flask import Flask, session, request, g, redirect, url_for, \
 abort, render_template, flash, jsonify, escape, flash
 
# konfigurasjon av globale variable
DATABASE = 'nyheter.db'
DEBUG = True
SECRET_KEY = 'Qh\x84J\xbb^\xeb\x8d\x96\x07\xa1\xf2Q\x905(\xbca\x06\x13\x1a\xb5\xf6\xad'

# lager og initialiserer app’en
app = Flask(__name__)
app.config.from_object(__name__)
@app.route('/', methods=['GET', 'POST'])

def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
          error = 'Feil innlogging'
        else:
          session['logged_in'] = True
          flash('Du er nå innlogget!')
          return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('logged_in', None)
    flash('Du er nå logget ut!')
    return redirect(url_for('login'))

@app.route('/index.html')

def index():
    """Leter etter data i databasen og viser de."""
    db = get_db()
    cur = db.execute('select * from nyheter order by id desc')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)
 
@app.route('/add', methods=['POST'])
def add_entry():
    """Legger inn nye data i databasen."""
    db = get_db()
    db.execute('insert into nyheter(tittel, nyhet, forfatter, dagens) values (?, ?, ?, ?)',
    [request.form['tittel'], request.form['nyhet'],
    request.form['forfatter'], request.form['dagens']])
    db.commit()
    flash('Innlegget ble sendt og lagret i databasen')
    return redirect(url_for('index'))
 
# kobler til databasen
def connect_db():
    """Kobler til databasen."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
 
# lager databasen
def init_db():
    with app.app_context():
      db = get_db()
      with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
      db.commit()
	
# åpner forbindelsen til databasen
def get_db():
    if not hasattr(g, 'sqlite_db'):
      g.sqlite_db = connect_db()
    return g.sqlite_db
 
# lukker forbindelsen til databasen
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
      g.sqlite_db.close()

@app.route('/delete/<post_id>', methods=['GET'])
def delete_entry(post_id):
    '''Delete post from database'''
    result = { 'status':0, 'message': 'Error' }
    try:
        db = get_db()
        db.execute('delete from nyheter where id=' + post_id)
        db.commit()
        result = { 'status':1, 'message': "Post Deleted" }
    except Exception as e:
        result = { 'status':0, 'message': repr(e) }

    
    return jsonify(result)
	  
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
