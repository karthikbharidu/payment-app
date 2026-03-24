from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

db= SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = False)
    mobile = db.Column(db.String(50), nullable = False)
    role = db.Column(db.String(100), nullable = False, default = 'user')

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email
        }

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):

        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount':self.amount,
            'status':self.amount,
            'timestamp':str(self.timestamp)
        }

class User_details(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(20), nullable = False)
    mobile = db.Column(db.String(20), nullable = False)

