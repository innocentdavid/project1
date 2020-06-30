import os
# import requests
from flask import (
    Flask,
    session,
    g,
    redirect,
    request,
    render_template,
    url_for
)
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class UserC:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config["DEBUG"] = True

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


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

        UserD = db.execute(
            "SELECT * FROM users WHERE username = :username", {"username": username}).fetchall()

        
        for user in UserD:

            if user and user.password == password:
                session['uid'] = user.id
                g.user = user
                return "Login successful!"
            return "Password incorrect! please try again"
        return "username does not exist try again or register"
    return "invalid!"

# @ap.route("/single", methods["GET", "POST"])
