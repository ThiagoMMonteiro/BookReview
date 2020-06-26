import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader)
    for isbn, title, author, publication_year in reader:
        db.execute("INSERT INTO books (isbn, title, author, publication_year) VALUES (:isbn, :title, :author, :publication_year)",
                    {"isbn": isbn, "title": title, "author": author, "publication_year": publication_year})
        print(f"Added book titled {title} to 'books' table.")
    db.commit()

if __name__ == "__main__":
    main()