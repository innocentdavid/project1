import os
import requests
from flask import Flask, session, redirect, render_template, session,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#from models import *

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


@app.route("/")
def index():
    return render_template('index.html')
