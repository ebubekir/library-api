from celery import Celery

from app.server.database.books import retrieve_book
from app.server.database.borrowBooks import checkBook, add_borrow_book
from app.server.database.user import retrieve_user
from app.server.models.book import ErrorResponseModel, ResponseModel

celery_app = Celery('tasks', broker="redis://localhost:6379/0")
celeryConfig = {
    "result_backend": "redis://localhost:6379/0"
}
celery_app.config_from_object(celeryConfig)
@celery_app.task(serializer='json')
def borrow_book_task(user_id, book_id):
    user_data = retrieve_user(user_id)
    book_data = retrieve_book(book_id)
    if checkBook(book_data["id"]):
        return { "message" : "This book already borrowed."}
    else:
        add_borrow_book(user_data, book_data)
        return ResponseModel("Book borrowed", "Book borrowed.")

