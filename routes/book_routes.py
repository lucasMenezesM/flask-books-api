from main import app
from flask import jsonify, request, Blueprint
from models import User, Book, Genre, db
from utilities import book_to_dict

books_bp = Blueprint('books_bp', __name__)

# ADD AND GET ALL BOOKS
@books_bp.route("/", methods=["POST", "GET"])
def get_all_books():

    # ADD A NEW BOOK
    if request.method == "POST":
        try:
            title = request.form["title"]
            author = request.form["author"]
            genre_id = request.form["genre_id"]
            user_id = request.form["user_id"]

            new_book = Book(title=title, author=author, genre_id= genre_id, user_id=user_id)

            db.session.add(new_book)
            db.session.commit()

            return jsonify(message="Book created.")
    
        except Exception as e:
            return jsonify(error=str(e)), 500
        
    # GET ALL BOOKS
    try:
        books = db.session.execute(db.select(Book)).scalars().all()
        books_list = [book_to_dict(book) for book in books]
    except Exception as e:
            return jsonify(error=str(e)), 500

    return jsonify(books=books_list)


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
def create_book(book_id):

    try:
        book = db.session.execute(db.select(Book).filter_by(id=book_id)).scalar()
        if not book:
            return jsonify(message="Book not found"), 404
        
        book.title = request.form["title"]
        book.author = request.form["author"]
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