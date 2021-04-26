import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("localhost", 27017)
database = client.library
user_collection = database.get_collection("users")

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstname": user["firstname"],
        "lastname": user["lastname"]
    }

def retrieve_users():
    users = []
    for user in user_collection.find():
        users.append(user_helper(user))
    return users

def retrieve_user(id: str) -> dict:
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

def add_user(user_data: dict) -> dict:
    user = user_collection.insert_one(user_data)
    new_user = user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

def update_user(id: str, data: dict):
    if len(data) < 1:
        return False
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = user_collection.update_one({"_id":ObjectId(id)}, {"$set":data})
        if update_user:
            return True
        return False

def delete_user(id: str):
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user_collection.delete_one({"_id": ObjectId(id)})
        return True