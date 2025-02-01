"""""loanminnow model (database)"""
from loanminnow import db
from flask_sqlalchemy import SQLAlchemy

# Example User model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

def get_db():
    """Open a new database connection"""
    return db.session()

def close_db():
    """Close the database connection"""
    return db.session.remove()