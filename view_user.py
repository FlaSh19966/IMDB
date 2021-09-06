
from flask import request, make_response, jsonify, Blueprint
from flask_restful import Resource, Api
from controller_user import *
import bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


usr = Blueprint("user", __name__)
api = Api(usr)


class SignUp(Resource):
    def post(self):
        try:
            user_info = request.get_json()
            # password = user_info["password"]
            # hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = {
                "name": user_info["name"],
                "email": user_info["email"],
                "password": user_info["password"],
                "isAdmin": False
            }
            add_user(new_user)
            return make_response(jsonify({"MSG": "Signup successful"}), 200)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class Login(Resource):
    def post(self):
        try:
            email = request.json.get("email")
            password = request.json.get("password")
            user_cursor = get_auth(email, password)
            if user_cursor:
                if user_cursor["isAdmin"]:
                    access_token = create_access_token(identity={"email": email, "role": "ADMIN"}, expires_delta=False)
                    create_session(email, access_token)
                    return make_response(jsonify({"Logged in as Admin Successful": access_token}), 200)
                else:
                    access_token = create_access_token(identity={"email": email, "role": "NORMAL"}, expires_delta=False)
                    create_session(email, access_token)
                    return make_response(jsonify({"Logged in as normal user Successful": access_token}), 200)
            else:
                return make_response(jsonify({"Invalid": "Credentials"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class Logout(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            remove_session(current_user["email"])
            return make_response(jsonify({"Logged": "out"}), 200)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class FindAllUser(Resource):
    @jwt_required
    def get(self):
        try:
            current_user = get_jwt_identity()
            if current_user["role"] == "ADMIN":
                alluser_cursor = find_all_user()
                users = [user for user in alluser_cursor]
                return make_response(users, 200)
            elif current_user["role"] == "NORMAL":
                return make_response(jsonify({"MSG": "Admin rights required"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


class ResetPassword(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            email = current_user["email"]
            retyped_password = request.json.get("password")
            new_password = request.json.get("new_password")
            user_cursor = get_auth(email, retyped_password)
            if user_cursor:
                reset_password(email, new_password)
                return make_response(jsonify({"MSG": "Password reset"}), 200)
            else:
                return make_response(jsonify({"MSG": "Credentials missing or invalid"}), 201)
        except Exception as e:
            return make_response(jsonify({"MSG": "Something went wrong", "Exception": str(e)}), 400)


api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(FindAllUser, '/allusers')
api.add_resource(ResetPassword, '/resetpassword')

