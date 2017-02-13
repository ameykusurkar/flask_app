from flask import Flask, render_template, g, request, redirect, session
from db_utils import get_db, close_db
import json

app = Flask(__name__)
app.secret_key = 'hakuna matata'

@app.route('/')
def index():
    username = 'Nobody'
    if 'username' in session:
        username = session['username']
        db = get_db(g)
        cur = db.execute('select * from entries where username=? order by id desc', [username])
        return render_template('index.html', entries=cur.fetchall(), username=username)
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect('/')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        db = get_db(g)
        db.execute('insert into entries (username, key, value) values (?, ?, ?)',
                   [session['username'], request.form['key'], request.form['value']])
        db.commit()
        return redirect('/')
    else:
        return render_template('add.html')

@app.teardown_appcontext
def close_db_connection(error):
    close_db(error, g)

if __name__ == '__main__':
    app.run()
