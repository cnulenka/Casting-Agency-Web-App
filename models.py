from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

database_name = os.environ.get('DATABASE_NAME', 'abc123abc1234')
database_path = "postgres://postgres:postgres@{}/{}".format(
    "localhost:5432", database_name
)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def setup_db_for_test():
	db.drop_all()
	db.create_all()

	#add test data
	actor_1 = Actor('Robert Downey Jr.',55,'Male')
	actor_2 = Actor('Scarlett Johansson',36,'Female')
	actor_3 = Actor('Chris Evans',39,'Male')

	actor_1.insert()
	actor_2.insert()
	actor_3.insert()

	movie_1 = Movie("Iron Man", datetime(2008,5,2))
	movie_2 = Movie("Captain America: The First Avenger", datetime(2011,7,22))
	movie_3 = Movie("The Avengers", datetime(2012,5,4))

	movie_1.insert()
	movie_2.insert()
	movie_3.insert()

	casting_1 = castings.insert().values(
		actor_id=actor_1.id, movie_id=movie_1.id)
	casting_2 = castings.insert().values(
		actor_id=actor_2.id, movie_id=movie_2.id)
	casting_3 = castings.insert().values(
		actor_id=actor_1.id, movie_id=movie_3.id)
	casting_4 = castings.insert().values(
		actor_id=actor_2.id, movie_id=movie_3.id)
	casting_5 = castings.insert().values(
		actor_id=actor_3.id, movie_id=movie_3.id)

	db.session.execute(casting_1)
	db.session.execute(casting_2)
	db.session.execute(casting_3)
	db.session.execute(casting_4)
	db.session.execute(casting_5)
	db.session.commit()

class Movie(db.Model):
	__tablename__ = "movies"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	release_date = db.Column(db.Date, nullable=False)

	def __init__(self, title, release_date):
		self.title = title
		self.release_date = release_date

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def format(self):
		return {
			"id": self.id,
			"title": self.title,
			"release_date": self.release_date
		}

#many:many relationship between actors and movies
castings = db.Table('castings',
	db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'),
				primary_key=True),
	db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'),
				primary_key=True)
)

class Actor(db.Model):
	__tablename__ = "actors"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	age = db.Column(db.Integer, nullable=False)
	gender = db.Column(db.String, nullable=False)
	movies = db.relationship('Movie', secondary=castings,
			backref=db.backref('actors', lazy=True))

	def __init__(self, name, age, gender):
		self.name = name
		self.age = age
		self.gender = gender

	def insert(self):
		db.session.add(self)
		db.session.commit()

	def update(self):
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def format(self):
		return {
			"id": self.id,
			"name": self.name,
			"age": self.age,
			"gender":self.gender
		}