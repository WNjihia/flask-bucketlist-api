from flask import Blueprint, make_response, jsonify, request
from flask.views import MethodView

from bucketlist.models import Bucketlist, User, Item

api_blueprint = Blueprint('api', __name__)


class Bucketlist_View(MethodView):
    def post(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            user_id = User.decode_auth_token(auth_token)
            post_data = request.get_json()

            #  check if bucketlist exists
            if Bucketlist.query.filter_by(bucketlist_title=
                                          post_data.get('title'),
                                          creator_id=user_id).first():
                response = {
                        'status': 'fail',
                        'message': 'Bucketlist already exists!'
                        }
                return make_response(jsonify(response)), 401

            try:
                new_bucketlist = Bucketlist(
                                 bucketlist_title=post_data.get('title'),
                                 creator_id=user_id
                                 )
                # insert the bucketlist
                new_bucketlist.save()
                response = {
                            'status': 'success',
                            'message': 'Bucketlist {} has been added'
                            .format(post_data.get('title'))
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
                        'message': 'Please provide a valid auth token!'
                        }
            return make_response(jsonify(response)), 401

    def get(self, id=None):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            user_id = User.decode_auth_token(auth_token)

            if id:
                bucketlist = Bucketlist.query.filter_by(id=id, creator_id=
                                                        user_id).first()
                response = {
                            'id': bucketlist.id,
                            'title': bucketlist.bucketlist_title,
                            'date_created': bucketlist.date_created
                }
                return make_response(jsonify(response)), 200

            response = []
            bucketlists = Bucketlist.query.filter_by(creator_id=user_id)
            for bucketlist in bucketlists:
                info = {
                        'id': bucketlist.id,
                        'title': bucketlist.bucketlist_title,
                        'date_created': bucketlist.date_created
                }
                response.append(info)
            return make_response(jsonify(response)), 200
        else:
            response = {
                        'status': 'fail',
                        'message': 'Please provide a valid auth token!'
                        }
            return make_response(jsonify(response)), 401

    def put(self, id):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            user_id = User.decode_auth_token(auth_token)

            bucketlist = Bucketlist.query.filter_by(id=id,
                                                    creator_id=
                                                    user_id).first()
            if not bucketlist:
                response = {
                            'status': 'fail',
                            'message': 'Bucketlist does not exist!'
                            }
                return make_response(jsonify(response)), 404

            post_data = request.get_json()
            bucketlist.bucketlist_title = post_data.get('title')
            bucketlist.save()
            info = {
                    'id': bucketlist.id,
                    'title': bucketlist.bucketlist_title,
                    'date_created': bucketlist.date_created
                    }
            response = {
                        'status': 'success',
                        'message': info
                        }
            return make_response(jsonify(response)), 200
        else:
            response = {
                        'status': 'fail',
                        'message': 'Please provide a valid auth token!'
                        }
            return make_response(jsonify(response)), 401

    def delete(self, id):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            user_id = User.decode_auth_token(auth_token)
            bucketlist = Bucketlist.query.filter_by(id=id,
                                                    creator_id=
                                                    user_id).first()
            bucketlist.delete()
            response = {
                        'status': 'success',
                        'message': 'Bucketlist successfully deleted!'
                        }
            return make_response(jsonify(response)), 200
        else:
            response = {
                        'status': 'fail',
                        'message': 'Please provide a valid auth token!'
                        }
            return make_response(jsonify(response)), 401


class Items_View(MethodView):
    def post(self, bucketlist_id):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            user_id = User.decode_auth_token(auth_token)
            post_data = request.get_json()

            # check if bucketlist exists
            bucketlist = Bucketlist.query.filter_by(id=bucketlist_id, creator_id=user_id).first()
            if not bucketlist:
                response = {
                            'status': 'fail',
                            'message': 'Bucketlist not found!'
                            }
                return make_response(jsonify(response)), 404

            duplicate_item = Item.query.filter_by(item_name=post_data.get('name'),
                                                  bucketlist_id=bucketlist_id).first()
            if duplicate_item:
                response = {
                            'status': 'fail',
                            'message': 'Item alredy exists!'
                            }
                return make_response(jsonify(response)), 401

            new_item = Item(
                            item_name=post_data.get('name'),
                            description=post_data.get('description'),
                            bucketlist_id=bucketlist_id
                            )
            new_item.save()
            response = {
                        'status': 'success',
                        'message': 'Item {} has been added'
                        .format(post_data.get('name'))
                        }
            return make_response(jsonify(response)), 201
        else:
            response = {
                        'status': 'fail',
                        'message': 'Please provide a valid auth token!'
                        }
            return make_response(jsonify(response)), 401


add_bucket_view = Bucketlist_View.as_view('add_bucket_api')
add_item_view = Items_View.as_view('add_item_view')

# add rules for API endpoints
api_blueprint.add_url_rule(
    '/api/v1/bucketlists/',
    view_func=add_bucket_view,
    methods=['POST', 'GET']
)

api_blueprint.add_url_rule(
    '/api/v1/bucketlists/<int:id>/',
    view_func=add_bucket_view,
    methods=['GET', 'PUT', 'DELETE']
)

api_blueprint.add_url_rule(
    '/api/v1/bucketlists/<int:bucketlist_id>/items/',
    view_func=add_item_view,
    methods=['POST', 'GET']
)

api_blueprint.add_url_rule(
    '/api/v1/bucketlists/<int:bucketlists_id>/<int:items_id>/',
    view_func=add_item_view,
    methods=['GET', 'PUT', 'DELETE']
)
