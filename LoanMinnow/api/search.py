import flask
from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from loanminnow.api.model import db, User, Venture, Pledge

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/<string:query>', methods=['GET'])
def search():
    q = request.args.get('q', '')

    if not q:
        return jsonify({
            "users": [],
            "ventures": [],
            "pledges": []
        })

    users = User.query.filter(or_(
        User.name.ilike(f"%{q}%"),
        User.email.ilike(f"%{q}%")
    )).all()

    ventures = Venture.query.filter(or_(
        Venture.name.ilike(f"%{q}%"),
        Venture.description.ilike(f"%{q}%")
    )).all()

    pledges = Pledge.query.join(User, Pledge.sender).join(Venture, Pledge.venture).filter(
        or_(
            User.name.ilike(f"%{q}%"),
            Venture.name.ilike(f"%{q}%")
        )
    ).all()

    users_list = [{
            "id": user.id,
            "email": user.email,
            "name": user.name,
        } for user in users]
    
    
    ventures_list = [{
        "id": venture.id,
        "name": venture.name,
        "description": venture.description,
        "goal": venture.goal,
        "interest_rate": venture.interest_rate,
        "due_date": venture.due_date.isoformat() if venture.due_date else None
    } for venture in ventures]

    
    pledges_list = [{
            "id": pledge.id,
            "amount": pledge.amount,
            "sender_id": pledge.sender_id,
            "venture_id": pledge.venture_id
        } for pledge in pledges]
    

    context = {
        "users": users_list,
        "ventures": ventures_list,
        "pledges": pledges_list
    }

    return jsonify(**context)
