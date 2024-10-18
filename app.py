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
    
@app.route('/addrecords', methods = ('POST','GET'))
def addrecords():
    if request.method == 'POST':
        season = request.form['season']
        games_played = request.form['games_played']
        games_won = request.form['games_won']
        games_drawn = request.form['games_drawn']
        games_lost = request.form['games_lost']
        goals_for = request.form['goals_for']
        goals_against = request.form['goals_against']
        goal_difference = request.form['goal_difference']
        points = request.form['points']
        top_goal_scorer = request.form['top_goal_scorer']
        top_assist_maker = request.form['top_assist_maker']
        conn = get_db_connection()
        conn.execute('INSERT INTO seasons (season,games_played,games_won,games_drawn,games_lost,goals_for,goals_against,goal_difference,points,top_goal_scorer,top_assist_maker) Values (?,?,?,?,?,?,?,?,?,?,?)', (season,games_played,games_won,games_drawn,games_lost,goals_for,goals_against,goal_difference,points,top_goal_scorer,top_assist_maker))
        conn.commit()
        conn.close
        return render_template('addrecords.html')
    return render_template('addrecords.html')

if __name__ == '__main__':
    app.run(debug = True)