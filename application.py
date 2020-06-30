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

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/loginsuccess", methods=["POST"])
def loginsuccess():
	if request.method == 'POST':		
		email = request.form.get("email")
		password = request.form.get("password")

		# Make sure user exists.
		if db.execute("SELECT * FROM users WHERE email = :email and password = :password", 
			{"email": email, "password": password}).rowcount == 0:
			return render_template("error.html", message="Your data doesn't match or you need to register!")

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
		return redirect(url_for('search'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('user_password', None)
    # session.pop('user_search', None)

    return redirect(url_for('login'))

@app.route("/search", methods=["POST", "GET"])
def search():
	try_search = 0
	if request.method == 'POST' and 'user_email' in session:
		search_type = request.form.get("inlineRadioOptions")
		to_search = request.form.get("to_search")
		try_search = 1
		if search_type == 'isbn' and to_search is not "":
			user_search = db.execute("SELECT * FROM books WHERE isbn LIKE :to_search", 
								{"to_search": '%'+to_search+'%'}).fetchall()
			return render_template("search.html", user_id = session["user_id"], user_email = session["user_email"], user_search = user_search, try_search = try_search)
		elif search_type == 'title' and to_search is not "":
			user_search = db.execute("SELECT * FROM books WHERE title LIKE :to_search", 
								{"to_search": '%'+to_search+'%'}).fetchall()
			return render_template("search.html", user_id = session["user_id"], user_email = session["user_email"], user_search = user_search, try_search = try_search)	
		elif search_type == 'author' and to_search is not "":
			user_search = db.execute("SELECT * FROM books WHERE author LIKE :to_search", 
								{"to_search": '%'+to_search+'%'}).fetchall()
			return render_template("search.html", user_id = session["user_id"], user_email = session["user_email"], user_search = user_search, try_search = try_search)		
		else:
			return render_template("search.html", user_id = session["user_id"], user_email = session["user_email"], user_search = None, try_search = try_search)
			
	elif request.method == 'GET' and 'user_email' in session:
		return render_template("search.html", user_id = session["user_id"], user_email = session["user_email"], try_search = try_search)
	elif request.method == 'POST' and 'user_email' not in session:
		return render_template("error.html", message="You need to register or login (if you already have an account) to do a search!")
	else:
		return render_template("error.html", message="You must be logged in to perform a search")

@app.route("/book/<string:isbn>", methods=["POST", "GET"])
def book(isbn):
	isbn = isbn
	book_clicked = db.execute("SELECT * FROM books WHERE isbn = :isbn",
									{"isbn": isbn}).fetchall()

	reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn",
									{"isbn": isbn}).fetchall()

	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "l7fl9mJYQXzlmikeRwJuhg", "isbns": isbn})

	if request.method == 'POST':
		if db.execute("SELECT * FROM reviews WHERE email = :email and isbn = :isbn", 
			{"email": session["user_email"], "isbn": isbn}).rowcount == 0:
			rating = request.form.get("rating")
			review = request.form.get("review")
			db.execute("INSERT INTO reviews (rating, review, isbn, email) VALUES (:rating, :review, :isbn, :email)", 
						{"rating": rating, "review": review, "isbn": isbn, "email": session["user_email"]})
			db.commit()
		else:
			return render_template("book.html", user_id = session["user_id"], user_email = session["user_email"], book_clicked = book_clicked, reviews = reviews, res = res.json(), message = "Users cannot submit multiple reviews for the same book !!")

	if res:
		return render_template("book.html", user_id = session["user_id"], user_email = session["user_email"], book_clicked = book_clicked, reviews = reviews, res = res.json())
	else:
		res['books'][0]['average_rating'] = "goodreads does not have any reviews on this book"
		res['books'][0]['work_ratings_count'] = "goodreads does not have any reviews on this book"
		return render_template("book.html", user_id = session["user_id"], user_email = session["user_email"], book_clicked = book_clicked, reviews = reviews, res = res.json())
		
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
	
	