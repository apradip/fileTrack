from flask import Flask, app, jsonify
from flask_restful import Api
from flask_jwt_extended import (JWTManager,
                                jwt_optional, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, unset_jwt_cookies,
                                create_access_token, create_refresh_token,
                                set_access_cookies, set_refresh_cookies)

# from flask_cors import CORS
import os

import model.mongo_setup as mongo_setup
from api.route import RoutesApi


def get_flask_app(config: dict = None):
    flask_app = Flask(__name__)

    # # header configuration
    # flask_app.config['JWT_TOKEN_LOCATION'] = ['headers']
    # flask_app.config['JWT_HEADER_NAME'] = 'Authorization'
    # flask_app.config['JWT_HEADER_TYPE'] = 'Bearer'
    # flask_app.config['JWT_SECRET_KEY'] = os.environ.get('FT_TOKEN_HASH_KEY')

    # cookie configuration
    flask_app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
    flask_app.config['JWT_COOKIE_SECURE'] = False
    flask_app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    flask_app.config['JWT_ALGORITHM'] = 'HS256'
    flask_app.config['JWT_DECODE_ALGORITHMS'] = 'HS256'
    flask_app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'
    flask_app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
    flask_app.config['JWT_REFRESH_COOKIE_PATH'] = '/api/'
    flask_app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token_cookie'
    flask_app.config['JWT_ACCESS_CSRF_COOKIE_PATH'] = '/api/'
    flask_app.config['JWT_ACCESS_CSRF_COOKIE_NAME'] = 'csrf_access_token'
    flask_app.config['JWT_REFRESH_CSRF_COOKIE_PATH'] = '/api/'
    flask_app.config['JWT_REFRESH_CSRF_COOKIE_NAME'] = 'csrf_refresh_token'
    flask_app.config['JWT_SECRET_KEY'] = os.environ.get('FT_TOKEN_HASH_KEY')

    jwt = JWTManager(flask_app)

    @jwt.expired_token_loader
    def expired_token_callback(expired_token):
        token_type = expired_token['type']
        return jsonify({'message': 'The {} token has expired'.format(token_type)}), 401

    @jwt.unauthorized_loader
    def unauthorized_token_callback(unauthorized_token):
        return jsonify({'message': 'UNAUTHORIZED_TOKEN'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(invalid_token):
        return jsonify({'message': 'INVALID_TOKEN'}), 422

    @jwt.needs_fresh_token_loader
    def fresh_jwt_required(refresh_token):
        return jsonify({'message': 'FRESH_TOKEN_REQUIRE'}), 401

    # @jwt.user_claims_loader
    # def add_claims_to_access_token(identity):
    #     return{'hello': identity,
    #            'foo': ['bar', 'baz']}

    # CORS(flask_app)
    # cors = CORS(flask_app, resources={
    #             r"/api/v1/*": {"http://127.0.0.1:5000": "*"}})

    mongo_setup.global_init()

    # init api and routes
    api = Api(app=flask_app)
    RoutesApi(api=api)

    return flask_app


if __name__ == '__main__':
    app = get_flask_app()
    # app.run(host='0.0.0.0', port=5000,  debug=True)
    app.run(debug=True)
