import os, requests

from flask import Flask, session, render_template, request, redirect, url_for
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
	
	if 'user_email' not in session:
		return render_template("index.html")
	return redirect(url_for('search'))
	
	# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "l7fl9mJYQXzlmikeRwJuhg", "isbns": "9781632168146"})
	# print(res.json())

@app.route("/login")
def login():
	return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('user_password', None)

    return redirect(url_for('login'))

@app.route("/search", methods=["POST", "GET"])
def search():
	if request.method == 'POST':		
		email = request.form.get("email")
		password = request.form.get("password")

		# Make sure user exists.
		if db.execute("SELECT * FROM users WHERE email = :email and password = :password", 
			{"email": email, "password": password}).rowcount == 0:
			return render_template("error.html", message="You need to register before!")

		# Save session user infos (id, email and password).
		user_row = db.execute("SELECT * FROM users WHERE email = :email AND password = :password", 
								{"email": email, "password": password}).fetchone()
		user_info = []
		for i in user_row:
			user_info.append(i)
		user_id = user_info[0]
		user_email = user_info[1]
		user_password = user_info[2]
		session["user_id"] = user_id
		session["user_email"] = user_email
		session["user_password"] = user_password
	elif request.method == 'GET' and 'user_email' not in session:
		return render_template("error.html", message="You need to register before!")

	return render_template("search.html", user_id = session["user_id"], user_email = session["user_email"])

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/registersuccess", methods=["POST"])
def registersuccess():
	email = request.form.get("email")
	password = request.form.get("password")
	db.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {"email": email, "password": password})
	db.commit()
	return redirect(url_for('login'))
	
	