from flask import Flask
from flask_sqlalchemy import flask_SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"]= False
app.config["SQLALCHEMY_DATABASE_URI"]='postgres://tibchumrwgmuym:767d5d8610d692050757f686ab151d2c2f214a7f7bb00cfe2d81698226bb72d8@ec2-34-230-231-71.compute-1.amazonaws.com:5432/dbuj3hhsofrf5f'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.column(db.integer, primary_key=True)
  username = db.column(db.String(120), unique=False)
  password = db.column(db.String(120), unique=False)
  
  def __init__(self, username, password):
    self.username = username
    self.password = password
	
if __name__ == '__main__':
  app.DEB6G= True
  db.create_all()
  
  
  import os

from flask import Flask, redirect, render_template, requests, session,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"]='postgres://tibchumrwgmuym:767d5d8610d692050757f686ab151d2c2f214a7f7bb00cfe2d81698226bb72d8@ec2-34-230-231-71.compute-1.amazonaws.com:5432/dbuj3hhsofrf5f'

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


class User:
  def __init__(self, username, password):
    self.username = username
    self.password = password
  
  def __repr__(self):
    return f"<user: {self.username}>"

users=[]
    
@app.route("/", method['GET', 'POST'])
def index():
  if request.method =='POST':
    session.pop('uid', None)
    username = request.form['username']
    password = request.form['password']
    
    user=[x for x in users if x.username == username][0]
    if user and user.password == password:
      session['uid'] = user.id
      return redirect(url_for('index'))
    
    return "G"
      
  return render_template('index.html')
