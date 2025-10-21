#used to create database models

from . import db #importing db from __init__.py
from flask_login import UserMixin
from sqlalchemy.sql import func 

class Biddings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   #user id of user who has placed highest bid 


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(100))
    data = db.Column(db.String(10000))
    bprice = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    state = db.Column(db.String(100))
    address = db.Column(db.String(150))
    listings = db.relationship('Listing')


