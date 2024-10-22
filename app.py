from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3

app = Flask(__name__)

app.secret_key = 'supersupersecretkey'

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
        if not season or not games_played or not games_won or not games_drawn or not games_lost or not goals_for or not goals_against or not goal_difference or not points or not top_assist_maker or not top_goal_scorer:
            flash("All fields are required")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO seasons (season,games_played,games_won,games_drawn,games_lost,goals_for,goals_against,goal_difference,points,top_goal_scorer,top_assist_maker) Values (?,?,?,?,?,?,?,?,?,?,?)', (season,games_played,games_won,games_drawn,games_lost,goals_for,goals_against,goal_difference,points,top_goal_scorer,top_assist_maker))
            conn.commit()
            conn.close
            return render_template('addrecords.html')
    return render_template('addrecords.html')

@app.route('/delete/ <int:id>', methods = ('POST',))
def delete_records(id):
    conn = get_db_connection()
    conn.execute('DELETE from seasons WHERE season_id = ?',(id,))
    conn.commit()
    conn.close
    flash('Record Deleted Successfully')
    return redirect(url_for('seasonhistory'))

@app.route("/editrecord/<int:id>", methods = ('GET', 'POST'))
def edit_record(id):
    conn = get_db_connection()
    seasons = conn.execute('SELECT * from users WHERE season_id = ?'(id,)).fetchone()

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
        if not season or not games_played or not games_won or not games_drawn or not games_lost or not goals_for or not goals_against or not goal_difference or not points or not top_assist_maker or not top_goal_scorer:
            flash("All fields are required")
        else:
            conn = get_db_connection()
            conn.execute('UPDATE seasons SET season = ?, games_played = ?, games_won = ?, games_drawn = ?, games_lost = ?, goals_for = ?,goals_against = ?,goal_difference = ?,points = ?,top_goal_scorer = ?,top_assist_maker = ? WHERE season_id = ?' (season,games_played,games_won,games_drawn,games_lost,goals_for,goals_against,goal_difference,points,top_goal_scorer,top_assist_maker, id))
            conn.commit()
            conn.close
            return redirct(url_for('seasonhistory'))
    return render_template('edit.html', seasons = seasons)


if __name__ == '__main__':
    app.run(debug = True)