from flask_restful import Api
from flask_jwt_extended import (JWTManager,
                                jwt_optional, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, unset_jwt_cookies,
                                create_access_token, create_refresh_token,
                                set_access_cookies, set_refresh_cookies)

from api.auth import AuthApi, PasswordApi, OTPApi
from api.user import UsersApi, UserApi
from api.file import FilesApi, FileApi, LocationApi
from api.section import SectionsApi, SectionApi
from api.designation import DesignationsApi, DesignationApi


def RoutesApi(api):
    api.add_resource(AuthApi, "/api/v1/auth")
    api.add_resource(PasswordApi, "/api/v1/changepassword")
    api.add_resource(OTPApi, "/api/v1/otp")

    api.add_resource(UsersApi, "/api/v1/user")
    api.add_resource(UserApi, "/api/v1/user/<public_id>")

    api.add_resource(FilesApi, "/api/v1/file")
    api.add_resource(FileApi, "/api/v1/file/<public_id>")
    api.add_resource(LocationApi, "/api/v1/file/location/<file_number>")

    api.add_resource(SectionsApi, "/api/v1/section")
    api.add_resource(SectionApi, "/api/v1/section/<public_id>")

    api.add_resource(DesignationsApi, "/api/v1/designation")
    api.add_resource(DesignationApi, "/api/v1/designation/<public_id>")
