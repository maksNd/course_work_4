from flask_restx import Resource, Namespace
from flask import request

from dao.model.genre import GenreSchema
from implemented import genre_service
from views.decorators import admin_required, auth_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):

    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data_for_genre = request.json
        genre = genre_service.create(data_for_genre)
        return '', 201, {"location": f"/genres/{genre.id}"}


@genre_ns.route('/<int:rid>')
class GenreView(Resource):

    @auth_required
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        data_for_genre = request.json
        if "id" not in data_for_genre:
            data_for_genre["id"] = rid
        genre_service.update(data_for_genre)
        return "", 204

    @admin_required
    def delete(self, rid):
        genre_service.delete(rid)
        return '', 204
