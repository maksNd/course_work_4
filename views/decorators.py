import jwt
from flask import request, abort
from constants import SECRET, ALGO


def admin_required(func, secret=SECRET, algo=ALGO):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        token = request.headers['Authorization']
        role = None
        try:
            user = jwt.decode(token, secret, algorithms=algo)
            role = user.get('role', 'user')
        except Exception as e:
            print('JWT decode exception', e)
            abort(401)

        if role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper


def auth_required(func, secret=SECRET, algo=ALGO):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        token = request.headers['Authorization']
        try:
            jwt.decode(token, secret, algorithms=algo)
        except Exception as e:
            print('JWT decode exception', e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper
