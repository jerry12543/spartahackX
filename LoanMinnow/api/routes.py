import flask
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import api.score
from loanminnow.api.model import db, User, Pledge, Venture
from sqlalchemy import func
from flask import abort


api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/', methods=['GET'])
def get_api_v1():
    """Return API resource URLs."""
    context = {
        'version': '1.0',
        'endpoints': {
            'dashboard': '/api/dashboard/',
            'feed': '/api/feed/',
            'venture': '/api/venture/',
            'pledge': '/api/pledge/',
            'payment': '/api/payment/',
        }
    }
    return flask.jsonify(**context)


@api_blueprint.route('/dashboard/', methods=['GET'])
@login_required
def dashboard():

    n = 3 # number of top supported and top created ventures to show

    user = current_user
    score = api.score.get_score(user)
    
    available_credits = user.available_credits

    credits_invested = sum(pledge.amount for pledge in user.pledges)

    top_supported = db.session.query(
        func.sum(Pledge.amount).label("total_amount_invested"), Venture
        ).join(
            Venture, Pledge.venture_id == Venture.id
        ).filter(
            Pledge.lender_id == user.id
        ).group_by(
            Venture.id
        ).order_by(
            func.sum(Pledge.amount).desc()
        ).limit(n).all()
    
    top_created = db.session.query(
        func.sum(Pledge.amount).label("total_amount_invested"), Venture
        ).join(
            Venture, Pledge.venture_id == Venture.id
        ).filter(
            Pledge.recipient_id == user.id
        ).group_by(
            Venture.id
        ).order_by(
            func.sum(Pledge.amount).desc()
        ).limit(n).all()

    top_supported_data = [
        {
            "venture_id": venture.id,
            "venture_name": venture.name,
            "total_amount_invested": total_amount_invested
        }
        for total_amount_invested, venture in top_supported
    ]
    top_created_data = [
        {
            "venture_id": venture.id,
            "venture_name": venture.name,
            "total_amount_invested": total_amount_invested
        }
        for total_amount_invested, venture in top_created
    ]

    context = {
        "score": score,
        "available_credits": available_credits,
        "credits_invested": credits_invested,
        "top_supported": top_supported_data,
        "top_created": top_created_data
    }
    return jsonify(**context)


@api_blueprint.route('/venture/newest/', methods=['GET'])
def get_newest_ventures():
    """
    Return the newest ventures (ordered by descending venture ID) with pagination.
    
    Query Parameters:
      - size: number of ventures to return (default: 10)
      - page: page number (default: 0)
      - ventureid_lte: upper bound on Venture.id (default: maximum id in table)
    """
    # Get query parameters
    size = request.args.get("size", default=10, type=int)
    page = request.args.get("page", default=0, type=int)
    max_venture_id = request.args.get("ventureid_lte", default=None, type=int)

    # Basic validation
    if size <= 0 or page < 0:
        abort(400, description="Invalid size or page parameter.")

    # If no max_venture_id is provided, get the maximum venture id available.
    if max_venture_id is None:
        max_venture_id = db.session.query(func.max(Venture.id)).scalar()
        if max_venture_id is None:
            # No ventures in the database.
            return jsonify(next="", results=[], url=request.full_path.rstrip('?'))

    # Query ventures with id <= max_venture_id, ordering by newest first.
    ventures_query = db.session.query(Venture).filter(
        Venture.id <= max_venture_id
    ).order_by(Venture.id.desc())
    
    ventures = ventures_query.limit(size).offset(page * size).all()

    # Determine the "next" link for pagination:
    if len(ventures) < size or len(ventures) == 0:
        next_link = ""
    else:
        # Use the id of the last venture in the current result as the new upper bound.
        next_max_id = ventures[-1].id
        next_link = (
            f"{request.path}?size={size}&page={page+1}&ventureid_lte={next_max_id}"
        )

    # Format the results. Adjust the fields as needed.
    results = [{
        "id": venture.id,
        "name": venture.name,
        "description": venture.description,
        "goal": venture.goal,
        "interest_rate": venture.interest_rate,
        "due_date": venture.due_date.isoformat(),
        "image_url": venture.image_url
    } for venture in ventures]

    context = {
        "next": next_link,
        "results": results,
        "url": request.full_path.rstrip('?')
    }
    return jsonify(**context)