""""This module contains the routes for user signup, login, and logout."""
from flask import Blueprint, request, redirect, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from loanminnow.api.model import db, User
from flask_login import login_user, login_required, logout_user
from flask import jsonify


auth_blueprint = Blueprint('auth', __name__)

def create_user(username, email, password):
    """Create a new user with a securely hashed password."""
    hashed_password = generate_password_hash(password)
    new_user = User(name=username, email=email, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return new_user


@auth_blueprint.route('/signup/', methods=['POST'])
def signup():
    """"Handle signup form submission."""
    data = request.get_json()
    email = data["email"]
    name = data["name"]
    password = data["password"]

    if not email or not name or not password:
        return jsonify({"error": "Missing required fields"}), 400 

    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email is already in use. Please log in or use a different email."}), 409

    new_user = create_user(name, email, password)

    # Log in the user automatically after signup
    login_user(new_user)

    return jsonify({"message": "Login successful"}), 200


@auth_blueprint.route('/login/', methods=['POST'])
def login():
    """""Handle login form submission."""
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found, please sign up."}), 400
    if not check_password_hash(user.password, password):
        print(user.password)
        print(generate_password_hash(password))
        return jsonify({"error": "Invalid password, please try again."}), 409

    
    login_user(user)
    return jsonify({"message": "Login successful"}), 200


@auth_blueprint.route('/logout/', methods=['POST'])
@login_required
def logout():
    """"Log out the current user."""
    logout_user()
    return jsonify({"message": "Logout successful"}), 200
