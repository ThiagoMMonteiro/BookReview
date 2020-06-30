import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR NOT NULL, password VARCHAR NOT NULL);")
print("Table 'users' created!")
db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, \
			publication_year INTEGER NOT NULL);")
print("Table 'books' created!")
db.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, rating VARCHAR NOT NULL, review VARCHAR, isbn VARCHAR NOT NULL, email VARCHAR NOT NULL);")
print("Table reviews created!")

db.commit() 