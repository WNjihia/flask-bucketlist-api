import re

from flask import Blueprint, make_response, jsonify, request
from flask.views import MethodView

from bucketlist.models import Bucketlist, User, Item

api_blueprint = Blueprint('api', __name__)


def response_for_updates_with_same_data():
    response = {
            'status': 'fail',
            'message': 'No updates detected'
            }
    return make_response(jsonify(response)), 409


def validate_token(self):
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        user_id = User.decode_auth_token(auth_token)
        return user_id


def validate_input_format(name):
    check_name = re.match('^[ a-zA-Z0-9_.-]+$', name)
    if check_name is None:
        return True
    elif len(name.strip(" ")) == 0:
        return True


class Bucketlist_View(MethodView):
    """
    Contains methods for BucketList Resource
    """
    def post(self):
        """
        Method: `POST`
        Create a bucketlist.
        `URL` path: `/api/v1/bucketlists/`
        """

        # validate token
        user_id_response = validate_token(request)
        if user_id_response is None:
            response = {
                                'status': 'fail',
                                'message': 'Please provide a valid auth token!'
                                }
            return make_response(jsonify(response)), 401

        post_data = request.get_json()

        #  check if bucketlist exists
        if Bucketlist.query.filter_by(bucketlist_title=
                                      post_data.get('title'),
                                      creator_id=user_id_response).first():
            response = {
                    'status': 'fail',
                    'message': 'Bucketlist already exists!'
                    }
            return make_response(jsonify(response)), 409

        # check if title format is valid
        if validate_input_format(post_data.get('title')):
            response = {
                        'status': 'fail',
                        'message': 'Invalid bucketlist title!'
                        }
            return make_response(jsonify(response)), 400

        try:
            new_bucketlist = Bucketlist(
                             bucketlist_title=post_data.get('title'),
                             creator_id=user_id_response
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
            return make_response(jsonify(response)), 500

    def get(self, id=None):
        """
        Method: `GET`
        Retrieve all bucketlists or a single bucketlist
        `URL` path: `/api/v1/bucketlists/` or
        `/api/v1/bucketlists/<bucketlist_id>/`
        """

        # validate token
        user_id_response = validate_token(request)
        if user_id_response is None:
            response = {
                                'status': 'fail',
                                'message': 'Please provide a valid auth token!'
                                }
            return make_response(jsonify(response)), 401

        if id:
            # retrieve a bucketlist
            bucketlist = Bucketlist.query.filter_by(id=id, creator_id=
                                                    user_id_response).first()
            if not bucketlist:
                response = {
                            'status': 'fail',
                            'message': 'Bucketlist cannot be found'
                            }
                return make_response(jsonify(response)), 404

            if not bucketlist.items:
                items = {}
            else:
                item_data = []
                # make items JSON serializable
                for item in bucketlist.items:
                    items = {
                            "item_id": item.id,
                            "item_name": item.item_name,
                            "item_description": item.description
                            }
                    item_data.append(items)
            response = {
                        'id': bucketlist.id,
                        'title': bucketlist.bucketlist_title,
                        'date_created': bucketlist.date_created,
                        'items': items
            }
            return make_response(jsonify(response)), 200

        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=20, type=int)
        search = request.args.get("q", type=str)
        response = []
        items = []

        if search:
            # implement search in query
            bucketlists = Bucketlist.query \
                          .filter_by(creator_id=user_id_response) \
                          .filter(Bucketlist.bucketlist_title
                                  .ilike('%' + search + '%')).paginate(
                                  page, limit, False)
        else:
            bucketlists = Bucketlist.query.filter_by(creator_id=
                                                     user_id_response) \
                          .paginate(page, limit, False)

        page_count = bucketlists.pages

        # add next and previous url links
        if bucketlists.has_next:
            next_page = request.url_root + 'api/v1/bucketlists' + \
                        '?limit=' + str(limit) + \
                        '&page=' + str(page + 1)
        else:
            next_page = 'None'
        if bucketlists.has_prev:
            prev_page = request.url_root + 'api/v1/bucketlists' + \
                        '?limit=' + str(limit) + \
                        '&page=' + str(page - 1)
        else:
            prev_page = 'None'

        for bucketlist_entry in bucketlists.items:
            item_data = []
            if bucketlist_entry.items:
                # make items JSON serializable
                for item in bucketlist_entry.items:
                    items = {
                            "item_id": item.id,
                            "item_name": item.item_name,
                            "item_description": item.description
                            }
                    item_data.append(items)

            info = {
                    'id': bucketlist_entry.id,
                    'title': bucketlist_entry.bucketlist_title,
                    'date_created': bucketlist_entry.date_created,
                    'items': item_data
            }
            response.append(info)

        meta_data = {'meta_data': {'next_page': next_page,
                                   'previous_page': prev_page,
                                   'total_pages': page_count
                                   }}
        response.append(meta_data)
        return make_response(jsonify(response)), 200

    def put(self, id):
        """
        Method: `PUT`
        Update a bucketlist
        `URL` path: `/api/v1/bucketlists/<bucketlist_id>/`
        """
        # validate token
        user_id_response = validate_token(request)
        if user_id_response is None:
            response = {
                                'status': 'fail',
                                'message': 'Please provide a valid auth token!'
                                }
            return make_response(jsonify(response)), 401

        # get the bucketlist
        bucketlist = Bucketlist.query.filter_by(id=id,
                                                creator_id=
                                                user_id_response).first()
        if not bucketlist:
            response = {
                        'status': 'fail',
                        'message': 'Bucketlist does not exist!'
                        }
            return make_response(jsonify(response)), 404

        post_data = request.get_json()

        # check if title format is valid
        if validate_input_format(post_data.get('title')):
            response = {
                        'status': 'fail',
                        'message': 'Invalid bucketlist title!'
                        }
            return make_response(jsonify(response)), 400

        # check for updates
        if post_data.get('title') == bucketlist.bucketlist_title:
            return response_for_updates_with_same_data()

        bucketlist.bucketlist_title = post_data.get('title')
        bucketlist.save()

        info = {
                'id': bucketlist.id,
                'title': bucketlist.bucketlist_title,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
                }
        response = {
                    'status': 'success',
                    'message': info
                    }
        return make_response(jsonify(response)), 200

    def delete(self, id):
        """
        Delete a bucketlist
        `URL` path: `/api/v1/bucketlists/<bucketlist_id>/`
        """
        # validate token
        user_id_response = validate_token(request)
        if user_id_response is None:
            response = {
                                'status': 'fail',
                                'message': 'Please provide a valid auth token!'
                                }
            return make_response(jsonify(response)), 401

        # retrieve bucketlist
        bucketlist = Bucketlist.query.filter_by(id=id,
                                                creator_id=
                                                user_id_response).first()
        # check if bucketlist exists
        if not bucketlist:
            response = {
                        'status': 'success',
                        'message': 'Bucketlist cannot be found'
                        }
            return make_response(jsonify(response)), 404

        bucketlist.delete()

        response = {
                    'status': 'success',
                    'message': 'Bucketlist successfully deleted!'
                    }
        return make_response(jsonify(response)), 200


