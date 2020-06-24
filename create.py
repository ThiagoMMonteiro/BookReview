import os

# from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR NOT NULL, password VARCHAR NOT NULL);")
print("Table 'users' created!")
# db.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, user VARCHAR NOT NULL, password VARCHAR NOT NULL")
# print("Table user created!")
# db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY, user VARCHAR NOT NULL, password VARCHAR NOT NULL")
# print("Table user created!")
db.commit() 