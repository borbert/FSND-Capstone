import os, json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db_drop_and_create_all, setup_db, Actor, Movies
from auth import requires_auth, AuthError

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app,resources={r"/*": {"origins": "*"}}) 

  return app

app = create_app()

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
  response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, DELETE, OPTIONS')
  return response

'''
Routes 
'''
#-------------------Generate a new auth token-----------------#
@app.route("/authorization", methods=["GET"])
def generate_auth_url():
  url = f'https://{AUTH0_DOMAIN}/authorize' \
      f'?audience={AUTH0_JWT_API_AUDIENCE}' \
      f'&response_type=token&client_id=' \
      f'{AUTH0_CLIENT_ID}&redirect_uri=' \
      f'{AUTH0_CALLBACK_URL}'
  return jsonify({
      'url': url
  })
#--------------------------General Routes------------------------#
'''
GET / endpoint
    This is a public endpoint that represents the list model with the short() description method.
    This returns status code 200 and json {'health': 'Running!!'}.
Returns:
    Status code 200 and list of lists.
'''
@app.route('/')
def heath_check():
  return jsonify({'health': 'Running!!'}), 200

#--------------------------Actors Controllers------------------------#
'''
GET /my_lists endpoint
    This is an endpoint that requires the 'get:lists' permission.  Once the action is authorized
    the method with retrieve a list of lists, in their long description format, from the database.
Requires:
    'get:lists' permission
Returns:
    Status code 200 and json {"success": True, "lists": lists} where lists is the list of user lists.
Known errors:
    401 Unauthorized if user lacks permission
'''
@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
  actors_query = Actor.query.order_by(Actor.id).all()
  actors = [actor.short() for actor in actors_query]

  return jsonify({
      "success": True,
      "actors": actors
  }), 200

'''
GET /my_lists endpoint
    This is an endpoint that requires the 'get:lists' permission.  Once the action is authorized
    the method with retrieve a list of lists, in their long description format, from the database.
Requires:
    'get:lists' permission
Returns:
    Status code 200 and json {"success": True, "lists": lists} where lists is the list of user lists.
Known errors:
    401 Unauthorized if user lacks permission
'''
@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(payload):
  # return 'auth implemented'
  try:
    request_body = request.get_json()
    if 'name' not in request_body \
            or 'date_of_birth' not in request_body:
        raise KeyError

    if request_body['name'] == '' \
            or request_body['date_of_birth'] == '':
        raise ValueError

    full_name = ''
    if 'full_name' in request_body:
      full_name = request_body["full_name"]

    new_actor = Actor(request_body['name'], full_name,request_body['date_of_birth'])
    new_actor.insert()

    return jsonify({
      "success": True,
      "created_actor_id": new_actor.id
    }), 201

  except (TypeError, KeyError, ValueError):
      abort(422)

  except Exception:
      abort(500)

'''
GET /my_lists endpoint
    This is an endpoint that requires the 'get:lists' permission.  Once the action is authorized
    the method with retrieve a list of lists, in their long description format, from the database.
Requires:
    'get:lists' permission
Returns:
    Status code 200 and json {"success": True, "lists": lists} where lists is the list of user lists.
Known errors:
    401 Unauthorized if user lacks permission
'''
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth("patch:actor")
def update_actor(payload, actor_id):
  actor = Actor.query.get_or_404(actor_id)

  try:
    request_body = request.get_json()
    if not bool(request_body):
      raise TypeError

    if "name" in request_body:
      if request_body["name"] == "":
        raise ValueError

      actor.name = request_body["name"]

    if "full_name" in request_body:
      if request_body["full_name"] == "":
        raise ValueError

      actor.full_name = request_body["full_name"]

    if 'date_of_birth' in request_body:
      if request_body["date_of_birth"] == "":
        raise ValueError

      actor.date_of_birth = request_body["date_of_birth"]

    actor.update()

    return jsonify({
      "success": True,
      "actor_info": actor.long()
    }), 200

  except (TypeError, ValueError, KeyError):
    abort(422)

  except Exception:
    abort(500)

'''
GET /my_lists endpoint
    This is an endpoint that requires the 'get:lists' permission.  Once the action is authorized
    the method with retrieve a list of lists, in their long description format, from the database.
Requires:
    'get:lists' permission
Returns:
    Status code 200 and json {"success": True, "lists": lists} where lists is the list of user lists.
Known errors:
    401 Unauthorized if user lacks permission
'''
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth("delete:actor")
def delete_actor(payload, actor_id):
  actor = Actor.query.get_or_404(actor_id)

  try:
    actor.delete()

    return jsonify({
        "success": True,
        "deleted_actor_id": actor.id
    }), 200

  except Exception:
    abort(500)

