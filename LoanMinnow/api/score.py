import math
from datetime import datetime, timezone
from sqlalchemy import func
from loanminnow.model import db, Pledge, Payment, Venture


def get_score():
    now = datetime.datetime(timezone.utc)

    # Current borrowed: sum of pledges for ventures that are not expired (due_date > now)
    current_borrowed = db.session.query(
        func.coalesce(func.sum(Pledge.amount), 0.0)
    ).join(Venture).filter(Venture.due_date > now).scalar()

    # Total borrowed: sum of all pledges
    total_borrowed = db.session.query(
        func.coalesce(func.sum(Pledge.amount), 0.0)
    ).scalar()

    # Current paid: sum of payments for ventures that are not expired
    current_paid = db.session.query(
        func.coalesce(func.sum(Payment.amount), 0.0)
    ).join(Venture).filter(Venture.due_date > now).scalar()

    # Total paid: sum of all payments
    total_paid = db.session.query(
        func.coalesce(func.sum(Payment.amount), 0.0)
    ).scalar()

    # For ventures whose due_date has passed (expired), get:
    expired_pledged = db.session.query(
        func.coalesce(func.sum(Pledge.amount), 0.0)
    ).join(Venture).filter(Venture.due_date <= now).scalar()
    
    expired_paid = db.session.query(
        func.coalesce(func.sum(Payment.amount), 0.0)
    ).join(Venture).filter(Venture.due_date <= now).scalar()

    # Current overdue: outstanding amount on expired ventures (if any)
    current_overdue = max(expired_pledged - expired_paid, 0)

    # Total paid overdue: sum of payments made after the due date (i.e. overdue payments)
    total_paid_overdue = db.session.query(
        func.coalesce(func.sum(Payment.amount), 0.0)
    ).join(Venture).filter(Payment.payment_date > Venture.due_date).scalar()

    # Total overdue (ever): overdue payments already made plus current overdue outstanding
    total_overdue = total_paid_overdue + current_overdue

    result = {
        'c_borrowed': current_borrowed,
        'borrowed': total_borrowed,
        'c_paid': current_paid,
        'paid': total_paid,
        'c_overdue': current_overdue,
        'overdue': total_overdue
    }

    return calculate_karma_score(result)


def calculate_karma_score(userinfo):
    c_borrowed = userinfo['c_borrowed'] # total of non expired loans
    c_paid = userinfo['c_paid']         # total of non expir
    c_overdue = userinfo['c_overdue']
    borrowed = userinfo['borrowed']
    paid = userinfo['paid']
    overdue = userinfo['overdue']

    # Calculate the karma score
    """
    - borrowing + paying back = +5% of loan
    - borrowing + never paying back = -50% of loan
    - borrowing + paying back late = -25% of loan
    - 40% current, 60% history
    - base score = 42
    - point increase/decrease proportional to loan amount
        - 1 = 100
        - 2 = 250
        - 3 = 625
        - 4 = 1562.5
        loan = 100 * 1.5^(score - 1)
    """
    base_score = 42
    current_score_factor = (abs(math.log(c_borrowed / 100, 1.5)) + 1)
    current_score = ((c_paid - c_overdue) / (c_borrowed * 0.85 + overdue * 2.5)) * 2 - 1
    history_score_factor = (abs(math.log(borrowed / 100, 1.5)) + 1)
    history_score = ((paid - overdue) / (borrowed + overdue * 2.5)) * 2 - 1
    score = base_score + 0.4 * current_score * current_score_factor + 0.6 * history_score * history_score_factor
    return score

