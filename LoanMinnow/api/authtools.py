""""This module contains the routes for user signup, login, and logout."""
from flask import Blueprint, request, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash
from loanminnow.model import db, User
from flask_login import login_user, login_required, logout_user
import flask

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
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Check if user exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already in use. Try logging in.', 'error')
        return #TODO

    new_user = create_user(name, email, password)

    # Log in the user automatically after signup
    login_user(new_user)

    flash('Signup successful! You are now logged in.', 'success')
    return #TODO


@auth_blueprint.route('/login/', methods=['POST'])
def login():
    """""Handle login form submission."""
    email = request.form.get('email')
    password = request.form.get('password')

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