from flask import Blueprint, request, jsonify
from loanminnow.api.model import db, Pledge, Payment
from flask_login import require_login, current_user
import sqlalchemy


transactions = Blueprint('transactions', __name__)

@transactions.route('/projects/<int:project_id>', methods=['GET'])
@require_login
def get_project_transactions(project_id):
    pledges = db.session.query(Pledge).filter_by(project_id=project_id).all()
    payments = db.session.query(Payment).filter_by(project_id=project_id).all()
    return jsonify({"pledges":[pledge.serialize() for pledge in pledges], "payments": [payment.serialize() for payment in payments]})


def calculate_pledge_remaining(pledge):
    """
    Calculates the remaining amount to be repaid for a given pledge.
    This is computed as: pledge.amount - (sum of previous payments made
    by the pledge recipient to the pledge lender for the same venture).
    """
    # Find all payments made by the current recipient (pledge.recipient)
    # to this pledge's lender for this venture.
    payments = Payment.query.filter_by(
        payer_id=pledge.recipient_id,
        recipient_id=pledge.lender_id,
        venture_id=pledge.venture_id
    ).all()
    total_paid = sum(p.amount for p in payments)
    remaining = pledge.amount - total_paid
    return max(remaining, 0)


@transactions.route('/projects/<int:project_id>/repay/', methods=['POST'])
@require_login
def repay_project(project_id):
    """
    Endpoint for repaying pledges based on their remaining balance.
    
    Expected JSON payload:
        {
          "repay_amount": <amount to repay>
        }
    
    For each pledge associated with the given venture (and where the current
    user is the pledge recipient), the repayment is allocated using the formula:
    
        payment_amount = repay_amount * (pledge_remaining / total_remaining)
    
    where:
        - pledge_remaining is the remaining balance for that pledge, and
        - total_remaining is the sum of remaining balances for all pledges.
    """


@transactions.route('/outgoing/', methods=['GET'])
@require_login
def get_outgoing_transactions():
    type = request.args.get('type')
    if type == "pledge":
        pledges = db.session.query(Pledge).filter_by(lender_id=current_user.id).all()
        return jsonify([pledge.serialize() for pledge in pledges])
    if type == "payment":
        payments = db.session.query(Payment).filter_by(payer_id=current_user.id).all()
        return jsonify([payment.serialize() for payment in payments])    
    return jsonify({"error": "Invalid type"}), 400


@transactions.route('/incoming/', methods=['GET'])
@require_login
def get_incoming_transactions():
    type = request.args.get('type')
    if type == "pledge":
        pledges = db.session.query(Pledge).filter_by(recipient_id=current_user.id).all()
        return jsonify([pledge.serialize() for pledge in pledges])
    if type == "payment":
        payments = db.session.query(Payment).filter_by(recipient_id=current_user.id).all()
        return jsonify([payment.serialize() for payment in payments])    
    return jsonify({"error": "Invalid type"}), 400
