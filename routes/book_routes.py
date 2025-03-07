from main import app
from flask import jsonify, request, Blueprint
from models import User, Book, Genre, db
from utilities import book_to_dict
from datetime import datetime
from flask_login import login_required

books_bp = Blueprint('books_bp', __name__)

# GET ALL BOOKS
@books_bp.route("/", methods=["GET"])
def get_all_books():

    try:
        books = db.session.execute(db.select(Book)).scalars().all()
        books_list = [book_to_dict(book) for book in books]
    except Exception as e:
            return jsonify(error=str(e)), 500

    return jsonify(books=books_list)


@books_bp.route("/", methods=["POST"])
@login_required
def add_new_book():
    try:
        title = request.form["title"]
        author = request.form["author"]
        genre_id = request.form["genre_id"]
        user_id = request.form["user_id"]
        description = request.form["description"]

        if title and author:
            new_book = Book(title=title, author=author, genre_id= genre_id, user_id=user_id, description=description)
            db.session.add(new_book)
            db.session.commit()
        else:
            jsonify(error="author and title fields should not be empty."), 400

        return jsonify(message="Book created.")

    except Exception as e:
        return jsonify(error=str(e)), 500
    

# GET A BOOK BY ID
@books_bp.route("/<int:book_id>")
def get_book_by_id(book_id):
    try:
        book = db.session.execute(db.select(Book).filter_by(id=book_id)).scalar()
        if not book:
            return jsonify(error="Book Not Found"), 404
        else:
            return jsonify(book=book_to_dict(book))

    except Exception as e:
        return jsonify(error=str(e)), 500


# EDIT BOOK
@books_bp.route("/edit/<int:book_id>", methods=["POST"])
@login_required
def edit_book(book_id):
    try:
        book = db.session.execute(db.select(Book).filter_by(id=book_id)).scalar()
        if not book:
            return jsonify(message="Book not found"), 404
        
        title = request.form["title"]
        author = request.form["author"]
        
        if not title or not author:
            return jsonify(error="author and title fields should not be empty."), 400
        
        book.title = title
        book.author = author
        book.description = request.form["description"]
        book.genre_id = request.form["genre_id"]

        db.session.commit()

        return jsonify(message="Book Edited.")
    
    except Exception as e:
        return jsonify(error=str(e)), 500
    

# GET ALL BOOKS BY USER ID
@books_bp.route("/user/<int:user_id>")
def get_book_from_user(user_id):
    try:
        books = db.session.execute(db.select(Book).filter_by(user_id=user_id)).scalars().all()
        if not books:
            return jsonify(error="No Books Found"), 404
        
        returned_books = [book_to_dict(book) for book in books]

        return jsonify(books=returned_books)
    except Exception as e:
        return jsonify(error=str(e)), 500


# DELETE A BOOK BY ID
@books_bp.route("/delete/<int:book_id>", methods=["DELETE"])
@login_required
def delete_book(book_id):
    try:
        book = db.session.execute(db.select(Book).filter_by(id=book_id)).scalar()
        if not book:
            return jsonify(error="Book not found"), 404
        
        db.session.delete(book)
        db.session.commit()

        return jsonify(message="Book deleted"), 202
    
    except Exception as e:
        return jsonify(error=str(e)), 500


# QUERY A BOOK USING PARAMS
@books_bp.route("/query")
def query_books():
    title = request.args.get("title")
    genre = request.args.get("genre")
    author = request.args.get("author")

    try:
        books = db.session.execute(db.select(Book)).scalars().all()
        selected_books = []

        if title or genre or author:
            for book in books:
                if title:
                    if title.lower() in book.title.lower():
                        selected_books.append(book)
                        continue

                if genre:
                    if genre.lower() in book.genre.name.lower():
                        selected_books.append(book)
                        continue
                
                if author:
                    if author.lower() in book.author.lower():
                        selected_books.append(book)
                        continue
        else:
            selected_books = books


        returned_books = [book_to_dict(book) for book in selected_books]
        
        return jsonify(books=returned_books)
    
    except Exception as e:
        return jsonify(error=str(e)), 500