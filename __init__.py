from flask import Flask, jsonify
from dotenv import dotenv_values
from flask import Flask
from models import db, User
from flask_login import LoginManager

config = dotenv_values(".env")

app = Flask(__name__)
app.config["SECRET_KEY"] = config["APP_KEY"]


app.config["SQLALCHEMY_DATABASE_URI"] = config["DB_URI"]
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).filter_by(id=user_id)).scalar()


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(error="Unauthorized"), 401

with app.app_context():
    db.create_all()


from routes.user_routes import users_bp 
from routes.book_routes import books_bp
from routes.genre_routes import genres_bp

app.register_blueprint(books_bp, url_prefix='/api/book')
app.register_blueprint(users_bp, url_prefix='/api/user')
app.register_blueprint(genres_bp, url_prefix='/api/genre')
