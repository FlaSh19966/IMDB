
from flask import Flask
from view_user import usr
from view_movies import mv
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

app.register_blueprint(usr)
app.register_blueprint(mv)


if __name__ == '__main__':
    app.run(debug=True)
