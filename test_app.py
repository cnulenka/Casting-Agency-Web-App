import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import *
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#auth tokens should be updated before running tests, read the README to know more details
CASTING_ASSISTANT_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxCRzVkMGJsbndGOGFMNktpWUFtTyJ9.eyJpc3MiOiJodHRwczovL2Rldi1rcms3aDY1aS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0NGM2ZTdiODQ1ODYwMDY5M2E0MGM0IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNTIxOTkwNCwiZXhwIjoxNjE1MzA2MzA0LCJhenAiOiJpdldHZ3NjczVJM055QkZRY01YdENneURBenBCckt3MCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.GQSsmX4mdm5ptGxtkHSRvTO1OM6WiWCzCm_Jccx37zlz4pVOth7ciGnDsYbUn58imbrwyiC0KVmXOzCqbvVR9YmCawYgyb7v6a-AMc9u62hehY-minBw1SCpMfRy_MUHVRr7uBk1gI1AOqdlO0hOUU4Ir3oomKo2C6OHxnccNsjUZcktaqrf0RjFq_kLo4N8WfDMAKXSD1vSzceg9PmLmq1HxsKg2wyxm0cVMqnyfP-uEU5TBlylWkpsrrukvtCcCfwKEQXRj7fjwxCGvoVgnbOC7bStWNyFcrB6epcK7_H6av_DAuDPCwjBqoTz6embE7GYB6A6Nsgov8eXuOtFjw'

CASTING_DIRECTOR_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxCRzVkMGJsbndGOGFMNktpWUFtTyJ9.eyJpc3MiOiJodHRwczovL2Rldi1rcms3aDY1aS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0NGM3MjAzNTE5ZDkwMDY4Zjg0ZjRlIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNTIyMDA1OCwiZXhwIjoxNjE1MzA2NDU4LCJhenAiOiJpdldHZ3NjczVJM055QkZRY01YdENneURBenBCckt3MCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.mi2Hem27YHATMctxABG4Hdt-_YLyvy3vKTPCIKV2zqsCVLFpET3ZDAtMfiu5kIuLPvkbJb_WPoWEX1ZTjb7pNx00ty2P0YClOeg3E6--1OcGKRWL1hw0J0CoXqmWfPcXmwep3te33YEc3B12x-8xSv6uCP-K5vRjDgf88Y_DESfhAg3DdQAD35xuxaY7QAl35Fbv689k3EzdJZ9knI7bMcUOeF1wrFzUweMLX-qJ6tBMM63CfJzzsfgdJ_CP0a4_6sQwGUIV5BSji60YNg9BysUrVGf9q2TSdmaYPQocUdfwATPOCGLTrhqh2RDFkR7KUrpYEh96txuQWWJE2jFAOQ'

EXECUTIVE_PRODUCER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxCRzVkMGJsbndGOGFMNktpWUFtTyJ9.eyJpc3MiOiJodHRwczovL2Rldi1rcms3aDY1aS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0NGM3NDczNTE5ZDkwMDY4Zjg0ZjUzIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNTIyMDEyMSwiZXhwIjoxNjE1MzA2NTIxLCJhenAiOiJpdldHZ3NjczVJM055QkZRY01YdENneURBenBCckt3MCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.JzGeOY_nK8mlZEaUGO76OsuoiKVZv1eeE4Cz243HLFoqOMURBqnidweEbKvQKwe_159x-NL0YYYCqzInEB3uK72AnyEVrr_IoWPlCcX2mwuFMc-ye2RBfnAzdm9vAZrgUgSS2LMSk1ezr4ThGudtt-gup5SXtLm8XIr0Ptwu90rKwu21-R8IxwgjF38mwQiy6_8hOHvHffa3KDw6AfH2bYpHSFX6UTjyImnyqqANv8mqJU4kLtm9VQTO5w0wWhZHDoZeSguia8oxpk31fMydraCZ8msNyNqdksPeThjiv5Qg0fmjTq-xlt2A6Su8qJpRzi0HhJgepTWwFk8XCOQrbg'

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
            "Authorization": "Bearer " + CASTING_ASSISTANT_TOKEN}

        self.casting_director_auth_header = {
            "Authorization": "Bearer " + CASTING_DIRECTOR_TOKEN}

        self.executive_producer_auth_header = {
            "Authorization": "Bearer " + EXECUTIVE_PRODUCER_TOKEN}

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
