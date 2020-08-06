from flask import (Flask, request, jsonify, make_response, escape)
from flask_restful import (reqparse, abort, Api, Resource, fields, marshal)
from flask_jwt_extended import (
    jwt_optional, jwt_required, jwt_refresh_token_required)

from .decorater import (requires_access_level, rate_limited, protected)
import service.user as User


user_output_structure = {
    'public_id': fields.String,
    'name': fields.String,
    'phone': fields.String,
    'email': fields.String,
    'role': fields.String,
    'section_public_id': fields.String,
    'section': fields.String,
    'designation': fields.String,
    'designation_public_id': fields.String
}


class UsersApi(Resource):
    def __init__(self):
        return

    # All users
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def get(self, user_public_id):
        try:
            output = User.all()

            if not output:
                return make_response(jsonify({'message': 'NOT_FOUND'}), 404)

            return (marshal(output, user_output_structure))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Create user
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def post(self, user_public_id):
        if not request.is_json:
            return make_response(jsonify({'message': 'INVALID_PARAMETER'}), 400)

        try:
            data = request.get_json()
            name = escape(data['name']).strip().upper()
            phone = escape(data['phone']).strip()
            email = escape(data['email']).strip().lower()
            role = escape(data['role']).strip().upper()
            section_public_id = escape(data['section_public_id']).strip()
            designation_public_id = escape(
                data['designation_public_id']).strip()

            item_by_phone = User.find_by_phone(phone)

            if item_by_phone:
                return make_response(jsonify({'message': 'DUPLICATE'}), 409)

            item_by_email = User.find_by_email(email)

            if item_by_email:
                return make_response(jsonify({'message': 'DUPLICATE'}), 409)

            item = User.create(name, phone, email,
                               role, section_public_id, designation_public_id)

            return (marshal(item, user_output_structure))
        except Exception as e:
            return make_response(jsonify({'error': __name__ + ":post:" + str(e)}), 500)


class UserApi(Resource):
    def __init__(self):
        return

    # Get one user
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def get(self, user_public_id, public_id):
        try:
            item = User.find(public_id)

            if not item:
                return make_response(jsonify({'message': 'NOT_FOUND'}), 404)

            return (marshal(item, user_output_structure))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Change user
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def put(self, user_public_id, public_id):
        if not request.is_json:
            return make_response(jsonify({'message': 'INVALID_PARAMETER'}), 400)

        try:
            data = request.get_json()
            name = escape(data['name']).strip().upper()
            phone = escape(data['phone']).strip()
            email = escape(data['email']).strip().lower()
            role = escape(data['role']).strip().upper()
            section_public_id = escape(data['section_public_id']).strip()
            designation_public_id = escape(
                data['designation_public_id']).strip()

            item_by_public_id = User.find(public_id)

            if not item_by_public_id:
                return make_response(jsonify({'message': 'NOT_FOUND'}), 404)

            item_by_phone = User.find_by_phone(phone)
            item_by_email = User.find_by_email(email)

            if item_by_phone:
                if item_by_public_id.public_id != item_by_phone.public_id:
                    return make_response(jsonify({'message': 'DUPLICATE'}), 409)

            if item_by_email:
                if item_by_public_id.public_id != item_by_email.public_id:
                    return make_response(jsonify({'message': 'DUPLICATE'}), 409)

            item = User.edit(public_id, name, phone, email,
                             role, section_public_id, designation_public_id)

            return (marshal(item, user_output_structure))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Delete user
    # @rate_limited(limit=50, minutes=60)
    @jwt_required
    @requires_access_level(['admin'])
    def delete(self, user_public_id, public_id):
        try:
            item = User.find(public_id)

            if not item:
                return make_response(jsonify({'message': 'NOT_FOUND'}), 404)

            item = User.remove(public_id)

            return (marshal(item, user_output_structure))
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)
