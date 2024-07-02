from flask import Flask, jsonify
from dotenv import dotenv_values
from flask import Flask
from models import db


config = dotenv_values(".env")

app = Flask(__name__)
app.config["SECRET_KEY"] = config["APP_KEY"]


app.config["SQLALCHEMY_DATABASE_URI"] = config["DB_URI"]
db.init_app(app)

with app.app_context():
    db.create_all()


import routes
