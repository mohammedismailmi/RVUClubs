import sqlite3


def initialize_db():
    conn = sqlite3.connect('RVUClubs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clubs (
            club_id INTEGER PRIMARY KEY,
            club_name TEXT NOT NULL,
            core_team TEXT NOT NULL,
            events TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def load_data_from_csv(csv_file):
    import pandas as pd
    data = pd.read_csv(csv_file)
    conn = sqlite3.connect('RVUClubs.db')
    cursor = conn.cursor()
    for index, row in data.iterrows():
        cursor.execute('''
            INSERT INTO clubs (club_id, club_name, core_team, events)
            VALUES (?, ?, ?, ?)
        ''', (row['club_id'], row['club_name'], row['core_team'], row['events']))
    conn.commit()
    conn.close()


def get_all_clubs():
    conn = sqlite3.connect('RVUClubs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clubs')
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_club(club_name, core_team, events):
    conn = sqlite3.connect('RVUClubs.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clubs (club_name, core_team, events)
        VALUES (?, ?, ?)
    ''', (club_name, core_team, events))
    conn.commit()
    conn.close()


def update_club(club_id, club_name, core_team, events):
    conn = sqlite3.connect('RVUClubs.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clubs
        SET club_name = ?, core_team = ?, events = ?
        WHERE club_id = ?
    ''', (club_name, core_team, events, club_id))
    conn.commit()
    conn.close()


def delete_club(club_id):
    conn = sqlite3.connect('RVUClubs.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM clubs WHERE club_id = ?
    ''', (club_id,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    initialize_db()
    load_data_from_csv('clubs.csv')
