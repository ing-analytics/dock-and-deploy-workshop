import psycopg2
from flask import Flask, render_template_string

app = Flask(__name__)

def setup_database():
    try:
        connection = psycopg2.connect(
            user="user",
            password="password",
            host="db",
            port="5432",
            database="mydatabase"
        )
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                year INT NOT NULL,
                rating FLOAT NOT NULL
            );
        """)

        cursor.execute("SELECT COUNT(*) FROM movies;")
        if cursor.fetchone()[0] == 0:
            movies = [
                ("The Shawshank Redemption", 1994, 9.3),
                ("The Godfather", 1972, 9.2),
                ("The Dark Knight", 2008, 9.0),
                ("Schindler's List", 1993, 9.0),
                ("12 Angry Men", 1957, 9.0),
                ("The Lord of the Rings: Return of the King", 2003, 8.9),
                ("Pulp Fiction", 1994, 8.9),
                ("The Good, the Bad and the Ugly", 1966, 8.8),
                ("Fight Club", 1999, 8.8),
                ("Forrest Gump", 1994, 8.8)
            ]
            cursor.executemany("INSERT INTO movies (title, year, rating) VALUES (%s, %s, %s)", movies)
            connection.commit()

    except Exception as error:
        print(f"Error setting up the database: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/')
def home():
    html_content = """
    <html>
        <head>
            <title>IMDb Top Movies</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
                button { font-size: 16px; padding: 10px 20px; margin-top: 20px; cursor: pointer; }
            </style>
        </head>
        <body>
            <h1>Welcome to the IMDb Top Movies API!</h1>
            <p>Click the button below to see the top 10 movies.</p>
            <button onclick="window.location.href='/movies'">See Movies</button>
        </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/movies')
def get_movies():
    try:
        connection = psycopg2.connect(
            user="user",
            password="password",
            host="db",
            port="5432",
            database="mydatabase"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT title, year, rating FROM movies ORDER BY rating DESC LIMIT 10;")
        movies = cursor.fetchall()

        html_content = """
        <html>
            <head>
                <title>Top IMDb Movies</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
                    table { width: 60%; margin: auto; border-collapse: collapse; }
                    th, td { padding: 10px; border: 1px solid black; }
                    th { background-color: #f4b400; color: white; }
                    td { background-color: #fdf6e3; }
                </style>
            </head>
            <body>
                <h1>Top 10 IMDb Movies</h1>
                <table>
                    <tr><th>Title</th><th>Year</th><th>Rating</th></tr>
        """
        
        for movie in movies:
            html_content += f"<tr><td>{movie[0]}</td><td>{movie[1]}</td><td>{movie[2]}</td></tr>"

        html_content += """
                </table>
                <br>
                <button onclick="window.location.href='/'">Go Home</button>
            </body>
        </html>
        """
        return render_template_string(html_content)
    except Exception as error:
        return f"<p>Error: {error}</p>"
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=5000)
