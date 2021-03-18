import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db_create_all, return_db, Item, List, User
from auth import requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app) #, resources={r"/api/": {"origins": "*"}}

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
#--------------------------Get METHODS------------------------#
'''
GET / endpoint
    This is a public endpoint that represents the list model with the short() description method.
    This returns status code 200 and json {"success": True, "lists": lists} where list is the
    list of lists.
Returns:
    Status code 200 and list of lists.
'''
@app.route('/', methods=['GET'])
def all_lists():
  return 'index where lists are'

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
@app.route('/my_lists', methods=['GET'])
@requires_auth('get:lists')
def my_lists(payload):
  return 'auth implemented'

@app.route('/add_item', methods=['POST'])
@requires_auth('post:item')
def add_item(payload):
  return 'auth implemented'

@app.route('/contents')
@requires_auth('post:store')
def contents():
  return 'contents implemented'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)