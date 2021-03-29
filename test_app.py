import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actor, db_drop_and_create_all
import configparser

config=configparser.ConfigParser()
config.read('config.ini')

#tokens for testing
casting_assistant_token=config["bearer_tokens"]['casting_assistant'] 
casting_director_token=config["bearer_tokens"]['casting_director']
executive_producer_token=config["bearer_tokens"]['executive_producer']
# casting_assistant="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ4T280WUI3M2dMdFhTV0p3Ym4xYiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtcHJvamVjdDMtYm9yYmVydC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxNzYyNDQ5ZGJkMWEwMDY4ZjBhZGZkIiwiYXVkIjoiaHR0cDovLzEyNy4wLjAuMTo1MDAwIiwiaWF0IjoxNjE2OTYxNjQyLCJleHAiOjE2MTY5NzE2NDIsImF6cCI6IkV5d21haktHdzdkVFJ2eU9SblE5VmNnZ2pSU2UxWXBlIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.zJzxhVXv3tZApip_nu3NB8i1qFIjBpPbOVu7_dK0dFPPNmwEqtPZGoI8k3inBvDQhxqgshiZcZPSEC3KQnIRpCnCSgO4QPUB6g7fHKm_e604AXbdGHwM4I-OpOJQ4qYmTdSJFsEgH_4VeyL8CAiVy4cVPUi2BRPIbrSRbxnDC7pBVdc0ZGf5A4efEYrv3pqZb5IX0hgof79YqCb2Qy0_2TAxj1rCe8y9hCmfE_CReMXSaGryr2W-oqpLwHAl02Vy6yRMathWm9br8mqErGecQJ1QyYMn325LD08K7wviYNTJpDyKk8kh9g7yXFiBOyCPCXeHJWeDmCtEXJ8KpA0aWQ"
# casting_director="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ4T280WUI3M2dMdFhTV0p3Ym4xYiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtcHJvamVjdDMtYm9yYmVydC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxNzY1ZDJkZjdiNWEwMDcxOGU2NTA2IiwiYXVkIjoiaHR0cDovLzEyNy4wLjAuMTo1MDAwIiwiaWF0IjoxNjE2OTYyMjM1LCJleHAiOjE2MTY5NzIyMzUsImF6cCI6IkV5d21haktHdzdkVFJ2eU9SblE5VmNnZ2pSU2UxWXBlIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.p9zkNXs3eug0yEpbZRRodZQpXCthT3wueukoe6Hy2ZBk1aQsOyaX0xREZ8j2To5R1yNXGwVx6v_FmkP9jz-_W_V5fXMAvwC4O-5zXphL6j6g-gLa1IafADLDdHmw8NZDbsKATJwR8QSq9Z_tiKQgvHW6-vEexT7Km3YGsDiwfqlJto7DE-qVbP5h4sN9wLm5YfNjfaYz-7AM0SmYf26Qh0fmfew7vmjb4TSWm4-3dzcF1roaYukrD25p_zQ6n9waEPs7ry8rl7CXFeeIXWwJL4kNCT-1crs0juqXoIarT4X0maUOYfe6bbqIvQzmotYIFLheHuEwYMaD19zQX90qDg"
# executive_producer="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ4T280WUI3M2dMdFhTV0p3Ym4xYiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtcHJvamVjdDMtYm9yYmVydC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDMwNTUyMjg3Njk0NjU2NTU5NjAiLCJhdWQiOiJodHRwOi8vMTI3LjAuMC4xOjUwMDAiLCJpYXQiOjE2MTY5NjQ4MDcsImV4cCI6MTYxNzA1MTIwNywiYXpwIjoiRXl3bWFqS0d3N2RUUnZ5T1JuUTlWY2dnalJTZTFZcGUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.cLy2EFLn7276biMXSUU2lY6PM_lwCdH-MuYL26jz0XEfzNLUJ6WE6xOJmWtp1qfmJ4P_gkMXKgE8-HCtVt4PoarMj4VpyfEn6n69yCyN65TgEamLT2o1EumytJ8nAwAtyDRB7wZKKezsfAQ_qAL_oIJ3sPh_qzWQZpvvOL6gpw5uwlGYxKPLQnAexOv9YUJUqA2s-tM0qMjWdUbDg4NXQnEGvi4v_L4oPCi_oeuGk2Uue32ciAHMrDszEmu2ORSnUQZBryvrigeLrVSt06bOQqGcEM25MjM5i3JJu7MUGbulUWR2AijAapA6yDuGCOYUMffaxTHKgG-x7VtmbbrKjA"

