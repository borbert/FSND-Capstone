import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db_create_all, return_db, Item, List, User

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
@app.route('/', methods=['GET'])
def all_lists():
  try:
    lists = List.query.all()
    if lists:
      data = [List.long() for list in lists]
      return jsonify(
        {
          'success':True,
          'data': data
        }
      )
    else:
      return "No lists created"
  except Exception as e:
    print(e)
    abort(404)

  

@app.route('/auth')
def auth():
  return 'auth Not implemented'

@app.route('/contents')
def contents():
  return 'contents Not implemented'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)