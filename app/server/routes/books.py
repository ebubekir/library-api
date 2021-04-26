from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database.borrowBooks import (
    checkBook,
    delete_borrow_book,
    get_borrowed_books
)
from app.server.database.books import (
    add_book,
    delete_book,
    retrieve_book,
    retrieve_books,
    update_book
)

from app.server.models.book import (
    ErrorResponseModel,
    ResponseModel,
    BookSchema,
    UpdateBookModel
)
from app.server.tasks import borrow_book_task

router = APIRouter()

@router.post("/add", response_description="Book data added into the database.")
async def add_book_data(book: BookSchema = Body(...)):
    book = jsonable_encoder(book)
    new_book = add_book(book)
    return ResponseModel(new_book, "Book added successfully.")

@router.get("/", response_description="Books retrieved")
def get_books():
    books = retrieve_books()
    if books:
        return ResponseModel(books, "Book data retrieved successfully.")
    return ResponseModel(books, "Empty list returned.")

@router.get("/detail/{id}", response_description="Book data retrieved")
async def get_book_data(id):
    book = retrieve_book(id)
    if book:
        return ResponseModel(book, "Book data retrieved successfully.")
    return ErrorResponseModel("An error occured. ", 404, "Book doesn't exist.")

@router.put("/update/{id}")
async def update_book_data(id, req: UpdateBookModel = Body(...)):
    req = {k : v  for k, v in req.dict().items() if v is not None}
    updated_book = update_book(id, req)
    if updated_book:
        return ResponseModel("Book with ID:{} name update is successful.".format(id), "Book name updated successfully,")
    return ErrorResponseModel("An error occured.", 404, "There was an error updating the book data.")

@router.delete("/delete/{id}", response_description="Book data deleted from the database.")
async def delete_book_data(id:str):
    deleted_book = delete_book(id)
    if deleted_book:
        return ResponseModel("Book with ID:{} removed.".format(id), "Book deleted successfully.")
    return ErrorResponseModel("An error occured.", 404, "Book with ID:{0} doesn't exist".format(id))

@router.post('/borrow/{user_id}/{book_id}', response_description="Borrow a book.")
async def borrow_book(user_id, book_id):
    borrow_book_task.delay(user_id, book_id)
    return ResponseModel("Task started", "Borrowed.")

@router.delete('/return/{book_id}', response_description="Return book to library.")
async def return_book(book_id):
    if checkBook(book_id):
        deleted_book = delete_borrow_book(book_id)
        if deleted_book:
            return ResponseModel("The book has been returned.", "The book has been returned")
        return ErrorResponseModel("An error occured.", 404, "The book could not be returned.")
    else:
        return ErrorResponseModel("This book is not on loan", 404, "This book is not on loan.")

@router.get('/borrowed', response_description="Get borrowed books.")
async def borrowed_book():
    books = get_borrowed_books()
    if books:
        return ResponseModel(books, "Books data retrieved successfully.")
    return ResponseModel(books, "Empty list returned.")