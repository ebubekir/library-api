import pymongo
from bson.objectid import ObjectId
import redis
import ast
client = pymongo.MongoClient("localhost", 27017)
database = client.library

book_collection = database.get_collection("books")
r = redis.Redis(
    host='localhost',
    port = '6379'
)

def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "name": book["name"],
        "author": book["author"]
    }

def retrieve_books():
    redis_data = r.get("libraryAPI:books")
    dict_str = redis_data.decode("UTF-8")
    books = ast.literal_eval(dict_str)
    return books

def add_book(book_data: dict) -> dict:
    book =  book_collection.insert_one(book_data)
    new_book =  book_collection.find_one({"_id": book.inserted_id})
    return book_helper(new_book)

def retrieve_book(id: str) -> dict:
    book =  book_collection.find_one({"_id": ObjectId(id)})
    if book:
        return book_helper(book)

def update_book(id: str, data: dict):
    if len(data) < 1:
        return False
    book =  book_collection.find_one({"_id": ObjectId(id)})
    if book:
        updated_book =  book_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_book:
            return True
        return False

def delete_book(id: str):
    book = book_collection.find_one({"_id":ObjectId(id)})
    if book:
        book_collection.delete_one({"_id":ObjectId(id)})
        return True

