from flask import Blueprint, request, jsonify
from loanminnow.api.model import db, Pledge, Payment, Venture, Interest
from flask_login import login_required, current_user
from collections import defaultdict

transactions_blueprint = Blueprint('transactions', __name__)

@transactions_blueprint.route('/projects/<int:project_id>', methods=['GET'])
@login_required
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


@transactions_blueprint.route('/ventures/<int:venture_id>/pledge/', methods=['POST'])
@login_required
def pledge_to_venture(venture_id):
    """
    Pledges a given amount to a venture. The amount pledged is added to the recipient's
    outstanding balance for the venture. The pledger is the current user.

    Expected JSON payload:
        {
          "amount": <amount to pledge>
        }
    """
    data = request.get_json() or {}
    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid or missing lender_id or amount."}), 400

    if amount <= 0:
        return jsonify({"error": "Pledge amount must be positive."}), 400

    # Retrieve the venture from the database.
    venture = Venture.query.get(venture_id)
    if not venture:
        return jsonify({"error": "Venture not found."}), 404

    # (Optional) Check if the current user has sufficient credits to cover the pledge.
    if current_user.available_credits < amount:
        return jsonify({"error": "Insufficient funds to pledge that amount."}), 400

    try:
        # Deduct the pledge amount from the user's available credits.
        current_user.available_credits -= amount

        # Update the venture's pledged total (initialize to 0 if None).
        venture.total_pledged = (venture.total_pledged or 0) + amount

        # Create a new pledge record.
        pledge = Pledge(
            venture_id=venture_id,
            lender_id=current_user.id,  # using current_user instead of a passed lender_id
            amount=amount
        )
        db.session.add(pledge)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to process pledge", "details": str(e)}), 500

    return jsonify({
        "message": "Pledge successful.",
        "pledge": pledge.serialize(),  # Assuming Pledge has a serialize method.
        "new_balance": current_user.available_credits,
        "total_pledged": venture.total_pledged
    }), 200

