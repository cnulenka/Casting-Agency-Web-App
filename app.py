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


if __name__ == "__main__":
    app.run()
