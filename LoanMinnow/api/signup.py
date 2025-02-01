from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user
from werkzeug.security import generate_password_hash

from config import Config
from model import db, User, get_db, close_db  # Import our db object, models, and helper functions

app = Flask(__name__)
app.config

# Bind the SQLAlchemy instance to the app.
db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    session = get_db()
    return session.query(User).get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session = get_db()
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        # Check if the email already exists
        user = session.query(User).filter_by(email=email).first()
        if user:
            flash('Email address already exists. Please try again or log in.')
            return redirect(url_for('signup'))

        # Hash the password and create a new user instance
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(email=email, name=name, password=hashed_password)
        session.add(new_user)
        session.commit()

        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login')
def login():
    return "Login page placeholder"

# Teardown: close the database session after each request.
@app.teardown_appcontext
def shutdown_session(exception=None):
    close_db()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
