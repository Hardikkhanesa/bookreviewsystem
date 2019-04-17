import os

from flask import Flask, session,render_template, request, redirect
from flask_session import Session
import sqlite3

app = Flask(__name__)
app.secret_key = "any random string"

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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cur = conn.cursor()
        rows = cur.execute("SELECT * FROM users WHERE username=?", (username,)).fetchall()
        exists = len(rows)
        if exists != 0:
            return render_template("register.html")
        sql = ''' INSERT INTO users(username, password)
                              VALUES(?, ?) '''
        cur = conn.cursor()
        cur.execute(sql, (username, password))
        conn.commit()
        session['username'] = username
        return render_template("index.html", login_successful=True)
    else:
        return render_template("register.html")

def login(username, password):
    if 'username' in session:
        return True
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password, )).fetchall()
    exists = len(rows)
    if exists != 0:
        session['username'] = username
        return True
    return False

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect("/")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        log = login(username, password)
        return render_template("index.html", login_successful=log)
    else:
        log = False
        if 'username' in session:
            log = True
        return render_template("index.html", login_successful=log)


@app.route("/books")
def books():
    """Lists all books."""
    if 'username' in session:
        books = conn.execute("SELECT * FROM books").fetchall()
        le = len(books)
        print(le)
        print(books[0][0])
        return render_template("allbooks.html", books=books, len=le)
    else:
        return render_template("index.html", loggin_successful=False)


if __name__ == '__main__':
    app.run(host='127.0.0.1')
