import sqlite3

def create_database():
    conn = sqlite3.connect('movies.db')
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

if __name__ == "__main__":
    create_database()
    print("Database and table created.")