import os

from flask import Flask, session,render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
  #  raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine('postgres://nysqtbkbaoexhh:04dccd0f6c64186ca6b9d49f288b49b85930ea913d560828c79aa5fe4fd1e256@ec2-54-221-201-212.compute-1.amazonaws.com:5432/d6v3stt6deu3s5');
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO"

@app.route("/books")
def books():
    """Lists all books."""
    books = db.execute("SELECT * FROM books").fetchall()
    for book in books:
        print(f"Book {book.id}: {book.isbn}: {book.title}: {book.year}  ")
    return render_template("allbooks.html", books=books)
