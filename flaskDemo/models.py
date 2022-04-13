from datetime import datetime
from flaskDemo import db
#from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

# add tables
class Product(db.Model):
    __table__ = db.Model.metadata.tables['product']
class Book(db.Model):
    __table__ = db.Model.metadata.tables['book']
class Customer(db.Model):
    __table__ = db.Model.metadata.tables['customer']
class Department(db.Model):
    __table__ = db.Model.metadata.tables['department']
class Employee(db.Model):
    __table__ = db.Model.metadata.tables['employee']
class Orderline(db.Model):
    __table__ = db.Model.metadata.tables['orderline']
class Orders(db.Model):
    __table__ = db.Model.metadata.tables['orders']
class Publisher(db.Model):
    __table__ = db.Model.metadata.tables['publisher']
class Subscription(db.Model):
    __table__ = db.Model.metadata.tables['subscription']