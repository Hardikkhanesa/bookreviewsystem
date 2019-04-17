import os

from flask import Flask, session,render_template
from flask_session import Session
import sqlite3

app = Flask(__name__)

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
  #  raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        con = sqlite3.connect(db_file, check_same_thread=False)
        return con
    except sqlite3.Error as e:
        print(e)

    return None


conn = create_connection("books1.db")

@app.route("/")
def index():
    return "Project 1: TODO"

@app.route("/books")
def books():
    """Lists all books."""
    books = conn.execute("SELECT * FROM books").fetchall()
    le = len(books)
    print(le)
    print(books[0][0])
    return render_template("allbooks.html", books=books, len=le)


if __name__ == '__main__':
    app.run(host='127.0.0.1')
