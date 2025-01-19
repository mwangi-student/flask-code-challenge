from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


class Users(db.Model):
    __tablename__ = "Users"  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    houses = db.relationship("House", backref="owner", lazy=True)


class House(db.Model):
    __tablename__ = "House"  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    size = db.Column(db.String(80), nullable=False)
    house_photo = db.Column(db.String(80), nullable=False)
    rent = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"  
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
