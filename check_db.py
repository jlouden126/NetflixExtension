import sqlite3

def check_movie_in_database(title, year):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM movies WHERE title = ? AND year = ?', (title, year))
    result = cursor.fetchone()

    conn.close()

    return result is not None