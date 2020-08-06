from flask import (Flask, jsonify, request, make_response, escape)
from flask_restful import (Resource)
from flask_jwt_extended import (JWTManager,
                                jwt_optional, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, unset_jwt_cookies,
                                create_access_token, create_refresh_token,
                                set_access_cookies, set_refresh_cookies)
import datetime

from .decorater import (rate_limited, protected)
from .utility import (generateOtp, sendSms, sendEmail)

import service.auth as Auth


class AuthApi(Resource):
    def __init__(self):
        return

    # Login
    # @rate_limited(limit=50, minutes=60)
    # @jwt_optional
    def post(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            resp = make_response(jsonify({'message': 'UNAUTHORIZE'}), 401)
            return resp

        try:
            user = Auth.login(auth.username.strip().lower(), auth.password)

            if not user:
                resp = make_response(jsonify({'message': 'UNAUTHORIZE'}), 401)
                return resp

            userInfo = {'public_id': user.public_id,
                        'role': user.role,
                        'name': user.name,
                        'phone': user.phone,
                        'email': user.email}

            expires = datetime.timedelta(seconds=60)
            access_token = create_access_token(
                identity=userInfo, expires_delta=expires, fresh=True)
            refresh_token = create_refresh_token(identity=userInfo)

            resp = jsonify({'message': 'SUCCESS'})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)

            return make_response(resp, 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Refresh token
    @jwt_refresh_token_required
    def put(self):
        try:
            userInfo = get_jwt_identity()
            expires = datetime.timedelta(seconds=60)
            access_token = create_access_token(
                identity=userInfo, expires_delta=expires, fresh=True)

            resp = jsonify({'message': 'SUCCESS'})
            set_access_cookies(resp, access_token)

            return make_response(resp, 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

    # Logout
    # @rate_limited(limit=50, minutes=60)
    def delete(self):
        try:
            resp = jsonify({'message': 'SUCCESS'})
            unset_jwt_cookies(resp)

            return make_response(resp, 200)
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)


class OTPApi(Resource):
    def __init__(self):
        return

    # Generate OTP
    # @rate_limited(limit=50, minutes=60)
    @jwt_optional
    def post(self):
        auth = request.authorization

        if not auth or not auth.username:
            abort(401)

        try:
            otp = generateOtp(6)
            user = Auth.update_otp(auth.username.strip().lower(), otp)

            if not user:
                abort(401)

            subject = "FileTrack OTP is {0}".format(
                otp)
            body = "Your OTP for FileTrack is {0}\nPlease login using the following url https://filetrack.in and do not share it with others.\nIf you have not requested for OTP reset, please contact your System Administrator.\nNote: This is a system generated email please do not reply.\n\n\nRegards FileTrack Team".format(
                otp)

            sendEmail(user.email, subject, body)

            body = "Your OTP fom FileTrack is {0}. Please login using the same. If you have not requested for OTP, please contact your System Administrator. Regards FileTrack Team".format(
                otp)

            sendSms(user.phone, body)

            return jsonify({'message': 'SUCCESS'})
        except Exception as e:
            return make_response(jsonify({'message': str(e)}), 500)

        return None


class PasswordApi(Resource):
    def __init__(self):
        return

    @jwt_required
    def put(self):
        public_id = None

        # try:
        userInfo = get_jwt_identity()

        #    if not userInfo:
        #         return make_response(jsonify({'message': 'UNAUTHORIZE'}), 401)

        #     public_id = userInfo['public_id']
        # except Exception as e:
        #     return make_response(jsonify({'message': str(e)}), 500)

        # try:
        #     data = request.get_json()
        #     password = escape(data['password']).strip()
        #     password_new = escape(data['password_new']).strip()

        #     if not Auth.update_password(public_id, password, password_new):
        #         return make_response(jsonify({'message': 'UNAUTHORIZE'}), 401)

        #     return jsonify({'message': 'SUCCESS'})
        # except Exception as e:
        #     return make_response(jsonify({'message': str(e)}), 500)
