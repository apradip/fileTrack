from flask import Flask, request, jsonify, make_response, escape
from flask_restful import reqparse, abort, Resource
from flask_jwt_extended import (JWTManager,
                                jwt_optional, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, get_jwt_claims, unset_jwt_cookies,
                                create_access_token, create_refresh_token,
                                set_access_cookies, set_refresh_cookies)

from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.contrib.cache import MemcachedCache
from functools import wraps
from datetime import datetime
import hashlib
# import memcache
import traceback
import os
# import jwt
import redis
# from wakatime_website import app

import service.auth as Auth

# app = Flask(__name__)

r = redis.Redis(decode_responses=True)

# mc = memcache.Client("127.0.0.1", debug=True)
# cache = MemcachedCache(mc)


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            public_id = None

            try:
                token = get_jwt_identity()

                if not token:
                    return make_response(jsonify({'message': 'UNAUTHORIZED'}), 401)

                for level in access_level:
                    if level == '*':
                        found = True
                        break

                    if level:
                        if token['role'] == level.upper():
                            found = True
                            break

                if not found:
                    return make_response(jsonify({'message': 'UNAUTHORIZED'}), 401)

                user_public_id = token['public_id']
            except Exception as e:
                return make_response(jsonify({'message': str(e)}), 500)
            return f(user_public_id, *args, **kwargs)
        return decorated_function
    return decorator


def rate_limited(fn=None, limit=20, methods=[], ip=True, minutes=1):
    if not isinstance(limit, int):
        raise Exception('Limit must be an integer number.')
    if limit < 1:
        raise Exception('Limit must be greater than zero.')

    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if not methods or request.method in methods:

                if ip:
                    increment_counter(type='ip',
                                      for_methods=methods,
                                      minutes=minutes)

                    count = get_count(type='ip',
                                      for_methods=methods)

                    if count > limit:
                        abort(429)

            return f(*args, **kwargs)

        return inner
    return wrapper(fn) if fn else wrapper


def get_counter_key(type=None,
                    for_only_this_route=True,
                    for_methods=None):

    if not isinstance(for_methods, list):
        for_methods = []
    if type == 'ip':
        key = request.remote_addr
    else:
        raise Exception('Unknown rate limit type: {0}'.format(type))
    route = ''

    if for_only_this_route:
        route = '{endpoint}'.format(
            endpoint=request.endpoint,
        )
    return ('{type}-{methods}-{key}{route}').format(
        type=type,
        methods=','.join(for_methods),
        key=key,
        route=route
    )


def increment_counter(type=None,
                      for_only_this_route=True,
                      for_methods=None,
                      minutes=1):

    if type not in ['ip']:
        raise Exception('Type must be ip or user.')

    key = get_counter_key(type=type,
                          for_only_this_route=for_only_this_route,
                          for_methods=for_methods)

    try:
        r.incr(key)
        r.expire(key, time=60 * minutes)
    except:
        print(traceback.format_exc())
        # app.logger.error(traceback.format_exc())
        pass


def get_count(type=None,
              for_only_this_route=True,
              for_methods=None):

    key = get_counter_key(
        type=type,
        for_only_this_route=for_only_this_route,
        for_methods=for_methods)

    try:
        return int(r.get(key) or 0)
    except:
        print(traceback.format_exc())
        # app.logger.error(traceback.format_exc())
        return 0


def protected(fn=None, limit=10, minutes=60):

    if not isinstance(limit, int):
        raise Exception('Limit must be an integer number.')
    if not isinstance(minutes, int):
        raise Exception('Minutes must be an integer number.')

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            key = 'bruteforce-{}-{}'.format(request.endpoint,
                                            request.remote_addr)
            try:
                count = int(r.get(key) or 0)
                if count > limit:
                    r.incr(key)
                    seconds = 60 * minutes
                    r.expire(key, time=seconds)
                    # app.logger.info('Request blocked by protected decorator.')
                    return '404', 404
            except:
                # app.logger.error(traceback.format_exc())
                print(traceback.format_exc())

            try:
                result = func(*args, **kwargs)
            except NotFound:
                try:
                    r.incr(key)
                    seconds = 60 * minutes
                    r.expire(key, time=seconds)
                except:
                    pass
                raise

            if isinstance(result, tuple) and len(result) > 1 and result[1] == 404:
                try:
                    r.incr(key)
                    seconds = 60 * minutes
                    r.expire(key, time=seconds)
                except:
                    pass

            return result

        return inner
    return wrapper(fn) if fn else wrapper


# def cached(fn=None, unique_per_user=True, minutes=30):
#     """Caches a Flask route/view in memcached.

#     The request url, args, and current user are used to build the cache key.
#     Only GET requests are cached.
#     By default, cached requests expire after 30 minutes.
#     """

#     if not isinstance(minutes, int):
#         raise Exception('Minutes must be an integer number.')

#     def wrapper(func):
#         @wraps(func)
#         def inner(*args, **kwargs):
#             if request.method != 'GET':
#                 return func(*args, **kwargs)

#             prefix = 'flask-request'
#             path = request.full_path
#             # user_id = app.current_user.id if app.current_user.is_authenticated else None
#             user_id = None
#             key = ('{user}-{method}-{path}').format(
#                 user=user_id,
#                 method=request.method,
#                 path=path
#             )

#             hashed = hashlib.md5(key.encode('utf8')).hexdigest()
#             hashed = '{prefix}-{hashed}'.format(prefix=prefix, hashed=hashed)

#             try:
#                 resp = cache.get(hashed)
#                 if resp:
#                     return resp
#             except:
#                 # app.logger.error(traceback.format_exc())
#                 print(traceback.format_exc())
#                 resp = None

#             resp = func(*args, **kwargs)

#             try:
#                 cache.set(hashed, resp, timeout=minutes * 60)
#             except:
#                 # app.logger.error(traceback.format_exc())
#                 print(traceback.format_exc())
#             return resp
#         return inner
#     return wrapper(fn) if fn else wrapper
