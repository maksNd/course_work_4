from flask_restx import Resource, Namespace
from flask import request, abort

from dao.model.user import UserSchema
from implemented import user_service
from views.decorators import admin_required, auth_required

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):

    @admin_required
    def get(self):
        users = user_service.get_all()
        result = UserSchema(many=True).dump(users)
        return result, 200

    def post(self):
        data_for_user = request.json
        try:
            user_service.create(data_for_user)
            return '', 201
        except Exception as e:
            return '', 400


@user_ns.route('/<int:uid>')
class UserView(Resource):

    @admin_required
    def get(self, uid):
        user = user_service.get_one(uid)
        result = UserSchema().dump(user)
        return result, 200

    @admin_required
    def put(self, uid):
        data_for_user = request.json
        if 'id' not in data_for_user:
            data_for_user['id'] = uid
        user_service.update(data_for_user)
        return '', 204

    @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return '', 204


@user_ns.route('/auth')
class UserAuth(Resource):
    def post(self):
        data = request.json
        login = data.get('username', None)
        password = data.get('password', None)
        role = data.get('role', None)
        if user_service.auth(login, password) is False:
            abort(400)
        return user_service.generate_jwt(login, password, role), 200

    def put(self):
        data = request.json
        login = data.get('username')
        role = data.get('role')
        password = data.get('password')
        refresh_token = data.get('refresh_token')
        if user_service.check_token(refresh_token) is False:
            abort(400)
        else:
            return user_service.generate_jwt(login, password, role), 200
