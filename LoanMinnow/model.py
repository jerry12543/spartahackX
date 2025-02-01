"""LoanMinnow Model (Database)"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    total_received = db.Column(db.Float, default=0)
    total_owed = db.Column(db.Float, default=0)
    total_pledged = db.Column(db.Float, default=0)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password


class Project(db.Model):  # Added db.Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)  # Increased description length
    goal = db.Column(db.Float, nullable=False)  # Defined type for goal

    def __init__(self, name, description, goal):
        self.name = name
        self.description = description
        self.goal = goal


class Pledge(db.Model):  # Added db.Model
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Fixed foreign key
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)  # Fixed foreign key

    sender = db.relationship('User', backref='pledges')  # Optional: Add relationship
    project = db.relationship('Project', backref='pledges')

    def __init__(self, amount, sender_id, project_id):
        self.amount = amount
        self.sender_id = sender_id
        self.project_id = project_id


class Payment(db.Model):  # Added db.Model
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Fixed foreign key
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)  # Fixed foreign key

    receiver = db.relationship('User', backref='payments')  # Optional: Add relationship
    project = db.relationship('Project', backref='payments')

    def __init__(self, amount, receiver_id, project_id):
        self.amount = amount
        self.receiver_id = receiver_id
        self.project_id = project_id