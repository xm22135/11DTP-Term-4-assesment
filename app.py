from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('chelsea.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with app.open_resource('schema.sql') as f:
        conn.executescript(f.read().decode('utf8'))
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/seasonhistory', methods = ('POST','GET'))
def seasonhistory():
    conn = get_db_connection()
    sql = 'SELECT * from seasons'
    seasons = conn.execute(sql).fetchall()
    conn.close
    return render_template('seasonhistory.html', seasons = seasons)
    
if __name__ == '__main__':
    app.run(debug = True)