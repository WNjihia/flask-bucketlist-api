"""models.py."""
import jwt
import os

from bucketlist import db, app
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash


class User(db.Model):
    """This class represents the user table."""

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128))
    bucketlist = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def set_password(self, password):
        """Hash the password."""
        pw_hash = generate_password_hash(password)
        return pw_hash

    def encode_auth_token(self, id):
        """Generate the Auth Token."""
        try:
            expire_date = datetime.utcnow() + timedelta(days=0, minutes=10)
            payload = {
                'exp': expire_date,
                'iat': datetime.utcnow(),
                'sub': id
            }
            return jwt.encode(
                payload,
                os.getenv('SECRET') or 'ohsoverysecret',
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decode the auth token and verify the signature."""
        try:
            payload = jwt.decode(auth_token, os.getenv('SECRET') or 'ohsoverysecret')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature Expired. Try log in again'
        except jwt.InvalidTokenError:
            return 'Invalid Token. Try log in again'


class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    bucketlist_title = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now,
                              onupdate=datetime.now)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item',
                            backref=db.backref('bucketlists'),
                            cascade="all, delete-orphan")

    def __repr__(self):
        """Return printable representation of the object."""
        return "Bucketlist: {}}".format(self.bucketlist_title)

    def save(self):
        """Save a bucketlist."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a bucketlist."""
        db.session.delete(self)
        db.session.commit()


class Item(db.Model):
    """This class represents the items table."""

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.now)
    modified_date = db.Column(db.DateTime, default=datetime.now,
                              onupdate=datetime.now)
    bucketlist_id = db.Column(db.Integer,
                              db.ForeignKey('bucketlists.id'))

    def __repr__(self):
        """Return printable representation of the object."""
        return "Item: {}".format(self.item_name)

    def save(self):
        """Save an item."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete an item."""
        db.session.delete(self)
        db.session.commit()
