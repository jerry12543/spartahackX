# model.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    available_credits = db.Column(db.Float, default=0.0, nullable=False)
    
    # Relationships
    ventures_owned = db.relationship('Venture', back_populates='owner', lazy=True)
    pledges = db.relationship('Pledge', foreign_keys='Pledge.lender_id', back_populates='lender', lazy=True)
    recipients = db.relationship('Pledge', foreign_keys='Pledge.recipient_id', back_populates='recipient', lazy=True)
    payments = db.relationship('Payment', foreign_keys='Payment.payer_id', back_populates='payer', lazy=True)
    payments_received = db.relationship('Payment', foreign_keys='Payment.recipient_id', back_populates='recipient', lazy=True)

    def __init__(self, email, name, password, image_url=None, available_credits=0.0):
        self.email = email
        self.name = name
        self.password = password
        self.image_url = image_url
        self.available_credits = available_credits

    def total_paid_overdue(self):
        """Total payments received after the due date."""
        return sum(payment.amount for payment in self.payments_received if payment.is_overdue)

    def current_overdue_amount(self):
        """Outstanding amount for overdue ventures."""
        now = datetime.now(timezone.utc)
        total_pledged = sum(pledge.amount for pledge in self.recipients if pledge.venture.due_date < now)
        total_received = sum(payment.amount for payment in self.payments_received if payment.venture.due_date < now)
        return max(total_pledged - total_received, 0)


class Venture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    goal = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    # Relationships
    owner = db.relationship('User', back_populates='ventures_owned')
    pledges = db.relationship('Pledge', back_populates='venture', lazy=True)
    payments = db.relationship('Payment', back_populates='venture', lazy=True)
    interests = db.relationship('Interest', back_populates='venture')
    
    def __init__(self, name, description, goal, interest_rate, due_date, owner, image_url=None):
        self.name = name
        self.description = description
        self.goal = goal
        self.interest_rate = interest_rate
        self.due_date = due_date
        self.owner = owner
        self.image_url = image_url




class Pledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)

    lender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    venture_id = db.Column(db.Integer, db.ForeignKey('venture.id'), nullable=False)

    # Relationships
    lender = db.relationship('User', foreign_keys=[lender_id], back_populates='pledges')
    recipient = db.relationship('User', foreign_keys=[recipient_id], back_populates='recipients')
    venture = db.relationship('Venture', back_populates='pledges')

    def __init__(self, amount, lender, recipient, venture):
        self.amount = amount
        self.lender = lender
        self.recipient = recipient
        self.venture = venture


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    venture_id = db.Column(db.Integer, db.ForeignKey('venture.id'), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    payer = db.relationship('User', foreign_keys=[payer_id], back_populates='payments')
    recipient = db.relationship('User', foreign_keys=[recipient_id], back_populates='payments_received')
    venture = db.relationship('Venture', back_populates='payments')

    def __init__(self, amount, payer, recipient, venture, payment_date=None):
        self.amount = amount
        self.payer = payer
        self.recipient = recipient
        self.venture = venture
        if payment_date:
            self.payment_date = payment_date

    @property
    def is_overdue(self):
        """Returns True if payment was made after the venture's due date."""
        return self.payment_date > self.venture.due_date


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    venture_id = db.Column(db.Integer, db.ForeignKey('venture.id'), nullable=False)
    interest_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    venture = db.relationship('Venture', back_populates='interests')

    def __init__(self, amount, venture, interest_date=None):
        self.amount = amount
        self.venture = venture
        if interest_date:
            self.interest_date = interest_date


def get_db():
    return db.session
