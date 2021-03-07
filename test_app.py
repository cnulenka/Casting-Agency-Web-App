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

        self.create_actor_success_1 = {
            "name": "Chris Hemsworth",
            "age": 37,
            "gender": "Male"
        }

        self.create_actor_fail_1 = {
            "name": "Chris Evans",
            "age": 39,
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
                json=self.create_actor_success_1)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    def test_create_actors_success_producer(self):
        res = self.client().post("/actors",
                headers=self.executive_producer_auth_header,
                json=self.create_actor_success_1)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    #create actor fails due authentication failure
    def test_create_actors_401_failure_assistant(self):
        res = self.client().post("/actors",
                headers=self.casting_assistant_auth_header,
                json=self.create_actor_success_1)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    #create actor fails due to incomplete input
    def test_422_if_create_actor_fails(self):
        res = self.client().post("/actors",
                headers=self.executive_producer_auth_header,
                json=self.create_actor_fail_1)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "unprocessable")

    def test_update_actors_success_producer(self):
        res = self.client().patch("/actors/1",
                headers=self.executive_producer_auth_header,
                json=self.create_actor_success_1)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    def test_update_actors_success_director(self):
        res = self.client().patch("/actors/1",
                headers=self.casting_director_auth_header,
                json=self.create_actor_success_1)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    #update actor fails due authentication failure
    def test_update_actors_401_failure_assistant(self):
        res = self.client().patch("/actors/1",
                headers=self.casting_assistant_auth_header,
                json=self.create_actor_success_1)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    def test_update_actors_404_failure(self):
        res = self.client().patch("/actors/100",
                headers=self.casting_director_auth_header,
                json=self.create_actor_success_1)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