#--------------------------Movie Controllers-------------------------#
'''
GET /my_lists endpoint
    This is an endpoint that requires the 'get:lists' permission.  Once the action is authorized
    the method with retrieve a list of lists, in their long description format, from the database.
Requires:
    'get:lists' permission
Returns:
    Status code 200 and json {"success": True, "lists": lists} where lists is the list of user lists.
Known errors:
    401 Unauthorized if user lacks permission
'''
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movies.query.all()

    if not movies:
        abort(404)

    return jsonify({
        'success': True,
        'movies': [movie.format() for movie in movies]
    }), 200

'''
GET /my_lists endpoint
    This is an endpoint that requires the 'get:lists' permission.  Once the action is authorized
    the method with retrieve a list of lists, in their long description format, from the database.
Requires:
    'get:lists' permission
Returns:
    Status code 200 and json {"success": True, "lists": lists} where lists is the list of user lists.
Known errors:
    401 Unauthorized if user lacks permission
'''
@app.route('/movies', methods=['POST'])
@requires_auth("post:movies")
def create_movie(payload):
  # return 'auth implemented'
  try:
    request_body = request.get_json()

    if 'title' not in request_body \
            or 'release_year' not in request_body \
            or 'duration' not in request_body \
            or 'imdb_rating' not in request_body \
            or 'cast' not in request_body:
        raise KeyError

    if request_body['title'] == '' \
            or request_body['release_year'] <= 0 \
            or request_body['duration'] <= 0 \
            or request_body['imdb_rating'] < 0 \
            or request_body["imdb_rating"] > 10 \
            or len(request_body["cast"]) == 0:
        raise TypeError

    new_movie = Movies(
        request_body['title'],
        request_body['release_year'],
        request_body['duration'],
        request_body['imdb_rating']
    )
    actors = Actor.query.filter(
        Actor.name.in_(request_body["cast"])).all()

    if len(request_body["cast"]) == len(actors):
        new_movie.cast = actors
        new_movie.insert()
    else:
        raise ValueError

    return jsonify({
        "success": True,
        "created_movie_id": new_movie.id
    }), 201

  except (TypeError, KeyError, ValueError):
    abort(422)

  except Exception:
    abort(500)

@app.route('/movies/<int:movie_id>')
@requires_auth("get:movies-info")
def get_movie_by_id(payload, movie_id):
  movie = Movies.query.get_or_404(movie_id)

  return jsonify({
    "success": True,
    "movie": movie.full_info()
  }), 200

@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth("patch:movie")
def update_movie(payload, movie_id):
  movie = Movies.query.get_or_404(movie_id)

  try:
    request_body = request.get_json()
    if not bool(request_body):
      raise TypeError

    if "title" in request_body:
      if request_body["title"] == "":
        raise ValueError

      movie.title = request_body["title"]

    if "release_year" in request_body:
      if request_body["release_year"] <= 0:
        raise ValueError

      movie.release_year = request_body["release_year"]

    if "duration" in request_body:
      if request_body["duration"] <= 0:
        raise ValueError

      movie.duration = request_body["duration"]

    if "imdb_rating" in request_body:
        if request_body["imdb_rating"] < 0 \
                or request_body["imdb_rating"] > 10:
          raise ValueError

        movie.imdb_rating = request_body["imdb_rating"]

    if "cast" in request_body:
      if len(request_body["cast"]) == 0:
        raise ValueError

        actors = Actor.query.filter(
          Actor.name.in_(request_body["cast"])).all()

        if len(request_body["cast"]) == len(actors):
          movie.cast = actors
        else:
          raise ValueError

    movie.update()

    return jsonify({
      "success": True,
      "movie_info": movie.long()
    }), 200

  except (TypeError, ValueError, KeyError):
    abort(422)

  except Exception:
    abort(500)

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth("delete:movie")
def delete_movie(payload, movie_id):
  movie = Movies.query.get_or_404(movie_id)

  try:
    movie.delete()

    return jsonify({
      "success": True,
      "deleted_movie_id": movie.id
    }), 200

  except Exception:
    abort(500)

#--------------------------Error Handling------------------------#
@app.errorhandler(401)
def not_authorized(error):
  return jsonify({
      "success": False,
      "error": 401,
      "message": "Authentication error."
  }), 401

@app.errorhandler(403)
def forbidden(error):
  return jsonify({
      "success": False,
      "error": 403,
      "message": "Forbidden."
  }), 403

@app.errorhandler(404)
def not_found(error):
  return jsonify({
      "success": False,
      "error": 404,
      "message": "Item not found."
  }), 404

@app.errorhandler(422)
def unprocessable(error):
  return jsonify({
      "success": False,
      "error": 422,
      "message": "Request could not be processed."
  }), 422

@app.errorhandler(AuthError)
def auth_error(error):
  return jsonify({
      'success': False,
      'error': error.status_code,
      'message': error.error['description']
  }), error.status_code

#--------------------------App Entry-----------------------------#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)