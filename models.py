from flask_login import UserMixin
from db import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    aquariums = db.relationship("Aquarium", backref="user")


class Aquarium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    livestock = db.relationship("Livestock", backref="aquarium", cascade="all,delete")
    actions = db.relationship("Action", backref="aquarium", cascade="all,delete")


class Livestock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aquarium_id = db.Column(db.Integer, db.ForeignKey("aquarium.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_on = db.Column(db.Date, nullable=False)


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aquarium_id = db.Column(db.Integer, db.ForeignKey("aquarium.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    due_on = db.Column(db.Date, nullable=False)
