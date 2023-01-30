from flask_restx import Resource, Namespace
from flask import request, abort

from dao.model.user import UserSchema
from implemented import user_service
from views.decorators import auth_required, login_required

user_ns = Namespace('user')


@user_ns.route('/<int:uid>')
class UserView(Resource):

    def get(self, uid):
        user = user_service.get_one(uid)
        result = UserSchema().dump(user)
        return result, 200

    def put(self, uid):
        data_for_user = request.json
        if 'id' not in data_for_user:
            data_for_user['id'] = uid
        user_service.update(data_for_user)
        return '', 204

    # @admin_required
    # def delete(self, uid):
    #     user_service.delete(uid)
    #     return '', 204


@user_ns.route('/auth/register')
class UsersRegister(Resource):

    def post(self):  # передавая  email и пароль, создаем пользователя
        data_for_user = request.json
        try:
            user_service.create(data_for_user)
            return '', 201
        except Exception as e:
            return '', 400


@user_ns.route('/auth/login')
class UserLogin(Resource):
    @login_required
    def post(self):  # передаем email и пароль и возвращаем пользователю токены
        data = request.json
        email = data.get('email', None)
        return user_service.generate_jwt(email), 200

    @auth_required
    def put(self):  # принимаем refresh token и, если он валиден, создаем пару новых
        email = request.headers.get('email')
        return user_service.generate_jwt(email), 200


@user_ns.route('/')
class UsersView(Resource):

    @auth_required
    def get(self):  # профиль пользователя
        email = request.headers.get('email', None)
        result = UserSchema().dump(user_service.search_by_email(email))
        return result, 200

    @auth_required
    def patch(self):
        data = request.json
        email = request.headers.get('email')
        user_service.update(data, email)
        return '', 200


@user_ns.route('/password')
class UserPassword(Resource):

    @auth_required
    @login_required
    def put(self):
        email = request.headers.get('email')
        new_password = request.json.get('new_password')
        data = {'password': new_password}
        user_service.update(data, email)
        return '', 200
