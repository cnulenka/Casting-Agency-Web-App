# Casting-Agency-Web-App

This web app models a casting agency compnay and facilitates managing actors and movies. Web app uses
authentication and has roles with specific permissions.

Web App Supports
1. Adding new actors, new movies and assigning actors to movies.
2. Deleting actors and movies.
3. Updating actors and movies.
4. Viewing movies of any actor.
5. Viewing actors of any movie.

Roles and Permissions
- Casting Assistant
	- Can view actors and movies
- Casting Director
	- All permissions a Casting Assistant has and…
	- Add or delete an actor from the database
 	- Modify actors or movies
- Executive Producer
	- All permissions a Casting Director has and…
	- Add or delete a movie from the database

#### Database Setup
Download and Install postgres database. Create a local database and update the setup.sh
script with your data base name. You also need to create a separate database for tests and
update setup.sh accordingly.

#### Setup Dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.
Major requirements are Flask, SQLAlchemy

#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.
Makesure you have updated setup.sh with database names and run it to set up the local env vars.

To run the server, execute:

```
export FLASK_APP=app
export FLASK_DEBUG=1
flask run
```

The application runs on `http://127.0.0.1:5000/` by default.

go to http://127.0.0.1:5000/login, it will redirect you to Auth0 login page, use any of the credentials below to get token with permissions as per the role. Once you get the token, it will be valid for 24 hours.

- Casting Assitant
    - email: castingassistant@gmail.com
    - password: casting@123
- Casting Director
    - email: castingdirector@gmail.com
    - password: casting@123
-Executive Producer
    -email: executiveproducer@gmail.com
    -password: casting@123

## Testing
To run the tests, make sure you have created a test db and updated setup.sh with test db.
Also make sure to update the auth tokens in test_app.py to run the tests successfully
name
```
python test_app.py
```
The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

* Base URL: This API is at hosted in heroku at . 
* The API can be run locally at `http://127.0.0.1:5000/`
* Authentication: This API implements Authentication using Auth0, requires Auth tokens
to access endpoints.

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

* 400 – bad request
* 404 – resource not found
* 401 - unauthorized
* 422 – unprocessable
* 500 - server error

### Endpoints

#### GET /actors
* General
	* Fetches the list of actors from data base
	* Request Arguments: None
	* Returns: An object with list of actors with attributes name, age, gender and id. 
* Sample: `curl -X GET http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"`<br>

        {
            "actors": [
                        {
                            "age": 55,
                            "gender": "Male",
                            "id": 1,
                            "name": "Robert Downey Jr."
                        },
                        {
                            "age": 36,
                            "gender": "Female",
                            "id": 2,
                            "name": "Scarlett Johansson"
                        },
                        {
                            "age": 39,
                            "gender": "Male",
                            "id": 3,
                            "name": "Chris Evans"
                        }
                    ],
            "success": true
        }

#### GET /movies

* General
    * Fetches the list of movies from data base
    * Request Arguments: None
    * Returns: An object with success_code and list of movies with attributes id, title, release_date. 
* Sample: `curl -X GET http://127.0.0.1:5000/movies -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"`<br>

        {
            "movies": [
                        {
                            "id": 3,
                            "release_date": "Fri, 22 Jul 2011 00:00:00 GMT",
                            "title": "Captain America: The First Avenger"
                        },
                        {
                            "id": 5,
                            "release_date": "Fri, 04 May 2012 00:00:00 GMT",
                            "title": "The Avengers"
                        },
                        {
                            "id": 6,
                            "release_date": "Fri, 01 May 2015 00:00:00 GMT",
                            "title": "Avengers: Age of Ultron"
                        },
                        {
                            "id": 7,
                            "release_date": "Fri, 02 May 2008 00:00:00 GMT",
                            "title": "Iron Man"
                        }
                    ],
            "success": true
        }

#### GET /movies/\<int:movie_id\>/actors

* General
    * Fetches the list of actors for the movie in data base with id movie_id
    * Request Arguments: None
    * Returns: An object with success_code and list of actors with attributes name, age, gender and id. 
* Sample: `curl -X GET http://127.0.0.1:5000/movies/3/actors -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"`<br>

        {
            "actors": [
                        {
                            "age": 39,
                            "gender": "Male",
                            "id": 3,
                            "name": "Chris Evans"
                        }
                    ],
            "success": true
        }

#### GET /actors/\<int:actor_id\>/movies

* General
    * Fetches the list of movies for the actor in data base with id actor_id
    * Request Arguments: None
    * Returns: An object with success_code and list of movies with attributes id, title, release_date. 
* Sample: `curl -X GET http://127.0.0.1:5000/actors/2/movies -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"`<br>

        {
            "movies": [
                    {
                        "id": 5,
                        "release_date": "Fri, 04 May 2012 00:00:00 GMT",
                        "title": "The Avengers"
                    },
                    {
                        "id": 6,
                        "release_date": "Fri, 01 May 2015 00:00:00 GMT",
                        "title": "Avengers: Age of Ultron"
                    }
                ],
            "success": true
        }

#### POST /actors

* General:
  * Creates a new actor using the submitted name, age and gender.
  * Returns JSON object with newly created actor information upon success.
* Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{
            "name": "Robert Downey Jr.",
            "age": 55,
            "gender": "Male"
        }'`<br>

        {
            "actor": {
                            "age": 55,
                            "gender": "Male",
                            "id": 1,
                            "name": "Robert Downey Jr."
                        },
            "success": true
        }

#### POST /movies

* General:
  * Creates a new movies using the submitted title, release_date and actors ids.
  * Returns JSON object with newly created movie information upon success.
* Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{
            "title": "The Avengers",
            "release_date":"04/05/2012",
            "actors_ids": [1,3,5]
        }'`<br>

        {
            "movie": {
                        "id": 5,
                        "release_date": "Fri, 04 May 2012 00:00:00 GMT",
                        "title": "The Avengers"
                    },
            "success": true
        }

#### PATCH /actors/\<int:actor_id\>

* General:
  * Updates the actor with id actor_id using submittd name, age or gender.
  * Returns JSON object with newly created actor information upon success.
* Sample: `curl http://127.0.0.1:5000/actors/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{
            "age": 50,
        }'`<br>

        {
            "actor": {
                            "age": 50,
                            "gender": "Male",
                            "id": 1,
                            "name": "Robert Downey Jr."
                        },
            "success": true
        }

#### PATCH /movies/\<int:movie_id\>

* General:
  * Updates the movie with id movie_id using the submitted title or release_date.
  * Returns JSON object with newly created movie information upon success.
* Sample: `curl http://127.0.0.1:5000/movies/5 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{
            "title": "Avengers",
        }'`<br>

        {
            "movie": {
                        "id": 5,
                        "release_date": "Fri, 04 May 2012 00:00:00 GMT",
                        "title": "Avengers"
                    },
            "success": true
        }

#### DELETE /actors/\<int:id\>

* General:
  * Deletes the actor by id, using url parameters.
  * Returns JSON with actor id and success upon successful deletion.
* Sample: `curl http://127.0.0.1:5000/actors/5 -X DELETE H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"`<br>

        {
            "success": True,
            "actor_id": 5
        }

#### DELETE /movies/\<int:id\>

* General:
  * Deletes the movie by id, using url parameters.
  * Returns JSON with movie id and success upon successful deletion.
* Sample: `curl http://127.0.0.1:5000/movies/5 -X DELETE H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"`<br>

        {
            "success": True,
            "movie_id": 5
        }

