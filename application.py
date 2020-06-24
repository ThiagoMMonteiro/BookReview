import os, requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

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
	
	return render_template("index.html")
	# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "l7fl9mJYQXzlmikeRwJuhg", "isbns": "9781632168146"})
	# print(res.json())

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/registersuccess", methods=["POST"])
def registersuccess():
	email = request.form.get("email")
	password = request.form.get("password")
	db.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {"email": email, "password": password})
	db.commit()
	return render_template("login.html")
	
	