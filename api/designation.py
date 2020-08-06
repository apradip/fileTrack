from flask import Flask, request, jsonify, make_response, escape
from flask_restful import reqparse, abort, Api, Resource, fields, marshal
from flask_jwt_extended import (
    jwt_optional, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

from .decorater import requires_access_level, rate_limited, protected

import service.designation as Designation

output_fields = {
    'public_id': fields.String,
    'name': fields.String
}


class DesignationsApi(Resource):
    def __init__(self):
        return

    # Get all designation
    # @protected(limit=10, minutes=60)
    # @rate_limited(limit=50, minutes=60)
    # @cached(minutes=5)
    def get(self):
        try:
            output = Designation.all()

            return (marshal(output, output_fields))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Create designation
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def post(self, user_public_id):
        if not request.is_json:
            return make_response(jsonify({'message': 'INVALID_PARAMETER'}), 400)

        try:
            data = request.get_json()
            name = escape(data['name']).strip().upper()

            item = Designation.find_by_name(name)

            if item:
                return make_response(jsonify({'message': 'DUPLICATE'}), 409)

            item = Designation.create(name)

            return (marshal(item, output_fields))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


class DesignationApi(Resource):
    def __init__(self):
        return

    # Get single designation
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def get(self, user_public_id, public_id):
        try:
            item = Designation.find(public_id)

            if not item:
                return make_response(jsonify({'message': 'NOT_FOUND'}), 404)

            return (marshal(item, output_fields))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Change designation
    @jwt_required
    @requires_access_level(['admin'])
    def put(self, user_public_id, public_id):
        if not request.is_json:
            return make_response(jsonify({'message': 'INVALID_PARAMETER'}), 400)

        try:
            data = request.get_json()
            name = escape(data['name']).strip().upper()
            item_by_public_id = Designation.find(public_id)

            if not item_by_public_id:
                return make_response(jsonify({'message': 'NOT_FOUND'}), 404)

            item_by_name = Designation.find_by_name(name)

            if item_by_name:
                if item_by_public_id.public_id != item_by_name.public_id:
                    return make_response(jsonify({'message': 'DUPLICATE'}), 409)

            item = Designation.edit(public_id, name)
            return (marshal(item, output_fields))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Delete designation
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def delete(self, user_public_id, public_id):
        try:
            item = Designation.find(public_id)

            if not item:
                return make_response(jsonify({'message': 'NOT_FOUND'}), 404)

            item = Designation.remove(public_id)
            return (marshal(item, output_fields))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)
