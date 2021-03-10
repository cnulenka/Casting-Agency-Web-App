import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# auth tokens should be updated before running tests,
# read the README to know more details
CASTING_ASSISTANT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxCRzVkMGJsbndGOGFMNktpWUFtTyJ9.eyJpc3MiOiJodHRwczovL2Rldi1rcms3aDY1aS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0NGM2ZTdiODQ1ODYwMDY5M2E0MGM0IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNTMyMjUwMSwiZXhwIjoxNjE1NDA4OTAxLCJhenAiOiJpdldHZ3NjczVJM055QkZRY01YdENneURBenBCckt3MCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.XGCjkJLdUFBDT9GS6s8KM6QxLAPPG87OPsJ95HIjBcXsD6m9lZBp1VSnxXacS4m-ulEZKSZODg0-t095cfJkvgR9lPmCKes--yMndvKRIHNm8zxCjT3ysmHg8DPWVVxOhFZ7S0k4tMJr6w_POea3FPTU9vgo04Zu_Mr8_fAGPraNdvAFNgnIYKEekW7rKt6vLDG6Y3X-n4DlOYxTxdeRk8zm6zaCx3VIvhEvrVSnGmM6xTGAULb_q883-7DJXcmS0whcUqHzlNPS0ptsP7Erp_iYP5z7e7ZVpQeYJvYA2vf6ZFuzmRB4KJErpoX8QqlH3EimXYVkUFx_4rRwU1go1A"

CASTING_DIRECTOR_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxCRzVkMGJsbndGOGFMNktpWUFtTyJ9.eyJpc3MiOiJodHRwczovL2Rldi1rcms3aDY1aS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0NGM3MjAzNTE5ZDkwMDY4Zjg0ZjRlIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNTMyMjY1OSwiZXhwIjoxNjE1NDA5MDU5LCJhenAiOiJpdldHZ3NjczVJM055QkZRY01YdENneURBenBCckt3MCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.bZYuMFbntbYkngKDWVA-e4KTjOmhi9EpY5JuCdP6svTDZYOMyoL4tfS0AIxDox67mLfY63DVx7Yy7AlTCU6FTyepK0EwsmBO8mCyIzliN1AL_3oB0TKJGIH_kLHQH6yCMW0HmXTXRRx1IjAW_iqpsYo8QXcT3QV3apLYVGFbU9Gs-0jwDldaDJ2U_w3gE0WTPfGYaPb0gWhGUwdWExF0t9qMAor8FWzy-oM2EUwfQE__5iSi8pGz3Y_6tCzF6DHpcnyc-_UeYTw2HOLEVY970-QXNEXL4YEVGsHc31U4tYmTAggzgqSPF8TdXdwgXUvdybR3QQr3V6DvymL-hg3pTQ"

EXECUTIVE_PRODUCER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxCRzVkMGJsbndGOGFMNktpWUFtTyJ9.eyJpc3MiOiJodHRwczovL2Rldi1rcms3aDY1aS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0NGM3NDczNTE5ZDkwMDY4Zjg0ZjUzIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYxNTMyMjc1NCwiZXhwIjoxNjE1NDA5MTU0LCJhenAiOiJpdldHZ3NjczVJM055QkZRY01YdENneURBenBCckt3MCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.UesOR1x8hwGJgUIAN241ElsI9qTiW3uWe31J7vWIXH6jsso6yQJpWPD4PEbo-7aodicTgB0qci-W_kQ8SrHEWDuDzycP5S5REEphRz-F3vH_dvqxo9DDwpOJIy9Vvr8ngOSp3f5VyrAXHHsQRQj-EZq5ZghPVF44coa1lXjtTEPCM620X4Po8IT2cXyuVRUU59nuKehGl9k7x5KRgpzY1BGl0TjMzjQcqHmH2CjZVNhrGUdwMCg_6oAL3Twpng3zvMEMrNwxygOvJKXoa97KxIgqc6r1BCSgiGutHsqaZiKRvA62mECJCwCsMb-TZU0i7sX7fFGrM2jMH6Yyl75i5A"


