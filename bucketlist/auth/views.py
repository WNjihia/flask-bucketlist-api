from flask import Blueprint, make_response, jsonify, request
from flask.views import MethodView

from bucketlist import db
from bucketlist.models import User

auth_blueprint = Blueprint('auth', __name__)


class UserRegistration(MethodView):
    """User Registration Resource."""
    def post(self):
        # get the post data
        data_posted = request.get_json()
        # check if the user already exists
        user = User.query.filter_by(email=data_posted.get('email')).first()
        if not user:
            try:
                new_user = User(
                                username=data_posted.get('username'),
                                email=data_posted.get('email'),
                                password=data_posted.get('password')
                                )
                # insert the user
                db.session.add(new_user)
                db.session.commit()
                response = {
                            'status': 'success',
                            'message': 'You have been successfully registered'
                            }
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {
                            'status': 'fail' + str(e),
                            'message': 'Some error occurred. Please try again'
                            }
                return make_response(jsonify(response)), 401
        else:
            response = {
                        'status': 'fail',
                        'message': 'User already exists!'
                        }
            return make_response(jsonify(response)), 409


# add rules for API endpoints
auth_blueprint.add_url_rule(
    '/api/v1/auth/register',
    view_func=registration_view,
    methods=['POST']
)
