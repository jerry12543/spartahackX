import flask
from flask import Blueprint, request, jsonify
import flask_login
from flask_login import login_required, current_user
import api.score
from model import db, User, Pledge, Venture
from sqlalchemy import func



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

# def get_posts():
#     size = flask.request.args.get("size", default=10, type=int)
#     maxpostid = flask.request.args.get("postid_lte", default=None, type=int)    

#     if not maxpostid:
#         connection = model.get_db()
#         cur = connection.execute(
#             """ SELECT MAX(postid) as maxpostid
#             FROM posts
#             ORDER BY postid DESC""")
#         maxpostid = cur.fetchone()["maxpostid"]
#     page = flask.request.args.get("page", default=0, type=int)
#     url = flask.request.full_path.rstrip('?')
#     return n_posts(size=size, maxpostid=maxpostid, page=page, url=url)



# def n_posts(size, maxpostid, page, url="/api/v1/posts/"):
#     """Return N newest post URLs and IDs."""
#     if size <= 0 or page < 0:
#         return flask.abort(400)
#     connection = model.get_db()
#     # Fetch the posts made by the user or by users they follow
#     cur = connection.execute(
#         """
#         SELECT p.postid
#         FROM posts AS p
#         WHERE p.postid <=
#         COALESCE(?, (SELECT MAX(postid) FROM posts))
#         AND
#         (p.owner = ?
#         OR p.owner IN (
#             SELECT username2 as username
#             FROM following
#             WHERE username1 = ?
#         ))
#         ORDER BY p.postid DESC
#         LIMIT ? OFFSET ?
#         """,
#         (maxpostid, model.User.name, model.User.name, size, page*size))

#     posts = cur.fetchall()
#     if len(posts) < size:
#         nxt = ""
#     else:
#         nxt = (f"/api/v1/posts/?size={size}"
#                f"&page={page+1}&postid_lte={str(maxpostid)}")
#         # posts[0]['postid']}")
#     if len(posts) == 0:
#         results = []
#     else:
#         results = [{
#             "postid": post["postid"],
#             "url": f"{flask.request.path}{post['postid']}/"
#         } for post in posts]

#     # Create the response context
#     context = {
#         "next": nxt,
#         "results": results,
#         "url": url
#     }

#     # Return the response as JSON
#     return jsonify(**context)
