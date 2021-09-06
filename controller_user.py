
from pymongo import MongoClient


uri = "mongodb+srv://m220student:m220password@mflix.ewyk5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db = MongoClient(uri)["sample_imdb"]


def find_all_user():
    return db.users.find({}, {"_id": 0})


def add_user(new_user):
    return db.users.insert_one(new_user)


def get_auth(email, password):
    return db.users.find_one({"email": email, "password": password})


def create_session(email, jwt):
    return db.sessions.insert_one({"email": email, "jwt": jwt})


def remove_session(email):
    return db.sessions.delete_one({"email": email})


def reset_password(email, new_password):
    return db.users.update_one({"email": email}, {"$set": {"password": new_password}})
