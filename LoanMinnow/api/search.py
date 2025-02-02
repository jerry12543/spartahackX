import flask
from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from loanminnow.api.model import db, User, Venture, Pledge
from flask_login import login_required

search_blueprint = Blueprint('search', __name__)

from flask import Blueprint, request, jsonify
from flask_login import login_required
from sqlalchemy import or_
from loanminnow.api.model import User, Venture  # Adjust import paths based on your project structure

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/<string:query>', methods=['GET'])
@login_required
def search(query):
    q = query.strip()
    print("searching for", q)

    if not q:
        return jsonify({
            "users": [],
            "ventures": []
        })

    # Search for users by email
    users = User.query.filter(User.email.ilike(f"%{q}%")).all()

    # Search for ventures by name
    ventures = Venture.query.filter(Venture.name.ilike(f"%{q}%")).all()

    # Format users' results
    users_list = [{
        "id": user.id,
        "email": user.email
    } for user in users]

    # Format ventures' results
    ventures_list = [{
        "id": venture.id,
        "name": venture.name
    } for venture in ventures]

    print("found ", len(users), "users and", len(ventures), "ventures")

    return jsonify({
        "users": users_list,
        "ventures": ventures_list
    })