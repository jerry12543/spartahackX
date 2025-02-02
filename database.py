from flask import Flask
from loanminnow.model import db, User, Venture, Pledge, Payment

# Initialize Flask App
app = Flask(__name__)

# Database Configuration - Change as needed
app.config.from_object('loanminnow.config')

# Bind database to Flask app
db.init_app(app)


def create_tables():
    """Creates all tables in the database."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

if __name__ == '__main__':
    create_tables()