class CastingAgencyTestCase(unittest.TestCase):
    """This class has the test cases for casting agency web app endpoints"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.environ.get(
                                            "TEST_DATABASE_NAME",
                                            "abc123abc1234"
                                            )
        self.database_path = "postgres://postgres:postgres@{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # drop db, create and populate with test data
        setup_db_for_test()

        self.casting_assistant_auth_header = {
            "Authorization": "Bearer " + CASTING_ASSISTANT_TOKEN
        }

        self.casting_director_auth_header = {
            "Authorization": "Bearer " + CASTING_DIRECTOR_TOKEN
        }

        self.executive_producer_auth_header = {
            "Authorization": "Bearer " + EXECUTIVE_PRODUCER_TOKEN
        }

        self.create_actor_success = {
            "name": "Chris Hemsworth",
            "age": 37,
            "gender": "Male",
        }

        self.create_actor_fail = {
            "name": "Chris Evans",
            "age": 39,
        }

        self.create_movie_success = {
            "title": "Captain America: Civil War",
            "release_date": "12/04/2016",
            "actors_ids": [1, 2, 3],
        }

        self.create_movie_fail_1 = {
            "title": "Avenger: Infinity War",
        }

        self.create_movie_fail_2 = {
            "title": "Avenger: Infinity War",
            "release_date": "27/04/2018",
            "actors_ids": [],
        }

        self.create_movie_fail_3 = {
            "title": "Avenger: Infinity War",
            "release_date": "27/04/2018",
            "actors_ids": [100],
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    # test get actors endpoint
    def test_get_actors(self):
        res = self.client().get(
                                "/actors",
                                headers=self.casting_assistant_auth_header
                                )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actors"]))

    # test create actor endpoint with casting director auth token
    def test_create_actors_success_director(self):
        res = self.client().post(
            "/actors",
            headers=self.casting_director_auth_header,
            json=self.create_actor_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    # test create actor endpoint with executive producer auth token
    def test_create_actors_success_producer(self):
        res = self.client().post(
            "/actors",
            headers=self.executive_producer_auth_header,
            json=self.create_actor_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    # create actor fails due authentication failure with casting
    # assistant auth token
    def test_create_actors_401_failure_assistant(self):
        res = self.client().post(
            "/actors",
            headers=self.casting_assistant_auth_header,
            json=self.create_actor_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    # create actor fails due to incomplete input
    def test_422_if_create_actor_fails(self):
        res = self.client().post(
            "/actors",
            headers=self.executive_producer_auth_header,
            json=self.create_actor_fail,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "unprocessable")

    # test update actors with executive producer auth token
    def test_update_actors_success_producer(self):
        res = self.client().patch(
            "/actors/1",
            headers=self.executive_producer_auth_header,
            json=self.create_actor_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    # test update actors with casting director auth token
    def test_update_actors_success_director(self):
        res = self.client().patch(
            "/actors/1",
            headers=self.casting_director_auth_header,
            json=self.create_actor_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actor"]))

    # update actor fails due authentication failure
    # with casting assitant auth token
    def test_update_actors_401_failure_assistant(self):
        res = self.client().patch(
            "/actors/1",
            headers=self.casting_assistant_auth_header,
            json=self.create_actor_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    # test update actor faiure if actor with id doesnot
    # exists in database
    def test_update_actors_404_failure(self):
        res = self.client().patch(
            "/actors/100",
            headers=self.casting_director_auth_header,
            json=self.create_actor_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    # test successfull delete actor with executive producer auth token
    def test_delete_actors_success_producer(self):
        res = self.client().delete(
            "/actors/1", headers=self.executive_producer_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertEqual(res_data["actor_id"], 1)

    # test successfull delete actor with casting director auth token
    def test_delete_actors_success_director(self):
        res = self.client().delete(
            "/actors/1", headers=self.casting_director_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertEqual(res_data["actor_id"], 1)

    # delete actor fails due authentication failure
    # with casting director auth token
    def test_delete_actors_401_failure_assistant(self):
        res = self.client().delete(
            "/actors/1", headers=self.casting_assistant_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    # delete actor failure if actor with input
    # id doesnot exits
    def test_delete_actors_404_failure(self):
        res = self.client().delete(
            "/actors/100", headers=self.casting_director_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    # test get movie endpoint
    def test_get_movies(self):
        res = self.client().get(
                                "/movies",
                                headers=self.casting_assistant_auth_header
                                )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["movies"]))

    # test create movie authentication failure
    # with casting director auth token
    def test_create_movies_401_failure_director(self):
        res = self.client().post(
            "/movies",
            headers=self.casting_director_auth_header,
            json=self.create_movie_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    # test create movies success with executive producer
    # auth token
    def test_create_movies_success_producer(self):
        res = self.client().post(
            "/movies",
            headers=self.executive_producer_auth_header,
            json=self.create_movie_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["movie"]))

    # create actor fails due authentication failure
    # with casting assistant auth token
    def test_create_movies_401_failure_assistant(self):
        res = self.client().post(
            "/movies",
            headers=self.casting_assistant_auth_header,
            json=self.create_movie_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    # create actor fails due to incomplete input
    def test_422_create_movie_fails_incomplete_info(self):
        res = self.client().post(
            "/movies",
            headers=self.executive_producer_auth_header,
            json=self.create_movie_fail_1,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "unprocessable")

    # create movie fails due to incomplete input, no input actor ids
    def test_422_create_movie_fails_no_actor_input_info(self):
        res = self.client().post(
            "/movies",
            headers=self.executive_producer_auth_header,
            json=self.create_movie_fail_2,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "unprocessable")

    # create movie fails due to wrong actor id input
    def test_404_create_movie_fails_wrong_actor_id(self):
        res = self.client().post(
            "/movies",
            headers=self.executive_producer_auth_header,
            json=self.create_movie_fail_3,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    # test update movie success with executive producer
    # auth token
    def test_update_movies_success_producer(self):
        res = self.client().patch(
            "/movies/1",
            headers=self.executive_producer_auth_header,
            json=self.create_movie_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["movie"]))

    # test update movies success with casting
    # director auth token
    def test_update_movies_success_director(self):
        res = self.client().patch(
            "/movies/1",
            headers=self.casting_director_auth_header,
            json=self.create_movie_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["movie"]))

    # update actor fails due authentication failure
    # with casting assitant auth token
    def test_update_movies_401_failure_assistant(self):
        res = self.client().patch(
            "/movies/1",
            headers=self.casting_assistant_auth_header,
            json=self.create_movie_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    # test update movies failure if movie with
    # input id does not exists
    def test_update_movies_404_failure(self):
        res = self.client().patch(
            "/movies/100",
            headers=self.casting_director_auth_header,
            json=self.create_movie_success,
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    # test delete movies success with executive producer
    # auth token
    def test_delete_movies_success_producer(self):
        res = self.client().delete(
            "/movies/1", headers=self.executive_producer_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertEqual(res_data["movie_id"], 1)

    # test delete movies failure with casting director
    # auth token
    def test_delete_movies_401_failure_director(self):
        res = self.client().delete(
            "/movies/1", headers=self.casting_director_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    # test delete actor fails due authentication failure
    # with casting assitant auth token
    def test_delete_actors_401_failure_assistant(self):
        res = self.client().delete(
            "/movies/1", headers=self.casting_assistant_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "Permission missing.")

    # test delete actor failure if actor with input id
    # doesnot exists
    def test_delete_actors_404_failure(self):
        res = self.client().delete(
            "/movies/100", headers=self.executive_producer_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    # test get actor by movies success
    def test_get_actors_by_movies(self):
        res = self.client().get(
            "/movies/1/actors", headers=self.casting_assistant_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["actors"]))

    # test get actor by movies failure if movie
    # with input id does not exits
    def test_404_get_actors_by_movies(self):
        res = self.client().get(
            "/movies/100/actors", headers=self.casting_assistant_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")

    # test get movies by actor success
    def test_get_movies_by_actors(self):
        res = self.client().get(
            "/actors/1/movies", headers=self.casting_assistant_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)
        self.assertTrue(len(res_data["movies"]))

    # test get movies by actor failure if actor
    # with input id does not exists
    def test_404_get_movies_by_actors(self):
        res = self.client().get(
            "/actors/100/movies", headers=self.casting_assistant_auth_header
        )
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["success"], False)
        self.assertEqual(res_data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
