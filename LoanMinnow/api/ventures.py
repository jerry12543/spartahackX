import flask
from loanminnow.api.model import Venture
from flask import Blueprint, request, jsonify

venture_blueprint = Blueprint('venture', __name__)

@venture_blueprint.route('/<int:venture_id>', methods=['GET'])
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


