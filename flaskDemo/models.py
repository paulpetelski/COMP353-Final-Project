from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm
from flask_login import LoginManager

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


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(id))


class Users(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
     __table_args__ = {'extend_existing': True}
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100), nullable=False)
     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
     content = db.Column(db.Text, nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

     def __repr__(self):
         return f"Post('{self.title}', '{self.date_posted}')"
