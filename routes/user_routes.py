from main import app
from flask import jsonify, request, Blueprint
from models import User, db

users_bp = Blueprint('users_bp', __name__)
