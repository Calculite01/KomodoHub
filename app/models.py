from app import db, app
from flask_login import UserMixin
from datetime import datetime
import os
from itsdangerous import URLSafeTimedSerializer as Serializer

class UserClassroom(db.Model):
    __tablename__ = "user_classroom"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    classroom_id = db.Column(db.Integer, db.ForeignKey("classroom.id"))


    user = db.relationship("User", backref="userclassrooms")
    classroom = db.relationship("Classroom", backref="userclassrooms")

class UserTask(db.Model):
    __tablename__ = "user_task"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))

    submitted = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref="usertasks")
    task = db.relationship("Task", backref="usertasks")

class User(db.Model,UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    acc_type = db.Column(db.String(20), nullable=False, default="Standard")
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    role = db.Column(db.String(20), nullable=False, default="None")
    contributions = db.relationship("Contribution", backref="user", lazy=True)
    #classrooms = db.relationship('UserClassroom', backref='user')
    #tasks = db.relationship('UserTask', backref='user', secondary="user_task")
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
    users = db.relationship('User', backref='organization', lazy=True)
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
    __tablename__ = "classroom"

    id = db.Column(db.Integer, nullable = False, primary_key= True)
    name = db.Column(db.String(50))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable = False)
    #users = db.relationship('UserClassroom', backref='classroom', secondary="user_classroom")
    tasks = db.relationship('Task', backref='classroom', lazy=True)

class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, nullable = False, primary_key= True)
    name = db.Column(db.String(50))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    #users = db.relationship('UserTask', backref='task')
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



class Messages(db.Model):
    id = db.Column(db.Integer, nullable= False, primary_key= True)
    text = db.Column(db.String(500), nullable= False)
    timestamp = db.Column(db.DateTime, default= datetime.now)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)            # link message to sender (user)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)          # link message to recipient (user)
    sender = db.relationship('User', foreign_keys= [sender_id], backref= 'sent_messages')               # backref allows u to see the messages each 'User' instance has sent
    receiver = db.relationship('User', foreign_keys= [receiver_id], backref= 'received_messages')       # backref allows u to see the messages each 'User' instance has received

    def __repr__(self):
        return f"Sender {self.sender_id} sent {self.receiver_id} the text:\n{self.text} to {self.receiver_id}"

class GlobalMesssages(db.Model):
    id = db.Column(db.Integer, nullable= False, primary_key= True)
    text = db.Column(db.String(500), nullable= False)
    timestamp = db.Column(db.DateTime, default= datetime.now)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    sender = db.relationship('User', backref= db.backref('messages', lazy= True))

with app.app_context():
    if not os.path.exists('komodohub.db'):
        db.create_all()
