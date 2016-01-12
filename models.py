from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from passlib.apps import custom_app_context as pwd_context

import random, string

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    password_hash = Column(String(64))
    email = Column(String)
    picture = Column(String)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid token but SignatureExpired
            print "valid token but SignatureExpired"
            return None
        except BadSignature:
            # Invalid token
            print "invalid token"
            return None
        user_id = data['id']
        return user_id

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'email': self.email
            'picture': self.picture
        }

class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key = True)
    mealType = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    mealTime = Column(String)
    filled = Column(Boolean)
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'meal type': self.mealType,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'meal time': self.mealTime,
            'filled': self.filled,
            'user id': self.user_id
        }

class Proposal(Base):
    __tablename__ = 'proposal'
    id = Column(Integer, primary_key = True)
    user_proposed_to = Column(Integer)
    user_proposed_from = Column(Integer)
    request = relationship(Request)
    request_id = Column(Integer, ForeignKey('request.id'))
    filled = Column(Boolean)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'user proposed to': self.user_proposed_to,
            'user proposed from': self.user_proposed_from,
            'request id': self.request_id,
            'filled': self.filled
        }

class MealDate(Base):
    __tablename__ = 'mealdate'
    id = Column(Integer, primary_key = True)
    user_1 = Column(Integer)
    user_2 = Column(Integer)
    restaurant_name = Column(String)
    restaurant_address = Column(String)
    restaurant_picture = Column(String)
    mealTime = Column(String)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'user 1': self.user_1,
            'user 2': self.user_2,
            'restaurant_name': self.restaurant_name,
            'restaurant_address': self.restaurant_address,
            'restaurant_picture': self.restaurant_picture,
            'meal time': self.mealType
        }


engine = create_engine('sqlite:///meetneat.db')

Base.metadata.create_all(engine)