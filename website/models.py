'''
Created on Jul 4, 2022

@author: chelseanieves

Purpose: Creates and manages User database model
'''
from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    '''defines database schema'''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True) # unique to prevent duplicate email entries
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    