class Items_View(MethodView):
    def post(self, bucketlist_id):
        """
        Method: `POST`
        Create a bucketlist item.
        `URL` path: `/api/v1/bucketlists/<bucketlist_id>/items/`
        """
        # validate token
        user_id_response = validate_token(request)
        if user_id_response is None:
            response = {
                                'status': 'fail',
                                'message': 'Please provide a valid auth token!'
                                }
            return make_response(jsonify(response)), 401

        post_data = request.get_json()

        # check if bucketlist exists
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id,
                                                creator_id=
                                                user_id_response).first()
        if not bucketlist:
            response = {
                        'status': 'fail',
                        'message': 'Bucketlist not found!'
                        }
            return make_response(jsonify(response)), 404

        # check if item already exists
        duplicate_item = Item.query.filter_by(item_name=
                                              post_data.get('name'),
                                              bucketlist_id=
                                              bucketlist_id).first()
        if duplicate_item:
            response = {
                        'status': 'fail',
                        'message': 'Item already exists!'
                        }
            return make_response(jsonify(response)), 409

        # check if title format is valid
        if validate_input_format(post_data.get('name')):
            response = {
                        'status': 'fail',
                        'message': 'Invalid name format'
                        }
            return make_response(jsonify(response)), 400

        # insert item
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

    def get(self, bucketlist_id, item_id=None):
        """
        Method: `GET`
        Retrieve all bucketlist items or a single bucketlist item.
        `URL` path: `/api/v1/bucketlists/<bucketlist_id>/items/` or
        `/api/v1/bucketlists/<bucketlist_id>/items/<item_id>`
        """
        # validate token
        user_id_response = validate_token(request)
        if user_id_response is None:
            response = {
                                'status': 'fail',
                                'message': 'Please provide a valid auth token!'
                                }
            return make_response(jsonify(response)), 401

        # check if bucketlist exists
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id,
                                                creator_id=
                                                user_id_response).first()
        # check if bucketlist exists
        if not bucketlist:
            response = {
                        'status': 'fail',
                        'message': 'Bucketlist not found!'
                        }
            return make_response(jsonify(response)), 404

        if item_id:
            item = Item.query.filter_by(bucketlist_id=bucketlist_id,
                                        id=item_id).first()
            # check if item exists
            if not item:
                response = {
                            'status': 'fail',
                            'message': 'Item not found!'
                            }
                return make_response(jsonify(response)), 404
            # if not item.is_completed:
            #     status = "Not done"
            # else:
            #     status = "Done"
            response = {
                    'id': item.id,
                    'name': item.item_name,
                    'description': item.description,
                    'is_completed': item.is_completed,
                    'date_created': item.created_date,
                    'bucketlist': bucketlist.bucketlist_title
            }
            return make_response(jsonify(response)), 200

        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=20, type=int)
        search = request.args.get("q", type=str)
        response = []
        if search:
            # implement search in query
            items = Item.query.filter_by(bucketlist_id=bucketlist_id) \
                        .filter(Item.item_name
                                .ilike('%' + search + '%')) \
                                .paginate(page, limit, False)
        else:
            items = Item.query.filter_by(bucketlist_id=bucketlist_id) \
                        .paginate(page, limit, False)

        if not items:
            response = {
                        'status': 'success',
                        'message': 'This bucketlist has no items'
                        }
            return make_response(jsonify(response)), 200

        page_count = items.pages

        # add next and previous url links
        if items.has_next:
            next_page = request.url_root + '/api/v1/bucketlists' + \
                        bucketlist_id + '/items' + '?limit=' + str(limit) + \
                        '&page=' + str(page + 1)
        else:
            next_page = 'None'
        if items.has_prev:
            prev_page = request.url_root + '/api/v1/bucketlists/' + \
                        bucketlist_id + '/items' + '?limit=' + str(limit) + \
                        '&page=' + str(page - 1)
        else:
            prev_page = 'None'

        for item in items.items:
            # if not item.is_completed:
            #     status = "Not done"
            # else:
            #     status = "Done"
            info = {
                    'id': item.id,
                    'name': item.item_name,
                    'description': item.description,
                    'is_completed': item.is_completed,
                    'date_created': item.created_date,
                    'bucketlist': bucketlist.bucketlist_title
            }
            response.append(info)
        meta_data = {'meta_data': {'next_page': next_page,
                                   'previous_page': prev_page,
                                   'total_pages': page_count
                                   }}
        response.append(meta_data)
        return make_response(jsonify(response)), 200

    def patch(self, bucketlist_id, item_id):
        """
        Method: `PATCH`
        Update a bucketlist item completion status.
        `URL` path: `/api/v1/bucketlists/<bucketlist_id>/items/<item_id>/`
        """
        # validate token
        user_id_response = validate_token(request)
        if user_id_response is None:
            response = {
                                'status': 'fail',
                                'message': 'Please provide a valid auth token!'
                                }
            return make_response(jsonify(response)), 401

        # check if bucketlist exists
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id,
                                                creator_id=
                                                user_id_response).first()
        if not bucketlist:
            response = {
                        'status': 'fail',
                        'message': 'Bucketlist not found!'
                        }
            return make_response(jsonify(response)), 404

        # check if item exists
        item = Item.query.filter_by(id=item_id, bucketlist_id=
                                    bucketlist_id).first()
        if not item:
            response = {
                        'status': 'fail',
                        'message': 'Item not found!'
                        }
            return make_response(jsonify(response)), 404

        post_data = request.get_json()

        if item.is_completed is True:
            if post_data.get('is_completed') == "true":
                return response_for_updates_with_same_data()
        if item.is_completed is False:
            if post_data.get('is_completed') == "false":
                return response_for_updates_with_same_data()

        item.is_completed = post_data.get('is_completed')
        # if (post_data.get('is_completed')):
        #     if (post_data.get('is_completed') != item.is_completed):
        #         item.is_completed = post_data.get('is_completed')
        #     else:
        #         return response_for_updates_with_same_data()

        item.save()

        info = {
                'id': item.id,
                'name': item.item_name,
                'description': item.description,
                'completion_status': item.is_completed,
                'date_created': item.created_date,
                'date_modified': item.modified_date
                }
        response = {
                    'status': 'success',
                    'message': info
                    }
        return make_response(jsonify(response)), 200

    def put(self, bucketlist_id, item_id):
        """
        Method: `PUT`
        Update a bucketlist item.
        `URL` path: `/api/v1/bucketlists/<bucketlist_id>/items/<item_id>/`
        """
        # validate token
        user_id_response = validate_token(request)
        if user_id_response is None:
            response = {
                                'status': 'fail',
                                'message': 'Please provide a valid auth token!'
                                }
            return make_response(jsonify(response)), 401

        # check if bucketlist exists
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id,
                                                creator_id=
                                                user_id_response).first()
        if not bucketlist:
            response = {
                        'status': 'fail',
                        'message': 'Bucketlist not found!'
                        }
            return make_response(jsonify(response)), 404

        # check if item exists
        item = Item.query.filter_by(id=item_id, bucketlist_id=
                                    bucketlist_id).first()
        if not item:
            response = {
                        'status': 'fail',
                        'message': 'Item not found!'
                        }
            return make_response(jsonify(response)), 404

        post_data = request.get_json()
        if item.item_name == post_data.get('name') and \
           item.description == post_data.get('description'):
            return response_for_updates_with_same_data()

        item.item_name = post_data.get('name')
        item.description = post_data.get('description')

        item.save()

        info = {
                'id': item.id,
                'name': item.item_name,
                'description': item.description,
                'completion_status': item.is_completed,
                'date_created': item.created_date,
                'date_modified': item.modified_date
                }
        response = {
                    'status': 'success',
                    'message': info
                    }
        return make_response(jsonify(response)), 201

    def delete(self, bucketlist_id, item_id):
        """
        Delete a bucketlist item.
        `URL` path: `/api/v1/bucketlists/<bucketlist_id>/items/<item_id>`
        """
        # validate token
        user_id_response = validate_token(request)
        if user_id_response is None:
            response = {
                                'status': 'fail',
                                'message': 'Please provide a valid auth token!'
                                }
            return make_response(jsonify(response)), 401

        # check if bucketlist exists
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id,
                                                creator_id=
                                                user_id_response).first()
        if not bucketlist:
            response = {
                        'status': 'fail',
                        'message': 'Bucketlist not found!'
                        }
            return make_response(jsonify(response)), 404

        # check if item exists
        item = Item.query.filter_by(id=item_id, bucketlist_id=
                                    bucketlist_id).first()

        if not item:
            response = {
                        'status': 'fail',
                        'message': 'Item not found!'
                        }
            return make_response(jsonify(response)), 404

        item.delete()

        response = {
                    'status': 'success',
                    'message': 'Item succesfully deleted'
                    }
        return make_response(jsonify(response)), 200


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
    '/api/v1/bucketlists/<int:bucketlist_id>/items/<int:item_id>/',
    view_func=add_item_view,
    methods=['GET', 'PUT', 'PATCH', 'DELETE']
)
