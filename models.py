from flask_sqlalchemy import SQLAlchemy


database_name = "castingagencydb"
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