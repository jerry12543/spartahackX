""""This module contains the routes for user signup, login, and logout."""
from flask import Blueprint, request, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash
from loanminnow.model import db, User
from flask_login import login_user, login_required, logout_user
from flask import jsonify

# INCOMPLETE
# TODO: return values

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
        flash('All fields are required.', 'error')
        return jsonify({"error": "Missing required fields"}), 400 

    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already in use. Try logging in.', 'error')
        return jsonify({"error": "Email is already in use. Please log in or use a different email."}), 409

    new_user = create_user(name, email, password)

    # Log in the user automatically after signup
    login_user(new_user)

    flash('Signup successful! You are now logged in.', 'success')

    context = {
        "name": new_user.name,
        "email": new_user.email,
        "id": new_user.id
    }
    return  jsonify({"message": "User created successfully", "user": context}), 201


@auth_blueprint.route('/login/', methods=['POST'])
def login():
    """""Handle login form submission."""
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if not user or not (user.password == generate_password_hash(password)):
        flash('Invalid email or password.', 'error')
        return redirect(url_for('auth.login'))
    
    login_user(user)
    flash('Login successful!', 'success')
    return 403


@auth_blueprint.route('/logout/', methods=['POST'])
@login_required
def logout():
    """"Log out the current user."""
    logout_user()
    flash('You have been logged out.', 'success')
    return 200