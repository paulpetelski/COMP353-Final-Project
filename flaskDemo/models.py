from datetime import datetime
from flaskDemo import db
#from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

class Product(db.Model):
    __table__ = db.Model.metadata.tables['product']