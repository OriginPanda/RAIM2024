from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Colummn(db.Integer, db.ForeignKey('user.id'))
    #patient_id
    #data_id



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    notes = db.relationship('Comment')