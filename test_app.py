import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import *
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class CastingAgencyTestCase(unittest.TestCase):
    """This class has the test cases for casting agency web app endpoints"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "casting_agency_test_db"
        self.database_path = "postgres://postgres:postgres@{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        #drop db, create and populate with test data
        setup_db_for_test()

        self.casting_assistant_auth_header = {
            "Authorization": "Bearer " + \
            os.environ.get('CASTING_ASSISTANT_TOKEN', 'abc123abc1234')
        }

        self.casting_director_auth_header = {
            "Authorization": "Bearer " + \
            os.environ.get('CASTING_DIRECTOR_TOKEN', 'abc123abc1234')
        }

        self.executive_producer_auth_header = {
            "Authorization": "Bearer " + \
            os.environ.get('EXECUTIVE_PRODUCER_TOKEN', 'abc123abc1234')
        }

        self.create_actor_success = {
            "name": "Chris Hemsworth",
            "age": 37,
            "gender": "Male"
        }

        self.create_actor_fail = {
            "name": "Chris Evans",
            "age": 39,
        }

        self.create_movie_success = {
            "title": "Captain America: Civil War",
            "release_date": "12/04/2016",
            "actors_ids": [1,2,3]
        }

        self.create_movie_fail_1 = {
            "title": "Avenger: Infinity War",
        }

        self.create_movie_fail_2 = {
            "title": "Avenger: Infinity War",
            "release_date": "27/04/2018",
            "actors_ids": []
        }

        self.create_movie_fail_3 = {
            "title": "Avenger: Infinity War",
            "release_date": "27/04/2018",
            "actors_ids": [100]
        }



        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_get_actors(self):
        res = self.client().get("/actors",
                headers=self.casting_assistant_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actors"]))

    def test_create_actors_success_director(self):
        res = self.client().post("/actors",
                headers=self.casting_director_auth_header,
                json=self.create_actor_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    def test_create_actors_success_producer(self):
        res = self.client().post("/actors",
                headers=self.executive_producer_auth_header,
                json=self.create_actor_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    #create actor fails due authentication failure
    def test_create_actors_401_failure_assistant(self):
        res = self.client().post("/actors",
                headers=self.casting_assistant_auth_header,
                json=self.create_actor_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    #create actor fails due to incomplete input
    def test_422_if_create_actor_fails(self):
        res = self.client().post("/actors",
                headers=self.executive_producer_auth_header,
                json=self.create_actor_fail)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "unprocessable")

    def test_update_actors_success_producer(self):
        res = self.client().patch("/actors/1",
                headers=self.executive_producer_auth_header,
                json=self.create_actor_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    def test_update_actors_success_director(self):
        res = self.client().patch("/actors/1",
                headers=self.casting_director_auth_header,
                json=self.create_actor_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    #update actor fails due authentication failure
    def test_update_actors_401_failure_assistant(self):
        res = self.client().patch("/actors/1",
                headers=self.casting_assistant_auth_header,
                json=self.create_actor_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    def test_update_actors_404_failure(self):
        res = self.client().patch("/actors/100",
                headers=self.casting_director_auth_header,
                json=self.create_actor_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    def test_delete_actors_success_producer(self):
        res = self.client().delete("/actors/1",
                headers=self.executive_producer_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertEqual(res_data["actor_id"], 1)

    def test_delete_actors_success_director(self):
        res = self.client().delete("/actors/1",
                headers=self.casting_director_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertEqual(res_data["actor_id"], 1)

    #delete actor fails due authentication failure
    def test_delete_actors_401_failure_assistant(self):
        res = self.client().delete("/actors/1",
                headers=self.casting_assistant_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    def test_delete_actors_404_failure(self):
        res = self.client().delete("/actors/100",
                headers=self.casting_director_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    #test movie endpoints
    def test_get_movies(self):
        res = self.client().get("/movies",
                headers=self.casting_assistant_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["movies"]))

    def test_create_movies_401_failure_director(self):
        res = self.client().post("/movies",
                headers=self.casting_director_auth_header,
                json=self.create_movie_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    def test_create_movies_success_producer(self):
        res = self.client().post("/movies",
                headers=self.executive_producer_auth_header,
                json=self.create_movie_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["movie"]))

    #create actor fails due authentication failure
    def test_create_movies_401_failure_assistant(self):
        res = self.client().post("/movies",
                headers=self.casting_assistant_auth_header,
                json=self.create_movie_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    #create actor fails due to incomplete input
    def test_422_create_movie_fails_incomplete_info(self):
        res = self.client().post("/movies",
                headers=self.executive_producer_auth_header,
                json=self.create_movie_fail_1)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "unprocessable")

    #create movie fails due to incomplete input
    def test_422_create_movie_fails_no_actor_input_info(self):
        res = self.client().post("/movies",
                headers=self.executive_producer_auth_header,
                json=self.create_movie_fail_2)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "unprocessable")

    #create movie fails due to wrong actor id
    def test_404_create_movie_fails_wrong_actor_id(self):
        res = self.client().post("/movies",
                headers=self.executive_producer_auth_header,
                json=self.create_movie_fail_3)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    def test_update_movies_success_producer(self):
        res = self.client().patch("/movies/1",
                headers=self.executive_producer_auth_header,
                json=self.create_movie_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["movie"]))

    def test_update_movies_success_director(self):
        res = self.client().patch("/movies/1",
                headers=self.casting_director_auth_header,
                json=self.create_movie_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["movie"]))

    #update actor fails due authentication failure
    def test_update_movies_401_failure_assistant(self):
        res = self.client().patch("/movies/1",
                headers=self.casting_assistant_auth_header,
                json=self.create_movie_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    def test_update_movies_404_failure(self):
        res = self.client().patch("/movies/100",
                headers=self.casting_director_auth_header,
                json=self.create_movie_success)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    def test_delete_movies_success_producer(self):
        res = self.client().delete("/movies/1",
                headers=self.executive_producer_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertEqual(res_data["movie_id"], 1)

    def test_delete_movies_401_failure_director(self):
        res = self.client().delete("/movies/1",
                headers=self.casting_director_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    #delete actor fails due authentication failure
    def test_delete_actors_401_failure_assistant(self):
        res = self.client().delete("/movies/1",
                headers=self.casting_assistant_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    def test_delete_actors_404_failure(self):
        res = self.client().delete("/movies/100",
                headers=self.executive_producer_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    def test_get_actors_by_movies(self):
        res = self.client().get("/movies/1/actors",
                headers=self.casting_assistant_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actors"]))

    def test_404_get_actors_by_movies(self):
        res = self.client().get("/movies/100/actors",
                headers=self.casting_assistant_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    def test_get_movies_by_actors(self):
        res = self.client().get("/actors/1/movies",
                headers=self.casting_assistant_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["movies"]))

    def test_404_get_movies_by_actors(self):
        res = self.client().get("/actors/100/movies",
                headers=self.casting_assistant_auth_header)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
