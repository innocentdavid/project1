import os
import requests

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
            users.append(
                User(id=userr.id, username=userr.username, password=userr.password))

        for user in users:
            if user.id == session['user_id']:
                g.user = user


@app.route("/", methods=["GET", "POST"])
def index():
    if not g.user:
        return redirect(url_for('login'))

    books = db.execute(
        "SELECT * FROM books ORDER BY RANDOM() LIMIT 50").fetchall()

    return render_template('index.html', books=books)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        UserD = db.execute("SELECT * FROM users WHERE username = :username",{"username": username}).fetchall()
        if UserD:

            return render_template('register.html', e_msg="username already taken!")

        Nuser = db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
        db.commit()

        if Nuser:
            return redirect(url_for('login'))

        return "Something went wrong, try again"

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        UserD = db.execute("SELECT * FROM users").fetchall()

        for userr in UserD:
            users.append(
                User(id=userr.id, username=userr.username, password=userr.password))

        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

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
    uid = g.user.id
    
    books = db.execute("SELECT books.isbn, books.title FROM books INNER JOIN reviews ON books.id = reviews.bid WHERE reviews.uid = :uid ORDER BY reviews.id DESC", {"uid": uid}).fetchall()
    
    return render_template('profile.html', books=books)


@app.route("/book_search", methods=["GET", "POST"])
def book_search():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == "POST":
        keyword = request.form['search_keyword']

        books = db.execute(
            f"SELECT * FROM books where title LIKE '%{keyword}%' ORDER BY RANDOM() LIMIT 50").fetchall()

        if books:
            return render_template('index.html', books=books)

        books = db.execute(
            f"SELECT * FROM books where author LIKE '%{keyword}%' ORDER BY RANDOM() LIMIT 50").fetchall()

        if books:
            return render_template('index.html', books=books)

        books = db.execute(
            f"SELECT * FROM books where year::text LIKE '%{keyword}%' ORDER BY RANDOM() LIMIT 50").fetchall()

        if books:
            return render_template('index.html', books=books)

        books = db.execute(
            f"SELECT * FROM books where isbn::text LIKE '%{keyword}%' ORDER BY RANDOM() LIMIT 50").fetchall()

        if books:
            return render_template('index.html', books=books)

        return "<div style='display:flex; justify-content:center; align-items:center; height:95vh'><h1>BOOK NOT FOUND! <a href='/'>TRY AGAIN</a> </h1>"

    return redirect(url_for('index'))


@app.route('/api', methods=["GET", "POST"])
def api():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == "GET":
        isbn = request.args.get('isbn')
        
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "zEBi0HiQzdWXuFb9TodMQ", "isbns": f"{isbn}"})
        if res.status_code !=200:
            raise Exception("ERROR: API request failed!")
        data = res.json()
        
        totalReview = data["books"][0]['work_reviews_count']
        
        totalRating = data["books"][0]['work_ratings_count']
        
        avg_rating = data["books"][0]['average_rating']

        books = db.execute("SELECT * FROM books where isbn = :isbn", {"isbn": isbn}).fetchall()
        
        for book in books:
            bid = book.id
        
            reviews = db.execute("SELECT CAST(AVG(rating) AS DECIMAL(10,2)) avg_rating, COUNT(*) totalreview FROM reviews WHERE bid = :bid",{"bid": bid})
            
            for review in reviews:
                DtotalReview = review.totalreview
                Davg_rating = review.avg_rating

        if books:
            return render_template('api.html', books=books, totalReview=totalReview, totalRating=totalRating, avg_rating=avg_rating, DtotalReview=DtotalReview, Davg_rating=Davg_rating)
            
        return f'<div style="display:flex; justify-content:center; align-items:center; height:95vh"><h1>Hey <b style="color:blue;">{g.user.username}</b> stop playing with the url :) <a href="/">Go back</a></h1></div>'

    return redirect(url_for('index'))
    

@app.route('/review', methods=["GET", "POST"])
def review():
    if not g.user:
        return redirect(url_for(index))
        
    if request.method == "POST":
        bid = request.form['bid']
        uid = request.form['uid']
        comment = request.form['comment']
        try:
            rating = request.form['rating']
        except:
            rating = 0
    
        review = db.execute("SELECT * FROM reviews WHERE bid = :bid AND uid = :uid", {"bid": bid, "uid": uid}).fetchall()
        
        if review:
            # that is the user has reviewed the book before
            return "You have already reviewed this book"
          
        Nreview = db.execute("INSERT INTO reviews (bid, uid, rating, comment) VALUES (:bid, :uid, :rating, :comment)", {"bid": bid, "uid": uid, "rating": rating, "comment": comment})
        db.commit()
        
        if Nreview:
            return "reviewed"
  
    return redirect(url_for(index))


@app.route('/getReview', methods=("GET", "POST"))
def getReview():
    if request.method == "POST":
        bid = request.form['bid']
        
        reviews = db.execute(f"SELECT * FROM reviews WHERE bid = {bid} ORDER BY id LIMIT 10").fetchall()
        if reviews:
            for review in reviews:
                uid = review.uid
                
                users = db.execute("SELECT * FROM users WHERE id = :uid", {"uid": uid}).fetchall()
                
                return render_template("reviews.html", reviews=reviews, users=users)
        return "<center><h1>Be The First To Review This Book</h1></center>"
            
@app.route('/logout')
def logout():
    if g.user:
        session.pop('user_id', None)
        return redirect(url_for('login'))

    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run()