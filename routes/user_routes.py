from main import app
from flask import jsonify, request, Blueprint
from models import User, db
from utilities import user_to_dict
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users_bp', __name__)

@users_bp.route("/", methods=["GET", "POST"])
def get_users():

    # REGISTER A NEW USER
    if request.method == "POST":
        try:
            email = request.form["email"]
            name = request.form["name"]
            password = request.form["password"]

            if not email or not name or not password:
                return jsonify(error="The fields should not be empty"), 400
            
            user_found = db.session.execute(db.select(User).filter_by(email=email)).scalar()

            if user_found:
                return jsonify(error="Email already registered"), 400
            
            hashed_password = generate_password_hash(password=password)

            new_user = User(name=name, email=email, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            return jsonify(message="User registered successfully")
        except Exception as e:
            return jsonify(error=str(e)), 500

    # GET ALL USERS
    try:
        users = db.session.execute(db.select(User)).scalars().all()
        returned_users = [user_to_dict(user) for user in users]
        print(returned_users)
        return jsonify(users=returned_users)
    except Exception as e:
        return jsonify(error=str(e)), 500
    

# RETURN A USER BY ID
@users_bp.route("/<int:user_id>")
def get_user_by_id(user_id):

    try:
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
        
        if not user:
            return jsonify(error="User not found."), 404
        
        return jsonify(user=user_to_dict(user))
    except Exception as e:
        return jsonify(error=str(e))


@users_bp.route("/edit/<int:user_id>", methods=["POST"])
def edit_user(user_id):
    try:
        name = request.form["name"]
        email = request.form["email"]

        if not name or not email:
            return jsonify(error="The fields should not be empty"), 400

        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
        email_found = db.session.execute(db.select(User).filter_by(email=email)).scalar()

        if not user:
            return jsonify(error="User not found."), 404
        
        if user.email != email and email_found:
            return jsonify(error="This email is already in use"), 400
        
        user.name = name
        user.email = email

        if request.form["new_password"]:
            confirmed_password = check_password_hash(pwhash=user.password, password=request.form["confirm_password"])

            if confirmed_password:
                user.password = generate_password_hash(password=request.form["new_password"])
            else:
                return jsonify(error="Invalid password"), 401

        db.session.commit()
        return jsonify(message="User Updated")

    except Exception as e:
        return jsonify(error=str(e))


@users_bp.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
        if not user:
            return jsonify(error="User not found"), 404
        
        db.session.delete(user)
        db.session.commit()
        return jsonify(message="User Deleted Successfully")

    except Exception as e:
        return jsonify(error=str(e))
