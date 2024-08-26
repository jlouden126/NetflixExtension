import sqlite3

def store_movie_data(data):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO movies (title, year, rated, genre, imdb_id, imdb_rating, rt_rating, metacritic, director, actors, plot, poster) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('Title'),
        data.get('Year'),
        data.get('Rated'),
        data.get('Genre'),
        data.get('imdbID'),
        data.get('imdbRating'),
        next((rating['Value'] for rating in data.get('Ratings', []) if rating['Source'] == 'Rotten Tomatoes'), 'N/A'),
        next((rating['Value'] for rating in data.get('Ratings', []) if rating['Source'] == 'Metacritic'), 'N/A'),
        data.get('Director'),
        data.get('Actors'),
        data.get('Plot'),
        data.get('Poster')
    ))

    conn.commit()
    conn.close()