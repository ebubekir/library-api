# library-api
Library API built with FastAPI
### Requirements
* FastAPI
* Uvicorn
* Pymongo
* Celery
### Install requirements via Requirements.txt
``
pip install -r requirements.txt
``
## Run app
`python app/main.py`

# Routes

## Books Routes
**GET** books/<br>
Get all the book information in the database.

**GET** books/detail/{book_id} <br>
Returns the details of a book.

**GET** books/borrowed<br>
List of borrowed books.

**POST** books/add/ <br>
Add book to the database.

**PUT** /books/update/{id} <br>
Updates the book information.

**DELETE** /books/delete/{id} <br>
Deletes the book from the database.

**POST** /books/borrow/{user_id}/{book_id} <br>
Borrow books from the library.

**DELETE** /books/return/{book_id} <br>
The book borrowed from the library is returned.

## Users Routes
**GET** users/<br>
Get all the users information in the database.

**GET** users/detail/{user_id} <br>
Returns the details of a user.

**POST** users/add/ <br>
Add user to the database.

**PUT** /users/update/{id} <br>
Updates the user information.

**DELETE** /users/delete/{id} <br>
Deletes the user from the database.