@transactions_blueprint.route('/ventures/<int:venture_id>/repay/', methods=['POST'])
@login_required
def repay_venture(venture_id):
    """
    Repays a venture's debt—including accrued interest—in a weighted fashion.

    Expected JSON payload:
        {
          "repay_amount": <amount to repay>
        }

    The total amount due is computed as:
       total_due = (total principal remaining across all pledges) + (total accrued interest)
       
    For each lender (i.e. each group of pledges by the same lender), we compute:
       - principal_remaining: the outstanding principal (pledged amount minus previous principal payments)
       - lender_interest_due: this lender’s share of the total accrued interest, computed as:
             
             lender_interest_due = (principal_remaining / total_principal_remaining) * total_accrued_interest

       - lender_total_due = principal_remaining + lender_interest_due

    The repayment amount (capped at total_due) is then allocated proportionally among lenders.
    For each lender the allocated repayment is split so that interest is repaid first and any
    remaining amount goes toward reducing principal.

    As interest is repaid, the corresponding Interest records (ordered by interest_date) are reduced
    (or deleted if fully repaid).
    """
    data = request.get_json() or {}
    try:
        repay_amount = float(data.get("repay_amount", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid or missing repay_amount."}), 400

    if repay_amount <= 0:
        return jsonify({"error": "repay_amount must be greater than zero."}), 400

    venture = Venture.query.get(venture_id)
    if not venture:
        return jsonify({"error": "Venture not found."}), 404

    # Ensure the current user is the recipient (i.e. the borrower) for this venture.
    pledges = [pledge for pledge in venture.pledges 
               if pledge.recipient_id == current_user.id and pledge.venture_id == venture_id]
    if not pledges:
        return jsonify({"error": "You are not authorized to repay pledges for this venture."}), 403

    # --- 1. Group pledges by lender and compute outstanding principal ---
    lender_groups = defaultdict(list)
    for pledge in pledges:
        lender_groups[pledge.lender_id].append(pledge)

    lender_principal_remaining = {}   # per lender: outstanding principal
    total_principal_remaining = 0.0
    for lender_id, pledge_list in lender_groups.items():
        # Total pledged amount from this lender:
        total_pledged = sum(pledge.amount for pledge in pledge_list)
        # Sum all previous payments made by current_user to this lender for this venture.
        payments = Payment.query.filter_by(
            payer_id=current_user.id,
            recipient_id=lender_id,
            venture_id=venture.id
        ).all()
        total_paid = sum(p.amount for p in payments)
        remaining = total_pledged - total_paid
        if remaining > 0:
            lender_principal_remaining[lender_id] = remaining
            total_principal_remaining += remaining

    if total_principal_remaining <= 0:
        return jsonify({"error": "All pledges are already fully repaid."}), 400

    # --- 2. Calculate total accrued interest for the venture ---
    interest_records = Interest.query.filter_by(venture_id=venture.id).order_by(Interest.interest_date).all()
    total_accrued_interest = sum(ir.amount for ir in interest_records)

    # Total due is the sum of principal and accrued interest.
    total_due = total_principal_remaining + total_accrued_interest

    # Cap the repayment amount to the total due, if necessary.
    if repay_amount > total_due:
        repay_amount = total_due

    if current_user.available_credits < repay_amount:
        return jsonify({"error": "Insufficient funds."}), 400

    payments_info = []

    # --- 3. Allocate repayment among lenders ---
    for lender_id, principal_remaining in lender_principal_remaining.items():
        # Calculate this lender's share of the total accrued interest.
        lender_interest_due = ((principal_remaining / total_principal_remaining) *
                               total_accrued_interest) if total_principal_remaining > 0 else 0
        lender_total_due = principal_remaining + lender_interest_due

        # Determine this lender's proportional weight.
        weight = lender_total_due / total_due
        lender_payment = repay_amount * weight

        # --- 4. Split the lender's allocated repayment into interest vs. principal ---
        if lender_payment <= lender_interest_due:
            # Entire repayment goes to interest.
            interest_repaid = lender_payment
            principal_repaid = 0.0
        else:
            interest_repaid = lender_interest_due
            principal_repaid = lender_payment - lender_interest_due
            # Ensure we never repay more principal than is owed.
            if principal_repaid > principal_remaining:
                principal_repaid = principal_remaining
                interest_repaid = lender_payment - principal_remaining

        # Create a Payment record (recording the total amount repaid to this lender).
        lender = lender_groups[lender_id][0].lender  # retrieve the lender object
        payment = Payment(
            amount=lender_payment,
            payer=current_user,
            recipient=lender,
            venture=venture
        )
        db.session.add(payment)
        # Update lender's available credits (they receive the repayment).
        lender.available_credits += lender_payment

        payments_info.append({
            "lender_id": lender_id,
            "payment_total": lender_payment,
            "interest_repaid": interest_repaid,
            "principal_repaid": principal_repaid,
            "principal_remaining_before": principal_remaining,
            "interest_due_before": lender_interest_due
        })

        # --- 5. Update Interest records by deducting the interest repaid ---
        remaining_interest_to_deduct = interest_repaid
        for ir in interest_records:
            if remaining_interest_to_deduct <= 0:
                break
            if ir.amount <= remaining_interest_to_deduct:
                remaining_interest_to_deduct -= ir.amount
                db.session.delete(ir)
            else:
                ir.amount -= remaining_interest_to_deduct
                remaining_interest_to_deduct = 0

    # Deduct the total repayment from the current user's available credits.
    current_user.available_credits -= repay_amount
    db.session.commit()

    return jsonify({
        "message": "Repayment successful.",
        "total_repaid": repay_amount,
        "payments": payments_info
    }), 200

@transactions_blueprint.route('/outgoing/', methods=['GET'])
@login_required
def get_outgoing_transactions():
    type = request.args.get('type')
    if type == "pledge":
        pledges = db.session.query(Pledge).filter_by(lender_id=current_user.id).all()
        return jsonify([pledge.serialize() for pledge in pledges])
    if type == "payment":
        payments = db.session.query(Payment).filter_by(payer_id=current_user.id).all()
        return jsonify([payment.serialize() for payment in payments])    
    return jsonify({"error": "Invalid type"}), 400


@transactions_blueprint.route('/incoming/', methods=['GET'])
@login_required
def get_incoming_transactions():
    type = request.args.get('type')
    if type == "pledge":
        pledges = db.session.query(Pledge).filter_by(recipient_id=current_user.id).all()
        return jsonify([pledge.serialize() for pledge in pledges])
    if type == "payment":
        payments = db.session.query(Payment).filter_by(recipient_id=current_user.id).all()
        return jsonify([payment.serialize() for payment in payments])    
    return jsonify({"error": "Invalid type"}), 400
