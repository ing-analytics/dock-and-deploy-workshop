import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Docker!"

@app.route('/db')
def db_test():
    try:
        connection = psycopg2.connect(
            user="user",
            password="password",
            host="db",
            port="5432",
            database="mydatabase"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        return jsonify({"PostgreSQL Version": record})
    except Exception as error:
        return jsonify({"error": str(error)})
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)