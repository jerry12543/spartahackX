from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import generate_password_hash

from config import Config
from model import db, User  # Import the db object and models

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Bind the SQLAlchemy instance to the app.
db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists. Please try again or log in.')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(email=email, name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login')
def login():
    return "Login page placeholder"

if __name__ == '__main__':
    # Create the database tables from the models.
    with app.app_context():
        db.create_all()
    app.run(debug=True)
