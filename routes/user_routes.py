from __init__ import login_manager
from flask import jsonify, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from models import User, db
from utilities import user_to_dict
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users_bp', __name__)

# GET ALL USERS
@users_bp.route("/", methods=["GET", "POST"])
def get_users():
    try:
        users = db.session.execute(db.select(User)).scalars().all()
        returned_users = [user_to_dict(user) for user in users]
        print(returned_users)
        return jsonify(users=returned_users)
    
    except Exception as e:
        return jsonify(error=str(e)), 500
    

@users_bp.route("/signup-user")
def add_new_user():
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

        login_user(new_user, remember=True)

        return jsonify(message="User registered successfully")
    except Exception as e:
        return jsonify(error=str(e)), 500
    

@users_bp.route("/login", methods=["POST"])
def login_a_user():
    try:
        email = request.form["email"]
        password = request.form["password"]

        user_found = db.session.execute(db.select(User).filter_by(email=email)).scalar()

        if user_found and check_password_hash(pwhash=user_found.password, password=password):
            login_user(user_found, remember=True)
            return jsonify(success={"message": "User logged in", "user": user_to_dict(user_found)})
        else:
            return jsonify(error="Invalid credentials"), 401

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
@login_required
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
@login_required
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


@users_bp.route("/logout")
@login_required
def logout_user_from_app():
    logout_user()
    return jsonify(message="User logged out.")