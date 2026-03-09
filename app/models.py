from app import db, app
from flask_login import UserMixin
from datetime import datetime
import os
from itsdangerous import URLSafeTimedSerializer as Serializer

user_classroom = db.Table('user_classroom',
    db.Column('user_id',db.Integer,db.ForeignKey('classroom.id')),
    db.Column('classroom_id',db.Integer,db.ForeignKey('user.id'))
)

user_task = db.Table('user_task',
    db.Column('user_id',db.Integer,db.ForeignKey('task.id')),
    db.Column('task_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('submitted',db.Boolean())
)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    acc_type = db.Column(db.String(20), nullable=False, default="Standard")
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False ,default="None")
    role = db.Column(db.String(20), nullable=False, default="None")
    contributions = db.relationship("Contribution", backref="user", lazy=True)
    classrooms = db.relationship('Classroom', secondary=user_classroom, backref='user')
    tasks = db.relationship('Task', secondary=user_task, backref='user')
    announcements = db.relationship('Announcement', backref='user', lazy=True)
    is_verified = db.Column(db.Boolean(), nullable=False, default=False)
    uniqueAccessCode = db.Column(db.String(8), nullable=False, default="None")

    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=600):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None

        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.id}','{self.email}','{self.first_name}', '{self.last_name}', '{self.password}', '{self.acc_type}', '{self.is_verified}')"
    
class Organization(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    org_type = db.Column(db.String(20), nullable=False)
    users = db.relationship('Organization', backref='organization', lazy=True)
    classrooms = db.relationship('Classroom', backref='organization', lazy=True)
    announcements = db.relationship('Announcement', backref='organization', lazy=True)

    def __repr__(self):
        return f"Organization('{self.id}','{self.name}')"
    
class Announcement(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(1000), nullable=False)
    images = db.relationship('AnnouncementImage', backref='announcement', lazy=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    time_of_creation = db.Column(db.DateTime, default=datetime.now())

class AnnouncementImage(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False)
    announcement_id = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    

class ContactMessage(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key= True)
    first_name = db.Column(db.String(20), nullable= False)
    last_name = db.Column(db.String(20), nullable= False)
    email = db.Column(db.String(120), nullable= False)
    region = db.Column(db.String(60), nullable= False)
    userMessage = db.Column(db.Text, nullable= False)
    time_of_creation = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"ContactMessage({self.first_name} {self.last_name}: {self.userMessage})"

class OTP(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key= True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    otp = db.Column(db.String(6), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable = False)

class Classroom(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key= True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable = False)
    users = db.relationship('User', secondary=user_classroom, backref='classroom')
    tasks = db.relationship('Task', backref='classroom', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key= True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    users = db.relationship('User', secondary=user_task, backref='task')
    due_date = db.Column(db.DateTime)


class Program(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key= True)
    contributions = db.relationship('Contribution', backref='program', lazy=True)

    
class Contribution(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key= True)
    contribution_type = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(1000))
    images = db.relationship('ContributionImage', backref='contribution', lazy=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_of_creation = db.Column(db.DateTime, default=datetime.now())

class ContributionImage(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key= True)
    image_file = db.Column(db.String(20), nullable=False)
    contribution_id = db.Column(db.Integer, db.ForeignKey('contribution.id'), nullable=False)



with app.app_context():
    if not os.path.exists('komodohub.db'):
        db.create_all()
