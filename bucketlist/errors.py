from flask import Blueprint, make_response, jsonify

error_blueprint = Blueprint('bucketlist', __name__)


@error_blueprint.app_errorhandler(404)
def route_not_found(e):
    response = {
                'message': 'Not found'
                }
    return make_response(jsonify(response)), 404


@error_blueprint.app_errorhandler(405)
def method_not_found(e):
    response = {
                'message': 'Method not allowed'
                }
    return make_response(jsonify(response)), 405


@error_blueprint.app_errorhandler(500)
def internal_server_error(e):
    response = {
                'message': 'Internal server error'
                }
    return make_response(jsonify(response)), 500
