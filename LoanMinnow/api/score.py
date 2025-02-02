import math
from datetime import datetime, timezone
from sqlalchemy import func
from loanminnow.api.model import db, User


def get_score(user: User):
    """
    Calculate the karma score for a given user based on their borrowing and repayment history.
    
    This function uses the following logic:
      - current borrowed: sum of pledge amounts (where the user is the recipient)
        for ventures that have not yet expired (i.e. due_date > now)
      - total borrowed: sum of all pledge amounts (as recipient)
      - current paid: sum of payments received for ventures that have not yet expired
      - total paid: sum of all payments received
      - current overdue: the outstanding amount on expired ventures,
        calculated by the User.current_overdue_amount() method
      - total paid overdue: the sum of payments that were made after a venture’s due_date,
        as defined in Payment.is_overdue (summed via User.total_paid_overdue())
      
    Finally, these metrics are combined into a karma score using a weighted formula.
    """

    now = datetime.now(timezone.utc)

    # Pledges where the user is the recipient (i.e. borrowing)
    current_borrowed = sum(
        pledge.amount for pledge in user.recipients 
        if pledge.venture.due_date > now
    )
    total_borrowed = sum(pledge.amount for pledge in user.recipients)

    # Payments received by the user.
    current_paid = sum(
        payment.amount for payment in user.payments_received 
        if payment.venture.due_date > now
    )
    total_paid = sum(payment.amount for payment in user.payments_received)

    # Use the User model’s helper methods for overdue amounts.
    current_overdue = user.current_overdue_amount()
    total_paid_overdue = user.total_paid_overdue()
    total_overdue = total_paid_overdue + current_overdue

    # Build the dictionary of metrics
    stats = {
        'c_borrowed': current_borrowed,
        'borrowed': total_borrowed,
        'c_paid': current_paid,
        'paid': total_paid,
        'c_overdue': current_overdue,
        'overdue': total_overdue
    }

    return calculate_karma_score(stats)


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

