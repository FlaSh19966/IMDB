
from pymongo import MongoClient


uri = "mongodb+srv://m220student:m220password@mflix.ewyk5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db = MongoClient(uri)["sample_imdb"]


def get_all_movies():
    return db.movies.find({}, {"_id": 0})


def get_movie_by_name(name):
    return db.movies.find_one({"name": name}, {"_id": 0})


def get_movies_by_director(director):
    return db.movies.find({"director": director}, {"_id": 0})


def add_movie(new_movie):
    return db.movies.insert_one(new_movie)


def update_movie(name, director, popularity, imdb_score):
    return db.movies.update_one(
            {"name": name, "director": director},
            {"$set": {"99popularity": popularity, "imdb_score": imdb_score}}
        )


def remove_movie(name):
    return db.movies.update_one({"name": name}, {"$set": {"isRemoved": True}})
