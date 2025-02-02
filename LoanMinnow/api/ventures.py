import flask
from flask_login import login_required, current_user
from loanminnow.api.model import Venture
from flask import Blueprint, request, jsonify

venture_blueprint = Blueprint('venture', __name__)

@venture_blueprint.route('/<int:venture_id>', methods=['GET'])
@login_required
def get_venture(venture_id):
    venture = Venture.query.get(venture_id)
    if not venture:
        return jsonify({"error": "Venture not found"}), 404
    
    return jsonify({
        "id": venture.id,
        "name": venture.name,
        "description": venture.description,
        "goal": venture.goal,
        "interest_rate": venture.interest_rate,
        "due_date": venture.due_date.isoformat() if venture.due_date else None,
        "image_url": venture.image_url
    })

@venture_blueprint.route('/', methods=['POST'])
@login_required
def create_venture():
    target = '/users/'+flask.session.get("logname")+'/'

    data = request.get_json()
    venture = Venture(
        name=data['name'],
        description=data['description'],
        goal=data['goal'],
        interest_rate=data['interest_rate'],
        due_date=data['due_date'],
        image_url=data['image_url']
    )
    venture.save()
    return jsonify({"id": venture.id}), 201
