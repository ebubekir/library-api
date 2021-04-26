import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("localhost", 27017)
database = client.library
collection = database.get_collection("reservedBooks")
def borrowBookHelper(book) -> dict:
    return {
        "book_id": book["book"]["id"],
        "book_name": book["book"]["name"],
        "user_id": book["user"]["id"],
        "user_firstname": book["user"]["firstname"],
        "user_lastname": book["user"]["lastname"]
    }
def add_borrow_book(user_data: dict, book_data: dict) ->dict:
    data = {
        "user": {
            "id": user_data["id"],
            "firstname": user_data["firstname"],
            "lastname": user_data["lastname"]
        },
        "book": {
            "id": book_data["id"],
            "name": book_data["name"],
            "author": book_data["author"]
        }
    }
    reserve_book_data = collection.insert_one(data)
    new_reserve_book_data = collection.find_one({"_id": reserve_book_data.inserted_id})
    return new_reserve_book_data

def checkBook(book_id: str):
    for books in collection.find():
        if books["book"]["id"] == book_id:
            return True
    return False

def delete_borrow_book(book_id):
    id = ""
    for books in collection.find():
        if books["book"]["id"] == book_id:
           id = books["_id"]
    borrowed_book = collection.find_one({"_id": ObjectId(id)})
    if borrowed_book:
        collection.delete_one({"_id": ObjectId(id)})
        return True
def get_borrowed_books():
    books = []
    for book in collection.find():
        books.append(borrowBookHelper(book))
    return books