from main import app
from flask import jsonify, request, Blueprint
from models import Genre, db
from utilities import genre_to_dic

genres_bp = Blueprint('genres_bp', __name__)

@genres_bp.route("/", methods=["GET", "POST"])
def get_genres():
    if request.method == "POST":
        try:
            name = request.form["name"]
            genre_found = db.session.execute(db.select(Genre).filter_by(name=name)).scalar()
            if genre_found:
                return jsonify(error="This Genre already exists."), 403
            
            if not name:
                return jsonify(error="The name should not be empty"), 400

            new_genre = Genre(name=name)
            db.session.add(new_genre)
            db.session.commit()
            return jsonify(message="Genre added successfully")
        
        except Exception as e:
            return jsonify(error=str(e))
    try:
        genres = db.session.execute(db.select(Genre)).scalars().all()
        returned_genres = [genre_to_dic(genre) for genre in genres]
        return jsonify(genres=returned_genres)
    
    except Exception as e:
        return jsonify(error=str(e))
    

@genres_bp.route("/edit/<int:genre_id>", methods=["POST"])
def edit_genre(genre_id):
    try:
        genre_found = db.session.execute(db.select(Genre).filter_by(id=genre_id)).scalar()
        if not genre_found:
            return jsonify(error="Genre not found"), 404
        
        if not request.form["name"]:
            return jsonify(error="The name should not be empty"), 400

        genre_found.name = request.form["name"]
        db.session.commit()
        return jsonify(message="The genre was updated successfully")
    
    except Exception as e:
        return jsonify(error=str(e))

    
@genres_bp.route("/delete/<int:genre_id>", methods=["DELETE"])
def delete_genre(genre_id):
    try:
        genre_found = db.session.execute(db.select(Genre).filter_by(id=genre_id)).scalar()
        if not genre_found:
            return jsonify(error="The genre was not found"), 404
        
        db.session.delete(genre_found)
        db.session.commit()

        return jsonify(message="Genre deleted successfully")
    except Exception as e:
        return jsonify(error=str(e))


@genres_bp.route("/<int:genre_id>")
def get_genre_by_id(genre_id):
    try:
        genre_found = db.session.execute(db.select(Genre).filter_by(id=genre_id)).scalar()
        if not genre_found:
            return jsonify(error="The genre was not found"), 404
            
        return jsonify(genre=genre_to_dic(genre_found))
    except Exception as e:
        return jsonify(error=str(e))
