from flask import Blueprint, request, jsonify
from loanminnow.api.model import db, User
from flask_login import login_required, current_user
from loanminnow.api.routes import self_dashboard, other_dashboard

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/profile/<int:profile_id>/', methods=['GET'])
@login_required
def profile(profile_id):
    n = 20
    if current_user.id == profile_id:
        return self_dashboard(n)
    profile = User.query.get(profile_id)
    return other_dashboard(n, profile)
        