from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import movie_service
from views.decorators import auth_required

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):

    # @auth_required
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
        }

        status = request.args.get('status')
        if status == 'new':
            all_movies = movie_service.get_sorted()
        else:
            all_movies = movie_service.get_all(filters)

        page = request.args.get('page')
        if page is not None:
            try:
                page = int(page)
                object_count_on_page = 5
                from_object = ((page - 1) * object_count_on_page)
                to_object = from_object + object_count_on_page
                result = MovieSchema(many=True).dump(all_movies[from_object:to_object])
            except ValueError:
                return '', 400
        else:
            result = MovieSchema(many=True).dump(all_movies)
        return result, 200

    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):

    # @auth_required
    def get(self, bid):
        b = movie_service.get_one(bid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        movie_service.update(req_json)
        return "", 204

    def delete(self, bid):
        movie_service.delete(bid)
        return "", 204
