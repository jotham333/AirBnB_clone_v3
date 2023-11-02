#!/usr/bin/python3
""" Index module """

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Return a JSON object with the status of the API """
    return jsonify({"status": "OK"})

@app_views.route('api/v1/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Return a JSON object with the number of each objects """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
