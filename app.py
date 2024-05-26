from flask import Flask, render_template, request, redirect, url_for
from clubs_db import get_all_clubs, add_club, update_club, delete_club

app = Flask(__name__)


@app.route('/')
def index():
    clubs = get_all_clubs()
    return render_template('index.html', clubs=clubs)


@app.route('/add', methods=['POST'])
def add():
    club_name = request.form['club_name']
    core_team = request.form['core_team']
    events = request.form['events']
    add_club(club_name, core_team, events)
    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    club_id = request.form['club_id']
    club_name = request.form['club_name']
    core_team = request.form['core_team']
    events = request.form['events']
    update_club(club_id, club_name, core_team, events)
    return redirect(url_for('index'))


@app.route('/delete/<int:club_id>')
def delete(club_id):
    delete_club(club_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
