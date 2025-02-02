from flask import Blueprint, request, jsonify, redirect, url_for
from loanminnow.api.model import db, User
from flask_login import login_required, current_user
from loanminnow.api.routes import self_dashboard, other_dashboard

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/profile/<int:profile_id>/', methods=['GET'])
@users_blueprint.route('/profile/', methods=['GET'])
@login_required
def profile(profile_id=None):
    n = 20
    if not profile_id:
        print("apple")
        return redirect(url_for('users.profile', profile_id=current_user.id))
    if current_user.id == profile_id:
        print("banan")
        return self_dashboard(n)
    print("cherry")
    profile = User.query.get(profile_id)
    return other_dashboard(n, profile)
        