from celery import Celery
from celery.schedules import crontab
import json
from app.server.database.books import retrieve_book, retrieve_books
from app.server.database.borrowBooks import checkBook, add_borrow_book
from app.server.database.user import retrieve_user
from app.server.models.book import ResponseModel
import redis
r = redis.Redis(
    host='localhost',
    port='6379'
)


celery_app = Celery('tasks', broker="redis://localhost:6379/0")
celeryConfig = {
    "result_backend": "redis://localhost:6379/0"
}
celery_app.config_from_object(celeryConfig)

@celery_app.on_after_configure.connect
def get_books_periodic_task(sender, **kwargs):
    sender.add_periodic_task(300.0, get_books_task.s(), name="Get books.")

@celery_app.task
def get_books_task():
    books = json.dumps(retrieve_books())
    r.set('libraryAPI:books', books)

@celery_app.task(serializer='json')
def borrow_book_task(user_id, book_id):
    user_data = retrieve_user(user_id)
    book_data = retrieve_book(book_id)
    if checkBook(book_data["id"]):
        return { "message" : "This book already borrowed."}
    else:
        add_borrow_book(user_data, book_data)
        return ResponseModel("Book borrowed", "Book borrowed.")

