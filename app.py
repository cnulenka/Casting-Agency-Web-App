from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    abort,
    jsonify,
)
from flask_cors import CORS
from models import *
import datetime

app = Flask(__name__)
setup_db(app)
CORS(app)

# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,POST,DELETE,PATCH,OPTIONS"
    )
    return response


@app.route("/actors", methods=["GET"])
def get_actors():
	try:
		actors = Actor.query.order_by(Actor.id).all()
		formatted_actors = [actor.format() for actor in actors]

		return jsonify({
			"success": True,
			"actors": formatted_actors
		}), 200
	except Exception as error:
		print(error)


@app.route("/actors", methods=["POST"])
def create_actors():
	body = request.get_json()
	input_name = body.get("name", None)
	input_age = body.get("age", None)
	input_gender = body.get("gender", None)
	if not input_name or not input_age or not input_gender:
		print("Incomplete actor infomation provided.")
		abort(422)
	try:
		actor = Actor(name=input_name, age=input_age, gender=input_gender)
		actor.insert()
		return jsonify({"success": True, "actor": actor.format()}), 200
	except Exception as error:
		db.session.rollback()
		print(error)
		abort(500)
	finally:
		db.session.close()



@app.route("/actors/<int:actor_id>", methods=["PATCH"])
def update_actors(actor_id):
	body = request.get_json()
	input_name = body.get("name", None)
	input_age = body.get("age", None)
	input_gender = body.get("gender", None)
	actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
	if actor is None:
		abort(404)
	if input_name:
		actor.name = input_name
	if input_age:
		actor.age = input_age
	if input_gender:
		actor.gender = input_gender
	try:
		actor.update()
		return jsonify({"success": True, "actor": actor.format()}), 200
	except Exception as error:
		print(error)
		db.session.rollback()
		abort(500)
	finally:
		db.session.close()


@app.route("/actors/<int:actor_id>", methods=["DELETE"])
def delete_actors(actor_id):
	actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
	if actor is None:
		abort(404)
	try:
		actor.delete()
		return jsonify({"success": True, "actor": actor_id}), 200
	except Exception as error:
		db.session.rollback()
		print(error)
		abort(500)
	finally:
		db.session.close()

@app.route("/movies", methods=["GET"])
def get_movies():
	try:
		movies = Movie.query.order_by(Movie.id).all()
		formatted_movies = [movie.format() for movie in movies]

		return jsonify({
			"success": True,
			"movies": formatted_movies
		}), 200
	except Exception as error:
		print(error)


@app.route("/movies", methods=["POST"])
def create_movies():
	body = request.get_json()
	input_title = body.get("title", None)
	input_release_date = body.get("release_date", None)
	input_actors_ids = body.get("actors_ids",None)
	if not input_title or not input_release_date:
		print("Incomplete movie infomation provided.")
		abort(422)
	if not input_actors_ids or len(input_actors_ids) == 0:
		print("Actors must be provided to add a movie")
		abort(422)
	try:
		day,month,year = map(int, input_release_date.split("/"))
		input_release_date = datetime.datetime(year, month, day)
		movie = Movie(title=input_title, release_date=input_release_date)
		for actor_id in input_actors_ids:
			actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
			if actor is None:
				print("Actor does not exists")
				abort(404)
			movie.actors.append(actor)
			actor.movies.append(movie)
		movie.insert()
		return jsonify({"success": True, "movie": movie.format()}), 200
	except Exception as error:
		db.session.rollback()
		print(error)
		abort(500)
	finally:
		db.session.close()

@app.route("/movies/<int:movie_id>", methods=["PATCH"])
def update_movies(movie_id):
	body = request.get_json()
	input_title = body.get("title", None)
	input_release_date = body.get("release_date", None)
	movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
	if movie is None:
		abort(404)
	if input_title:
		movie.title = input_title
	if input_release_date:
		movie.release_date = input_release_date
	try:
		movie.update()
		return jsonify({"success": True, "movie": movie.format()}), 200
	except Exception as error:
		print(error)
		db.session.rollback()
		abort(500)
	finally:
		db.session.close()

@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movies(movie_id):
	movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
	if movie is None:
		abort(404)
	try:
		movie.delete()
		return jsonify({"success": True, "movie": movie_id}), 200
	except Exception as error:
		db.session.rollback()
		print(error)
		abort(500)
	finally:
		db.session.close()


@app.route("/movies/<int:movie_id>/actors", methods=["GET"])
def get_actors_by_movies(movie_id):
	movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
	if movie is None:
		abort(404)
	formatted_actors = [actor.format() for actor in movie.actors]
	return jsonify({"success": True, "actors": formatted_actors,})


@app.route("/actors/<int:actor_id>/movies", methods=["GET"])
def get_movies_by_actors(actor_id):
	actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
	if actor is None:
		abort(404)
	formatted_movies = [movie.format() for movie in actor.movies]
	return jsonify({"success": True, "movies": formatted_movies})


# Error Handling
"""
    Error handlers to pass message with the error codes
"""


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"success": False,
                    "error": 500,
                    "message": "server error"
                    }), 500



if __name__ == "__main__":
    app.run()
