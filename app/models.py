from app import db, app
from flask_login import UserMixin
from datetime import datetime
import os

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    acc_type = db.Column(db.String(20), nullable=False)
    is_verified = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return f"User('{self.id}','{self.email}','{self.first_name}', '{self.last_name}', '{self.password}', '{self.acc_type}', '{self.is_verified}')"
    
class Organization(db.Model,UserMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    og_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Organization('{self.id}','{self.name}')"

class ContactMessage(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key= True)
    first_name = db.Column(db.String(20), nullable= False)
    last_name = db.Column(db.String(20), nullable= False)
    email = db.Column(db.String(120), nullable= False)
    region = db.Column(db.String(60), nullable= False)
    userMessage = db.Column(db.Text, nullable= False)
    time_of_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ContactMessage({self.first_name} {self.last_name}: {self.userMessage})"

with app.app_context():
    if not os.path.exists('komodohub.db'):
        db.create_all()

# Todo: implement DB storage for OTPs
otp_storage = {}    # stores OTPs for verification of user entered OTP