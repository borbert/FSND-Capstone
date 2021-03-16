import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_name = os.getenv('DATABASE_NAME',default='listapp_dev')
db_user = os.getenv('DB_USER',default='postgres')
db_pass = os.getenv('DB_PASS',default=None)
db_host = os.getenv('DB_HOST', default='localhost')
port = os.getenv('PORT',default=5432)
database_path = os.getenv(
    'DATABASE_URL',default="postgres://{}:{}@{}:{}/{}".format(
        db_user,db_pass,db_host, port, database_name))
# "postgres://{}:{}@{}/{}".format(db_user,db_pass,db_host, database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app,db)

def return_db():
    return db
    
def db_create_all():
    db.create_all()

'''
Models
'''

class User(db.Model):
    __tablename__ = 'users'
    # username = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    description = db.Column(db.Text())
    token = db.Column(db.String(250))
    user_lists = db.relationship('List',order_by='List.list_id')


    def __init__(self, email,
                 password, firstname="",
                 lastname="", description=""):
        # self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.description = description
        self.token = ""

    def add(self):
        """
        This method add a new record to the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        """
        This method update a new record to the database
        :return:
        """
        db.session.commit()

    def delete(self):
        """
        This method deletes a record from the database
        :return:
        """
        db.session.delete(self)
        db.session.commit()


class Item(db.Model):
    __tablename__ = 'item'

    item_id = Column(db.Integer, primary_key=True)
    prod_description = db.Column(db.String)
    category = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    favorite = db.Column(db.Boolean)
    stores = db.Column(db.ARRAY(db.String()))
    barcode = db.Column(db.String(500))
    lists = db.relationship('List', backref='Items')

    def __repr__(self):
        return f'<Item {self.name}: ID {self.item_id}>'

    '''
    add a new item
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def long(self):
        return {
        'id': self.id,
        'prod_description': self.prod_description,
        'category': self.category,
        'favorite': self.favorite,
        'stores': self.stores,
        'lists':self.lists,
        }
        

class List(db.Model):
    __tablename__ = 'lists'

    list_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    list_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text())
    # store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    date_added = db.Column(db.DateTime, nullable=False)
    date_completed = db.Column(db.DateTime, nullable=True)
    complete = db.Column(db.Boolean)
    list_items = db.relationship('Item', order_by='Item.item_id')

    def __init__(self, list_name, user_id, description=""):
        # self.list_id = list_id
        self.list_name = list_name
        self.user_id = user_id
        self.description = description

    def __repr__(self):
        return f'<List {self.id}-{self.list_name}>'

    '''
    create a new list
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def long(self):
        return {
                'id':self.id,
                'items':self.items,
                'store_id':self.store_id,
                'complete':self.complete,
                'date_completed':self.date_completed,
            }
        

# class Store(db.Model):
#     __tablename__ = 'store'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     website = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     api = db.Column(db.Boolean)
#     favorite = db.Column(db.Boolean)
#     items = db.relationship('Item', backref='Stores', lazy=True)
#     lists = db.relationship('List', backref='Stores', lazy=True)

#     def __repr__(self):
#         return f'<Artist {self.name}>'