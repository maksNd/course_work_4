import jwt
from flask import request, abort
from constants import SECRET, ALGO
from implemented import user_service


def auth_required(func, secret=SECRET, algo=ALGO):
    def wrapper(*args, **kwargs):
        email = request.headers.get('email', None)
        token = request.headers.get('Authorization', None)
        if user_service.check_token_email_conformance(email, token) is False:
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def login_required(func):
    def wrapper(*args, **kwargs):
        data = request.json
        email = request.headers.get('email', None)
        password = data.get('password', None)
        if password is None:
            abort(401)
        if user_service.check_email_password_confirmance(email, password) is False:
            abort(401)
        return func(*args, **kwargs)

    return wrapper

# def admin_required(func, secret=SECRET, algo=ALGO):
#     def wrapper(*args, **kwargs):
#         if 'Authorization' not in request.headers:
#             abort(401)
#
#         token = request.headers['Authorization']
#         role = None
#         try:
#             user = jwt.decode(token, secret, algorithms=algo)
#             role = user.get('role', 'user')
#         except Exception as e:
#             print('JWT decode exception', e)
#             abort(401)
#
#         if role != 'admin':
#             abort(403)
#
#         return func(*args, **kwargs)
#
#     return wrapper
