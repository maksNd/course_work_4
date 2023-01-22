from flask_restx import Resource, Namespace
from flask import request

from dao.model.director import DirectorSchema
from implemented import director_service
from views.decorators import auth_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):

    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        director_data = request.json
        director = director_service.create(director_data)
        return '', 201, {"location": f"/directors/{director.id}"}


@director_ns.route('/<int:rid>')
class DirectorView(Resource):

    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    def put(self, rid):
        director_data = request.json
        if 'id' not in director_data:
            director_data['id'] = rid
        director_service.update(director_data)
        return '', 204

    def delete(self, rid):
        director_service.delete(rid)
        return '', 204
