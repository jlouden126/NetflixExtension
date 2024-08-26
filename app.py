from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


api_key = os.getenv('OMDB_API_KEY')  # Load the API key from .env
    
def connect_db():
    conn = sqlite3.connect('movies.db')
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            year TEXT,
            rated TEXT,
            genre TEXT,
            imdb_id TEXT,
            imdb_rating TEXT,
            rt_rating TEXT,
            metacritic TEXT,
            director TEXT,
            actors TEXT,
            plot TEXT,
            poster TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def index():
    return "Flask server is running!"

@app.route('/movies', methods=['POST', 'OPTIONS'])
def handle_movie_request():
    print("IT WORKED")
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = headers or '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        return response

    data = request.json
    title = data.get('title')
    year = data.get('year')
    if title and year:
        print("DAT FOUND IN DATABASE")
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM movies WHERE title = ? AND year = ?', (title, year))
        movie_data = cursor.fetchone()

        if movie_data:
            movie_dict = {
                'title': movie_data[1],
                'year': movie_data[2],
                'rated': movie_data[3],
                'genre': movie_data[4],
                'imdbID': movie_data[5],
                'imdbRating': movie_data[6],
                'rtRating': movie_data[7],
                'metacriticRating': movie_data[8],
                'director': movie_data[9],
                'actors': movie_data[10],
                'plot': movie_data[11],
                'poster': movie_data[12]
            }
            conn.close()
            response = jsonify(movie_dict)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 200
        else:
            print("MOVIE NOT FOUND API CALL MADE")
            # If the movie is not found, make an API call to fetch the data
            omdb_api_key = api_key  # Use your OMDB API key
            omdb_url = f"http://www.omdbapi.com/?t={title}&y={year}&apikey={omdb_api_key}"
            omdb_response = requests.get(omdb_url)
            if omdb_response.status_code == 200:
                omdb_data = omdb_response.json()

                # Extract data from the API response
                movie_dict = {
                    'title': omdb_data.get('Title'),
                    'year': omdb_data.get('Year'),
                    'rated': omdb_data.get('Rated'),
                    'genre': omdb_data.get('Genre'),
                    'imdbID': omdb_data.get('imdbID'),
                    'imdbRating': omdb_data.get('imdbRating'),
                    'rtRating': next((rating['Value'] for rating in omdb_data.get('Ratings', []) if rating['Source'] == 'Rotten Tomatoes'), 'N/A'),
                    'metacriticRating': next((rating['Value'] for rating in omdb_data.get('Ratings', []) if rating['Source'] == 'Metacritic'), 'N/A'),
                    'director': omdb_data.get('Director'),
                    'actors': omdb_data.get('Actors'),
                    'plot': omdb_data.get('Plot'),
                    'poster': omdb_data.get('Poster')
                }

                # Insert the data into the database
                cursor.execute('''
                    INSERT INTO movies (title, year, rated, genre, imdb_id, imdb_rating, rt_rating, metacritic, director, actors, plot, poster)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    movie_dict['title'],
                    movie_dict['year'],
                    movie_dict['rated'],
                    movie_dict['genre'],
                    movie_dict['imdbID'],
                    movie_dict['imdbRating'],
                    movie_dict['rtRating'],
                    movie_dict['metacriticRating'],
                    movie_dict['director'],
                    movie_dict['actors'],
                    movie_dict['plot'],
                    movie_dict['poster']
                ))
                conn.commit()
                conn.close()

                response = jsonify(movie_dict)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response, 200
            else:
                conn.close()
                response = jsonify({"error": "Failed to fetch data from OMDB"})
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response, 500  # Return 500 if the API call fails
        
    else:
        response = jsonify({"error": "Invalid data"})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 400

if __name__ == "__main__":
    app.run(debug=True)