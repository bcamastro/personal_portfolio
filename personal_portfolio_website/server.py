from flask import Flask
from flask_app import app
from flask_app.controllers import controllers_users
from flask_app.controllers import controllers_blogs





if __name__ == "__main__":
    app.run(debug = True, port = 5002)