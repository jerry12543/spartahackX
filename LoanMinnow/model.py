from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    # A lender’s pledges and the payments they receive
    pledges = db.relationship('Pledge', backref='lender', lazy=True)
    payments = db.relationship('Payment', backref='lender', lazy=True)
    
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def total_paid_overdue(self):
        """
        Returns the total amount received in payments that were made after
        the associated venture’s due date.
        """
        return sum(payment.amount for payment in self.payments if payment.is_overdue)

    def current_overdue_amount(self):
        """
        Returns the current outstanding (unpaid) amount for ventures that are past due.
        This is computed by taking the total amount pledged for ventures whose due date
        has passed, minus the total payments already received for those ventures.
        """
        now = datetime.now(timezone.utc)
        total_pledged = sum(pledge.amount for pledge in self.pledges if pledge.venture.due_date < now)
        total_received = sum(payment.amount for payment in self.payments if payment.venture.due_date < now)
        # In case more money was repaid than pledged (should not happen), return at least 0.
        return max(total_pledged - total_received, 0)


class Venture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    goal = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)

    # One venture may have many pledges and payments.
    pledges = db.relationship('Pledge', backref='venture', lazy=True)
    payments = db.relationship('Payment', backref='venture', lazy=True)
    
    def __init__(self, name, description, goal, interest_rate, due_date):
        self.name = name
        self.description = description
        self.goal = goal
        self.interest_rate = interest_rate
        self.due_date = due_date



class Pledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    lender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    venture_id = db.Column(db.Integer, db.ForeignKey('venture.id'), nullable=False)

    def __init__(self, amount, lender_id, venture_id):
        self.amount = amount
        self.lender_id = lender_id
        self.venture_id = venture_id


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)

    lender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    venture_id = db.Column(db.Integer, db.ForeignKey('venture.id'), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, amount, lender_id, venture_id, payment_date=None):
        self.amount = amount
        self.lender_id = lender_id
        self.venture_id = venture_id
        if payment_date:
            self.payment_date = payment_date

    @property
    def is_overdue(self):
        """
        Returns True if this payment was made after the venture's due date.
        (You can also use this property in queries or for reporting.)
        """
        return self.payment_date > self.venture.due_date


def get_db():
    return db.session
