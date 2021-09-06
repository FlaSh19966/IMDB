
from flask import request, make_response, jsonify, Blueprint
from flask_restful import Resource, Api
from controller_movies import *
from flask_jwt_extended import get_jwt_identity, jwt_required

mv = Blueprint("movies", __name__)
api = Api(mv)


class GetMovieByName(Resource):
    @jwt_required
    def get(self, name):
        try:
            movie_cursor = get_movie_by_name(name)
            movie = []
            if movie_cursor["isRemoved"]:
                return make_response(jsonify({"MSG": "Movie was removed and no longer exists"}), 201)
            else:
                movie.append(movie_cursor)
                return make_response(jsonify(movie), 200)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class GetMoviesByDirector(Resource):
    @jwt_required
    def get(self, director):
        try:
            director_cursor = get_movies_by_director(director)
            movies = [movie for movie in director_cursor if movie["isRemoved"] is False]
            if bool(movies):
                return make_response(jsonify(movies), 200)
            else:
                return make_response(jsonify({"MSG": "No movies available"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class GetAllMovies(Resource):
    def get(self):
        try:
            movie_cursor = get_all_movies()
            movies = [movie for movie in movie_cursor if movie["isRemoved"] is False]
            return make_response(jsonify(movies), 200)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class AddMovie(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            if current_user["role"] == "ADMIN":
                movie = request.get_json()
                new_movie = {
                    "99popularity": movie["99popularity"],
                    "director": movie["director"],
                    "genre": movie["genre"],
                    "imdb_score": movie["imdb_score"],
                    "name": movie["name"],
                    "isRemoved": False
                }
                add_movie(new_movie)
                return make_response(jsonify({"MSG": "Movie added"}), 200)
            elif current_user["role"] == "NORMAL":
                return make_response(jsonify({"MSG": "Admin rights required"}), 403)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class RemoveMovie(Resource):
    @jwt_required
    def delete(self, name):
        try:
            current_user = get_jwt_identity()
            if current_user["role"] == "ADMIN":
                remove_movie(name)
                return make_response(jsonify({"MSG": "Movie removed"}), 200)
            elif current_user["role"] == "NORMAL":
                return jsonify({"MSG": "Admin rights required"}, 403)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class UpdateMovie(Resource):
    @jwt_required
    def put(self):
        try:
            current_user = get_jwt_identity()
            if current_user["role"] == "ADMIN":
                name = request.json.get("name")
                director = request.json.get("director")
                popularity = request.json.get("99popularity")
                imdb_score = request.json.get("imdb_score")
                update_movie(name, director, popularity, imdb_score)
                return make_response(jsonify({"MSG": "Update successful"}), 200)
            elif current_user["role"] == "NORMAL":
                return make_response(jsonify({"MSG": "Admin rights required"}), 403)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


api.add_resource(GetMovieByName, '/getmoviebyname/<string:name>')
api.add_resource(GetMoviesByDirector, '/getmoviesbydirector/<string:director>')
api.add_resource(GetAllMovies, '/getallmovies')
api.add_resource(AddMovie, '/addmovie')
api.add_resource(RemoveMovie, '/removemovie/<string:name>')
api.add_resource(UpdateMovie, '/updatemovie')
