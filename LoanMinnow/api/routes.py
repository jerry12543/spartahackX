from flask import Blueprint, request, jsonify

api_blueprint = Blueprint('api', __name__)




@api_blueprint.route('/dashboard', methods=['GET']):
def dashboard():
    return jsonify({'message': 'Dashboard'})

@api_blueprint.route('/feed', methods=['GET']):
def feed():

