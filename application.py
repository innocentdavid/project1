import os

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1000000, username='Anthony', password='password'))
users.append(User(id=2000000, username='Becca', password='secret'))
users.append(User(id=3000000, username='Carlos', password='somethingsimple'))


app = Flask(__name__)
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

app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        UserD = db.execute("SELECT * FROM users").fetchall()

        for userr in UserD:
            users.append(User(id=userr.id, username=userr.username, password=userr.password))

        for user in users:
            if user.id == session['user_id']:
                g.user = user
        
@app.route("/", methods=["GET", "POST"])
def index():
    if not g.user:
        return redirect(url_for('login'))

    books = db.execute("SELECT * FROM books LIMIT 50").fetchall()

    return render_template('index.html', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        print(users)
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')


@app.route("/book_search", methods=["GET", "POST"])
def book_search():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == "POST":
        keyword = request.form['search_keyword']

        books = db.execute(f"SELECT * FROM books where title LIKE '%{keyword}%' LIMIT 50").fetchall()

        if books:
            return render_template('index.html', books=books)

        books = db.execute(f"SELECT * FROM books where author LIKE '%{keyword}%' LIMIT 50").fetchall()

        if books:
            return render_template('index.html', books=books)

        books = db.execute(f"SELECT * FROM books where year LIKE '%{keyword}%' LIMIT 50").fetchall()

        if books:
            return render_template('index.html', books=books)

        
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    if g.user:
        session.pop('user_id', None)
        return redirect(url_for('login'))

    return redirect(url_for('login'))
