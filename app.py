from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import *
import datetime
import os
from auth import AuthError, requires_auth
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
API_AUDIENCE = os.environ['API_AUDIENCE']
AUTH0_CALLBACK_URL = os.environ['AUTH0_CALLBACK_URL']

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

@app.route("/", methods=["GET"])
def index():
	return jsonify("Welcome to Casting Agency.")

@app.route("/login", methods=["GET"])
def login():
	return redirect('https://{}/authorize?audience={}&response_type=token&\
client_id={}&redirect_uri={}'.format(AUTH0_DOMAIN,
	API_AUDIENCE, AUTH0_CLIENT_ID,
	AUTH0_CALLBACK_URL))

@app.route("/actors", methods=["GET"])
@requires_auth(permission="get:actors")
def get_actors(jwtoken):
	try:
		actors = Actor.query.order_by(Actor.id).all()
		formatted_actors = [actor.format() for actor in actors]

		return jsonify({
			"success": True,
			"actors": formatted_actors
		}), 200
	except AuthError as auth_error:
		print(auth_error)
	except Exception as error:
		print(error)


@app.route("/actors", methods=["POST"])
@requires_auth(permission="post:actors")
def create_actors(jwtoken):
	try:
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
	except AuthError as auth_error:
		print(auth_error)



@app.route("/actors/<int:actor_id>", methods=["PATCH"])
@requires_auth(permission="patch:actors")
def update_actors(jwtoken, actor_id):
	try:
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
	except AuthError as auth_error:
		print(auth_error)


@app.route("/actors/<int:actor_id>", methods=["DELETE"])
@requires_auth(permission="delete:actors")
def delete_actors(jwtoken, actor_id):
	try:
		actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
		if actor is None:
			abort(404)
		try:
			actor.delete()
			return jsonify({"success": True, "actor_id": actor_id}), 200
		except Exception as error:
			db.session.rollback()
			print(error)
			abort(500)
		finally:
			db.session.close()
	except AuthError as auth_error:
		print(auth_error)


@app.route("/movies", methods=["GET"])
@requires_auth(permission="get:movies")
def get_movies(jwtoken):
	try:
		movies = Movie.query.order_by(Movie.id).all()
		formatted_movies = [movie.format() for movie in movies]

		return jsonify({
			"success": True,
			"movies": formatted_movies
		}), 200
	except AuthError as auth_error:
		print(auth_error)
	except Exception as error:
		print(error)


@app.route("/movies", methods=["POST"])
@requires_auth(permission="post:movies")
def create_movies(jwtoken):
	try:
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
		try:
			movie.insert()
			return jsonify({"success": True, "movie": movie.format()}), 200
		except Exception as error:
			db.session.rollback()
			print(error)
			abort(500)
		finally:
			db.session.close()
	except AuthError as auth_error:
		print(auth_error)

@app.route("/movies/<int:movie_id>", methods=["PATCH"])
@requires_auth(permission="patch:movies")
def update_movies(jwtoken, movie_id):
	try:
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
	except AuthError as auth_error:
		print(auth_error)

@app.route("/movies/<int:movie_id>", methods=["DELETE"])
@requires_auth(permission="delete:movies")
def delete_movies(jwtoken, movie_id):
	try:
		movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
		if movie is None:
			abort(404)
		try:
			movie.delete()
			return jsonify({"success": True, "movie_id": movie_id}), 200
		except Exception as error:
			db.session.rollback()
			print(error)
			abort(500)
		finally:
			db.session.close()
	except AuthError as auth_error:
		print(auth_error)


@app.route("/movies/<int:movie_id>/actors", methods=["GET"])
@requires_auth(permission="get:actors")
def get_actors_by_movies(jwtoken, movie_id):
	try:
		movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
		if movie is None:
			abort(404)
		formatted_actors = [actor.format() for actor in movie.actors]
		return jsonify({"success": True, "actors": formatted_actors})
	except AuthError as auth_error:
		print(auth_error)


@app.route("/actors/<int:actor_id>/movies", methods=["GET"])
@requires_auth(permission="get:movies")
def get_movies_by_actors(jwtoken, actor_id):
	try:
		actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
		if actor is None:
			abort(404)
		formatted_movies = [movie.format() for movie in actor.movies]
		return jsonify({"success": True, "movies": formatted_movies})
	except AuthError as auth_error:
		print(auth_error)


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


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"success": False,
                    "error": 401,
                    "message": "unauthorized"
                    }), 401


@app.errorhandler(AuthError)
def authorization_error(error):
    return (
        jsonify(
            {
                "success": False,
                "error": error.status_code,
                "message": error.error["description"],
            }
        ),
        error.status_code,
    )


if __name__ == "__main__":
    app.run()
