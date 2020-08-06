from flask import (request, jsonify, make_response, escape)
from flask_restful import (Resource, fields, marshal)
from flask_jwt_extended import (JWTManager,
                                jwt_optional, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, unset_jwt_cookies,
                                create_access_token, create_refresh_token,
                                set_access_cookies, set_refresh_cookies)


import datetime

from .decorater import (requires_access_level, rate_limited, protected)
import service.section as Section


output_fields = {
    'public_id': fields.String,
    'name': fields.String
}


class SectionsApi(Resource):
    def __init__(self):
        return

    # Get all sections
    # @cross_origin()
    # @protected(limit=10, minutes=60)
    # @rate_limited(limit=50, minutes=60)
    # @cached(minutes=5)
    @jwt_required
    def get(self):
        try:
            output = Section.all()

            return (marshal(output, output_fields))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Create section
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def post(self, user_public_id):
        if not request.is_json:
            return make_response(jsonify({'message': 'INVALID_PARAMETER'}), 400)

        try:
            data = request.get_json()
            name = escape(data['name']).strip().upper()

            item = Section.find_by_name(name)

            if item:
                return make_response(jsonify({'message': 'DUPLICATE'}), 409)

            item = Section.create(name)
            return (marshal(item, output_fields))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


class SectionApi(Resource):
    def __init__(self):
        return

    # Get one section
    # @cross_origin()
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def get(self, user_public_id, public_id: str):
        try:
            item = Section.find(public_id)

            return (marshal(item, output_fields))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Change section
    # @cross_origin()

    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def put(self, user_public_id, public_id: str):
        if not request.is_json:
            return make_response(jsonify({'message': 'INVALID_PARAMETER'}), 400)

        try:
            data = request.get_json()
            name = escape(data['name']).strip().upper()

            item_by_public_id = Section.find(public_id)

            if not item_by_public_id:
                return make_response(jsonify({'message': 'NOT_FOUND'}), 404)

            item_by_name = Section.find_by_name(name)

            if item_by_name:
                if item_by_public_id.public_id != item_by_name.public_id:
                    return make_response(jsonify({'message': 'DUPLICATE'}), 409)

            item = Section.edit(public_id, name)
            return (marshal(item, output_fields))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Delete section
    # @cross_origin()
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def delete(self, user_public_id, public_id: str):
        try:
            item = Section.find(public_id)

            if not item:
                return make_response(jsonify({'message': 'NOT_FOUND'}), 404)

            item = Section.remove(public_id)
            return (marshal(item, output_fields))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)