database_name = os.getenv('DATABASE_NAME',default='test_agency_db')
db_user = os.getenv('DB_USER',default='postgres')
db_pass = os.getenv('DB_PASS',default=None)
db_host = os.getenv('DB_HOST', default='localhost')
port = os.getenv('PORT',default=5432)
database_path = os.getenv(
    'DATABASE_URL',default="postgres://{}:{}@{}:{}/{}".format(
        db_user,db_pass,db_host, port, database_name))


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.casting_assistant_token=config["bearer_tokens"]['casting_assistant'] 
        self.casting_director_token=config["bearer_tokens"]['casting_director']
        self.executive_producer_token=config["bearer_tokens"]['executive_producer']
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.VALID_NEW_ACTOR = {
            "name": "Ana de Armas",
            "full_name": "Ana Celia de Armas Caso",
            "date_of_birth": "April 30, 1988"
        }

        self.INVALID_NEW_ACTOR = {
            "name": "Ana de Armas"
        }

        self.VALID_UPDATE_ACTOR = {
            "full_name": "Anne Hathaway"
        }

        self.INVALID_UPDATE_ACTOR = {}

        self.VALID_NEW_MOVIE = {
            "title": "Suicide Squad",
            "duration": 137,
            "release_year": 2016,
            "imdb_rating": 6,
            "cast": ["Margot Robbie"]
        }

        self.INVALID_NEW_MOVIE = {
            "title": "Knives Out",
            "imdb_rating": 7.9,
            "cast": ["Ana de Armas"]
        }

        self.VALID_UPDATE_MOVIE = {
            "imdb_rating": 6.5
        }

        self.INVALID_UPDATE_MOVIE = {}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_health(self):
        """Test for GET / (health endpoint)"""
        res = self.client().get('/')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('health', data)
        self.assertEqual(data['health'], 'Running!!')

    # def test_api_call_without_token(self):
    #     """Failing Test trying to make a call without token"""
    #     res = self.client().get('/actors')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data["success"])
    #     self.assertEqual(data["message"], "Authorization Header is required.")

    # def test_get_actors(self):
    #     """Passing Test for GET /actors"""
    #     res = self.client().get('/actors', headers={
    #         'Authorization': "Bearer {}".format(self.casting_assistant_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(len(data))
    #     self.assertTrue(data["success"])
    #     self.assertIn('actors', data)
    #     self.assertTrue(len(data["actors"]))

    # def test_get_actors_by_id(self):
    #     """Passing Test for GET /actors/<actor_id>"""
    #     res = self.client().get('/actors/1', headers={
    #         'Authorization': "Bearer {}".format(self.user_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('actor', data)
    #     self.assertIn('full_name', data['actor'])
    #     self.assertTrue(len(data["actor"]["movies"]))

    # def test_404_get_actors_by_id(self):
    #     """Failing Test for GET /actors/<actor_id>"""
    #     res = self.client().get('/actors/100', headers={
    #         'Authorization': "Bearer {}".format(self.user_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_create_actor_with_user_token(self):
    #     """Failing Test for POST /actors"""
    #     res = self.client().post('/actors', headers={
    #         'Authorization': "Bearer {}".format(self.user_token)
    #     }, json=self.VALID_NEW_ACTOR)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data["success"])
    #     self.assertIn('message', data)

    # def test_create_actor(self):
    #     """Passing Test for POST /actors"""
    #     res = self.client().post('/actors', headers={
    #         'Authorization': "Bearer {}".format(self.manager_token)
    #     }, json=self.VALID_NEW_ACTOR)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 201)
    #     self.assertTrue(data["success"])
    #     self.assertIn('created_actor_id', data)

    # def test_422_create_actor(self):
    #     """Failing Test for POST /actors"""
    #     res = self.client().post('/actors', headers={
    #         'Authorization': "Bearer {}".format(self.manager_token)
    #     }, json=self.INVALID_NEW_ACTOR)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_update_actor_info(self):
    #     """Passing Test for PATCH /actors/<actor_id>"""
    #     res = self.client().patch('/actors/1', headers={
    #         'Authorization': "Bearer {}".format(self.manager_token)
    #     }, json=self.VALID_UPDATE_ACTOR)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('actor_info', data)
    #     self.assertEqual(data["actor_info"]["full_name"],
    #                      self.VALID_UPDATE_ACTOR["full_name"])

    # def test_422_update_actor_info(self):
    #     """Failing Test for PATCH /actors/<actor_id>"""
    #     res = self.client().patch('/actors/1', headers={
    #         'Authorization': "Bearer {}".format(self.manager_token)
    #     }, json=self.INVALID_UPDATE_ACTOR)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_delete_actor_with_manager_token(self):
    #     """Failing Test for DELETE /actors/<actor_id>"""
    #     res = self.client().delete('/actors/5', headers={
    #         'Authorization': "Bearer {}".format(self.manager_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data["success"])
    #     self.assertIn('message', data)

    # def test_delete_actor(self):
    #     """Passing Test for DELETE /actors/<actor_id>"""
    #     res = self.client().delete('/actors/5', headers={
    #         'Authorization': "Bearer {}".format(self.admin_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('deleted_actor_id', data)

    # def test_404_delete_actor(self):
    #     """Passing Test for DELETE /actors/<actor_id>"""
    #     res = self.client().delete('/actors/100', headers={
    #         'Authorization': "Bearer {}".format(self.admin_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_get_movies(self):
    #     """Passing Test for GET /movies"""
    #     res = self.client().get('/movies', headers={
    #         'Authorization': "Bearer {}".format(self.user_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(len(data))
    #     self.assertTrue(data["success"])
    #     self.assertIn('movies', data)
    #     self.assertTrue(len(data["movies"]))

    # def test_get_movie_by_id(self):
    #     """Passing Test for GET /movies/<movie_id>"""
    #     res = self.client().get('/movies/1', headers={
    #         'Authorization': "Bearer {}".format(self.user_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('movie', data)
    #     self.assertIn('imdb_rating', data['movie'])
    #     self.assertIn('duration', data['movie'])
    #     self.assertIn('cast', data['movie'])
    #     self.assertTrue(len(data["movie"]["cast"]))

    # def test_404_get_movie_by_id(self):
    #     """Failing Test for GET /movies/<movie_id>"""
    #     res = self.client().get('/movies/100', headers={
    #         'Authorization': "Bearer {}".format(self.user_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_create_movie_with_user_token(self):
    #     """Failing Test for POST /movies"""
    #     res = self.client().post('/movies', headers={
    #         'Authorization': "Bearer {}".format(self.user_token)
    #     }, json=self.VALID_NEW_MOVIE)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data["success"])
    #     self.assertIn('message', data)

    # def test_create_movie(self):
    #     """Passing Test for POST /movies"""
    #     res = self.client().post('/movies', headers={
    #         'Authorization': "Bearer {}".format(self.manager_token)
    #     }, json=self.VALID_NEW_MOVIE)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 201)
    #     self.assertTrue(data["success"])
    #     self.assertIn('created_movie_id', data)

    # def test_422_create_movie(self):
    #     """Failing Test for POST /movies"""
    #     res = self.client().post('/movies', headers={
    #         'Authorization': "Bearer {}".format(self.manager_token)
    #     }, json=self.INVALID_NEW_MOVIE)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_update_movie_info(self):
    #     """Passing Test for PATCH /movies/<movie_id>"""
    #     res = self.client().patch('/movies/1', headers={
    #         'Authorization': "Bearer {}".format(self.manager_token)
    #     }, json=self.VALID_UPDATE_MOVIE)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('movie_info', data)
    #     self.assertEqual(data["movie_info"]["imdb_rating"],
    #                      self.VALID_UPDATE_MOVIE["imdb_rating"])

    # def test_422_update_movie_info(self):
    #     """Failing Test for PATCH /movies/<movie_id>"""
    #     res = self.client().patch('/movies/1', headers={
    #         'Authorization': "Bearer {}".format(self.manager_token)
    #     }, json=self.INVALID_UPDATE_MOVIE)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_delete_movie_with_manager_token(self):
    #     """Failing Test for DELETE /movies/<movie_id>"""
    #     res = self.client().delete('/movies/3', headers={
    #         'Authorization': "Bearer {}".format(self.manager_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data["success"])
    #     self.assertIn('message', data)

    # def test_delete_movie(self):
    #     """Passing Test for DELETE /movies/<movie_id>"""
    #     res = self.client().delete('/movies/3', headers={
    #         'Authorization': "Bearer {}".format(self.admin_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('deleted_movie_id', data)

    # def test_404_delete_movie(self):
    #     """Passing Test for DELETE /movies/<movie_id>"""
    #     res = self.client().delete('/movies/100', headers={
    #         'Authorization': "Bearer {}".format(self.admin_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()