from flask import Flask, render_template, g, request, redirect
from db_utils import get_db, close_db
import json

app = Flask(__name__)

@app.route('/')
def index():
    db = get_db(g)
    cur = db.execute('select * from entries order by id desc')
    return render_template('index.html', entries=cur.fetchall())

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        db = get_db(g)
        db.execute('insert into entries (key, value) values (?, ?)',
                   [request.form['key'], request.form['value']])
        db.commit()
        return redirect('/')
    else:
        return render_template('add.html')

@app.teardown_appcontext
def close_db_connection(error):
    close_db(error, g)

if __name__ == '__main__':
    app.run()
