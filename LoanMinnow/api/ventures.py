import flask
from flask import current_app
from flask_login import login_required, current_user
from loanminnow.api.model import db, Venture
from flask import Blueprint, request, jsonify
from flask import abort
import uuid
import pathlib
import os
import datetime

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
        "image_url": venture.image_url,
        "pledged_amount": sum(pledge.amount for pledge in venture.pledges),
    })


def save_image(fileobj):
    filename = fileobj.filename
    if len(fileobj.read()) == 0:
        print("ERROR: filesize is zero")
        return abort(400)
    fileobj.seek(0)
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"
    upload_path = current_app.config["UPLOAD_FOLDER"] / uuid_basename
    fileobj.save(upload_path)
    print(f"Saved image to {upload_path}")
    
    return uuid_basename

@venture_blueprint.route('/new/', methods=['POST', 'PATCH'])
@login_required
def update_venture():
    operation = request.form.get("operation")
    print(operation)
    if operation == "create":
        fileobj = request.files.get('image')
        if not fileobj:
            return jsonify({"error": "Image is required"}), 400
        
        uuid_basename = save_image(fileobj)

        # Get the additional fields from the form.
        name = request.form.get("name")
        description = request.form.get("description")
        goal = request.form.get("goal")
        interest_rate = request.form.get("interest_rate")
        due_date = datetime.datetime.strptime(request.form.get("due_date"), "%Y-%m-%d")

        venture = Venture(
            name=name,
            description=description,
            goal=goal,
            interest_rate=interest_rate,
            due_date=due_date,
            image_url=uuid_basename,
            owner=current_user,
        )
        db.session.add(venture)
        db.session.commit()
        return jsonify({"id": venture.id}), 201

    if operation == "update":
        venture_id = request.form["venture_id"]
        venture = Venture.query.get(venture_id)
        if not venture:
            return jsonify({"error": "Venture not found"}), 404
        fileobj = request.files.get("file")
        if fileobj:
            uuid_basename = save_image(fileobj)
            # Remove the old file if it exists.
            old_path = current_app.config["UPLOAD_FOLDER"] / venture.image_url
            if os.path.exists(old_path):
                os.remove(old_path)
            venture.image_url = uuid_basename
        # Update the other fields from the form (or keep the old value if not provided).
        venture.name = request.form.get("name", venture.name)
        venture.description = request.form.get("description", venture.description)
        venture.goal = request.form.get("goal", venture.goal)
        venture.interest_rate = request.form.get("interest_rate", venture.interest_rate)
        venture.due_date = datetime.datetime.strptime(int(request.form.get("due_date")), "%Y-%m-%d")
        db.session.add(venture)
        db.session.commit()
        return jsonify({"id": venture.id}), 200
    
    if operation == "delete":
        venture_id = request.form["venture_id"]
        venture = Venture.query.get(venture_id)
        if not venture:
            return jsonify({"error": "Venture not found"}), 404
        
        if venture.owner_id != current_user.id:
            return jsonify({"error": "Unauthorized"}), 403
        image_path = current_app.config["UPLOAD_FOLDER"] / venture.image_url
        if os.path.exists(image_path):
            os.remove(image_path)

        venture.delete()
        return jsonify({"id": venture.id}), 200
    
    return jsonify({"error": "Invalid operation"}), 400
