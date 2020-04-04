## link to azure mysql database

from datetime import date

from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import bcrypt
from sqlalchemy import extract

builtin_list = list


db = SQLAlchemy()

def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

# [START model]

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255))
	password = db.Column(db.String(255))
	isMerchant = db.Column(db.String(1), default="N")

	@property
	def hash_password(self):
		return self.password

	@hash_password.setter
	def set_password(self, password):
		self.password = bcrypt.hashpw(password, bcrypt.gensalt())

	def verify_password(self, password):
		print("verifying")
		if bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')):
			print("Passwords match")
			return True
		else:
			print("Passwords don't match")
			return False

	def __repr__(self):
		return "<USer(name='%s')" % (self.username)

