# Project 1 - Book Review

[![author](https://img.shields.io/badge/Author-thiagommonteiro-blue)](https://www.linkedin.com/in/thiago-m-monteiro/) 

Web Programming with Python and JavaScript

Hi! This is the second project (project1) of Web Programming with Python and Java Script course. Let's see a brief explanation of this project:

This project contain two folders with twenty files:

layout.html - layout.css

index.html - index.css

login.html - login.css

register.html - register.css

search.html - search.css

book.html - book.css

error.html - error.css

application.py

create.py

import.py

books.csv

requirements.txt

README.md

## Explaining layout.html - layout.css (briefly)

layout.html is the general layout of the website, being used in all other .html files to avoid duplicate code.

## Explaining index.html - index.css (briefly)

index.html is the first page of my website. Contains links to log in or register.

## Explaining login.html - login.css (briefly)

On this page we have the login form

## Explaining register.html - register.css (briefly)

On this page we have the register form

## Explaining search.html - search.css (briefly)

search.html is the website's home page and on it, as well as on other pages, it is possible to search for books, as long as the user is logged in.

## Explaining book.html - book.css (briefly)

When clicking on a book on the search page, the user is taken to this page where the details of the selected book can be found. In addition, here you can check the use of the external Goodreads API. On this same page, we have the functionality to add a review to a book.

## Explaining error.html - error.css (briefly)

Here we have a standard error page, where a message is provided through our python code, using flask and jinja2

## Explaining application.py (briefly)

This file contains practically the entire website backend. Using flask routes to navigate and use functions, in addition to database connection and login sessions

## Explaining create.py (briefly)

This file only helps to create tables faster and more organized in our database that is in Heroku

## Explaining import.py (briefly)

Program that will take the books from books.csv and import them into your PostgreSQL database

## Explaining books.csv (briefly)

file containing books and their details to be inserted into the database initially

## Explaining requirements.txt (briefly)

It contains some libraries needed to run the application. Due to some platforms, something may have been missing, if it does, you will only need to install the missing libraries.

[![Project 1 Explanation](http://img.youtube.com/vi/2AtpsNDbSho/0.jpg)](http://www.youtube.com/watch?v=2AtpsNDbSho "Project 1 Explanation")