import os
#import requests
from flask import (
    Flask,
    g,
    session,
    redirect,
    request,
    render_template,
    url_for
)
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#from models import *

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://tibchumrwgmuym:767d5d8610d692050757f686ab151d2c2f214a7f7bb00cfe2d81698226bb72d8@ec2-34-230-231-71.compute-1.amazonaws.com:5432/dbuj3hhsofrf5f'
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


class User:

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<user: {self.username} added!>"


@app.route("/")
def index():

    books = db.execute("SELECT * FROM books LIMIT 50").fetchall()

    return render_template('index.html', books=books)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop('uid', None)
        username = request.form["username"]
        password = request.form["password"]

        # users = []
        # users.append(User(id=1, username="admin", password="admin"))

        Userz = db.execute(
            "SELECT * FROM users WHERE username=:username", {"username": username}).fetchall()
        for user in Userz:
            print(f"user: {user.id} | {user.username}")
            if user.username == username:
                return "username exist"
            if user.password == password:
                session['uid'] = user.id
                return "Login successful!"
            if not user.password == password:
                return "Password incorrect! please try again"

        return f"{username}? not found! recheck or register"
        return "d"
    return "invalid!"


# @app.route("/getBooks", methods=["GET", "POST"])
# def getBooks():
#     if request.method == "POST":
#         yearx = request.form['yearx']
#         yeary = request.form['yeary']

#         books = db.execute(
#             "SELECT * FROM books WHERE year BETWEEN :yearx AND :yeary", {"yearx": yearx, "yeary": yeary})

#         for book in books:

    # return book = book

    # return f'<tr> <td><a href="/single">{book.title}</a></td>
    # <td>Paul Innocent</td> <td>2000</td> <td>4.9</td> <td>4,000</td>
    # <td>012345678</td> </tr>'


# @app.before_request
# def before_request():
    # if 'uid' in session:
    # user=[x for x in users if x.id == #session['uid']][0]
    #g.user = user
