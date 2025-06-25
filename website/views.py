from flask import Blueprint, jsonify

views = Blueprint('views', __name__)

@views.route('/api/test')
def api_home():
    return jsonify({"message": "Test"})