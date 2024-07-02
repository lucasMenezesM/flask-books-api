from main import app
from flask import jsonify
from models import User, Book, Genre, db


@app.route("/")
def home():
    return jsonify(message="First route is working")


