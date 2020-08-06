from flask import (Flask, request, jsonify, make_response, escape)
from flask_restful import (reqparse, abort, Api, Resource, fields, marshal)
from flask_jwt_extended import (
    jwt_optional, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

from .decorater import (requires_access_level, rate_limited, protected)
import service.section as Section
import service.file as File


file_output_structure = {
    'public_id': fields.String,
    'name': fields.String,
    'number': fields.String,
    'section_public_id': fields.String,
    'section': fields.String
}

user_field = {'name': fields.String, 'phone': fields.String,
              'email': fields.String, 'section': fields.String, 'designation': fields.String}

file_field = {
    'name': fields.String,
    'number': fields.String,
    'section': fields.String
}

location_field = {
    'user': fields.Nested(user_field),
    'in_date_time': fields.DateTime(dt_format='rfc822'),
    'out_date_time': fields.DateTime(dt_format='rfc822'),
    'processing_time': fields.String
}

location_output_structure = {
    'name': fields.String,
    'number': fields.String,
    'section': fields.String,
    'locations': fields.List(fields.Nested(location_field))
}


class FilesApi(Resource):
    def __init__(self):
        return

    # Get all files
    # @protected(limit=10, minutes=60)
    # @rate_limited(limit=50, minutes=60)
    @jwt_optional
    def get(self):
        try:
            output = File.all()
            return (marshal(output, file_output_structure))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Crate file
    # @rate_limited(limit=50, minutes=60)

    @jwt_required
    @requires_access_level(['admin', 'file creator'])
    def post(self, user_public_id):
        user_public_id = self

        try:
            if not request.is_json:
                return make_response(jsonify({'message': 'INVALID_PARAMETER'}), 400)

            data = request.get_json()
            name = escape(data['name']).strip().upper()
            number = escape(data['number']).strip().upper()
            section_public_id = escape(data['section_public_id']).strip()

            item_by_number = File.find_by_number(number)

            if item_by_number:
                return make_response(jsonify({'message': 'DUPLICATE'}), 409)

            item = File.create(name,
                               number,
                               section_public_id,
                               user_public_id)

            return (marshal(item, file_output_structure))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


class FileApi(Resource):
    def __init__(self):
        return

    # Change file
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin', 'file creator'])
    def put(self, user_public_id, public_id):
        if not request.is_json:
            return make_response(jsonify({'message': 'INVALID_PARAMETER'}), 400)

        try:
            data = request.get_json()
            name = escape(data['name']).strip().upper()
            number = escape(data['number']).strip().upper()
            section_public_id = escape(
                data['section_public_id']).strip()

            item_by_public_id = File.find(public_id)
            if not item_by_public_id:
                return make_response(jsonify({'message': 'NOT_FOUND'}), 404)

            item_by_number = File.find_by_number(number)

            if item_by_number:
                if item_by_public_id.public_id != item_by_number.public_id:
                    return make_response(jsonify({'message': 'DUPLICATE'}), 409)

            item = File.edit(public_id, name, number,
                             section_public_id)

            return (marshal(item, file_output_structure))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Delete file

    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin', 'file creator'])
    def delete(self, user_public_id, public_id):
        try:
            item = File.find(public_id)

            if not item:
                return make_response(jsonify({'message': 'NOT_FOUND'}), 404)

            item = File.remove(public_id)
            return (marshal(item, file_output_structure))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


class LocationApi(Resource):
    def __init__(self):
        return

    # Get file position
    # @protected(limit=10, minutes=60)
    # @rate_limited(limit=50, minutes=60)
    # @cached(minutes=5)
    @jwt_optional
    def get(self, file_number):
        if len(file_number) < 5:
            return make_response(jsonify({'message': 'INVALID_PARAMETER'}), 402)
        else:
            try:
                output = File.get_all_location(file_number)

                return (marshal(output, location_output_structure))
            except Exception as e:
                return make_response(jsonify({'message': str(e)}), 500)

    # Change file position

    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['*'])
    def put(self, user_public_id, file_number):
        user_public_id = self

        try:
            item = File.find_by_number(file_number)

            if item:
                if not File.update_out(item.public_id, user_public_id):
                    File.update_in(item.public_id, user_public_id)

                    return jsonify({'message': 'SUCCESS'})

                return jsonify({'message': 'SUCCESS'})

            return make_response(jsonify({'message': 'NOT_FOUND'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)
