import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import *


class CastingAgencyTestCase(unittest.TestCase):
    """This class has the test cases for casting agency web app endpoints"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test_db"
        self.database_path = "postgres://postgres:postgres@{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
