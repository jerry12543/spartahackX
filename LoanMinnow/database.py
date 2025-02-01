from flask import Flask
from model import db

# Initialize Flask App
app = Flask(__name__)

# Database Configuration - Change as needed
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///venture_funding.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind database to Flask app
db.init_app(app)


def create_tables():
    """Creates all tables in the database."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

if __name__ == '__main__':
    create_tables()