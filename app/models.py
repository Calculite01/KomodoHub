from app import db, app
from flask_login import UserMixin
from datetime import datetime
import os
from itsdangerous import URLSafeTimedSerializer as Serializer

class UserCourse(db.Model):
    __tablename__ = "user_course"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))


    user = db.relationship("User", backref="usercourses")
    course = db.relationship("Course", backref="usercoures")

class UserTask(db.Model):
    __tablename__ = "user_task"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    
    submitted = db.Column(db.Boolean, default=False)
    date_submitted = db.Column(db.DateTime, nullable=True)
    submission_file = db.Column(db.String(500), nullable=True)
    grade = db.Column(db.Integer, nullable=True)
    replies = db.relationship('TaskReply', backref='usertask', cascade="all, delete-orphan", lazy=True)

    user = db.relationship("User", backref="assigned_tasks")

class TaskReply(db.Model):
    __tablename__ = 'task_reply'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    time_of_creation = db.Column(db.DateTime, default=datetime.now, nullable=False)
    usertask_id = db.Column(db.Integer, db.ForeignKey('user_task.id'), nullable=False)

    user = db.relationship("User", backref="task_replies")

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(500), nullable=False)
    
    # Polymorphic columns
    parent_id = db.Column(db.Integer, nullable=False)
    parent_type = db.Column(db.String(50), nullable=False) # 'material', 'common_room', 'workshop', 'contribution'

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(500), nullable=False)
    
    # Polymorphic columns
    parent_id = db.Column(db.Integer, nullable=False)
    parent_type = db.Column(db.String(50), nullable=False) # 'material', 'workshop'

class User(db.Model,UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    acc_type = db.Column(db.String(20), nullable=False, default="Standard")
    image = db.Column(db.String(500), nullable=False, default='default_profile.jpg')
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    role = db.Column(db.String(20), nullable=False, default="None")
    contributions = db.relationship("Contribution", backref="user", lazy=True)
    sightings = db.relationship("Sighting", backref="user", lazy=True)
    is_verified = db.Column(db.Boolean(), nullable=False, default=False)
    uniqueAccessCode = db.Column(db.String(8), nullable=False, default="None")
    common_room_msgs = db.relationship('CommonRoomMessage', backref='user', lazy=True)
    common_room_replies = db.relationship('CommonRoomMessageReply', backref='user', lazy=True)
    contribution_replies = db.relationship('ContributionReply', backref='user', lazy=True)
    profile_pattern = db.Column(db.String(20),default='none')

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
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(500), nullable=True, default='default_org.jpg') 
    org_type = db.Column(db.String(20), nullable=False)
    users = db.relationship('User', backref='organization', lazy=True)

    def __repr__(self):
        return f"Organization('{self.id}','{self.name}')"
        
class ContactMessage(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key= True)
    first_name = db.Column(db.String(20), nullable= False)
    last_name = db.Column(db.String(20), nullable= False)
    email = db.Column(db.String(120), nullable= False)
    region = db.Column(db.String(60), nullable= False)
    userMessage = db.Column(db.Text, nullable= False)
    time_of_creation = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"ContactMessage({self.first_name} {self.last_name}: {self.userMessage})"

class OTP(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key= True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    otp = db.Column(db.String(6), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable = False)

class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, nullable = False, primary_key= True)
    name = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.DateTime)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    user_assignments = db.relationship("UserTask", backref="task", lazy=True)
    
class Course(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(500), nullable=True, default='default_course.jpg')
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    tasks = db.relationship('Task', backref='task', lazy=True)
    
    materials = db.relationship('Material', backref='course', lazy=True)
    workshopActivities = db.relationship('WorkshopActivity', backref='course', lazy=True)

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

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    is_visible = db.Column(db.Boolean, default=True)

    # FIXED: Added explicit foreign_keys and checked primaryjoin string
    images = db.relationship('Image', 
        primaryjoin="and_(Image.parent_id==Material.id, Image.parent_type=='material')",
        foreign_keys="Image.parent_id", overlaps="images", cascade="all, delete-orphan", lazy=True)
    
    files = db.relationship('File', 
        primaryjoin="and_(File.parent_id==Material.id, File.parent_type=='material')",
        foreign_keys="File.parent_id", overlaps="files", cascade="all, delete-orphan", lazy=True)

class CommonRoomMessage(db.Model):
    __tablename__ = 'common_room_message' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    time_of_creation = db.Column(db.DateTime, default=datetime.now, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    # FIXED: Added explicit foreign_keys
    images = db.relationship('Image', 
        primaryjoin="and_(Image.parent_id==CommonRoomMessage.id, Image.parent_type=='common_room_message')",
        foreign_keys="Image.parent_id", overlaps="images", cascade="all, delete-orphan", lazy=True)
    
    replies = db.relationship('CommonRoomMessageReply', backref='message', cascade="all, delete-orphan", lazy=True)

class CommonRoomMessageReply(db.Model):
    __tablename__ = 'common_room_message_reply'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    time_of_creation = db.Column(db.DateTime, default=datetime.now, nullable=False)
    common_room_message_id = db.Column(db.Integer, db.ForeignKey('common_room_message.id'), nullable=False)

class WorkshopActivity(db.Model):
    __tablename__ = 'workshop_activity'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    time_of_creation = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # FIXED: Added explicit foreign_keys
    images = db.relationship('Image', 
        primaryjoin="and_(Image.parent_id==WorkshopActivity.id, Image.parent_type=='workshop')",
        foreign_keys="Image.parent_id", overlaps="images", cascade="all, delete-orphan", lazy=True)
    
    files = db.relationship('File', 
        primaryjoin="and_(File.parent_id==WorkshopActivity.id, File.parent_type=='workshop')",
        foreign_keys="File.parent_id", overlaps="files", cascade="all, delete-orphan", lazy=True)
    
    contributions = db.relationship('Contribution', backref='workshop', lazy=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

class Contribution(db.Model):
    __tablename__ = 'contribution'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_of_creation = db.Column(db.DateTime, default=datetime.now)
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop_activity.id'))
    replies = db.relationship('ContributionReply', backref='message', cascade="all, delete-orphan", lazy=True)
    moderated = db.Column(db.Boolean, default=False)

    # FIXED: Added explicit foreign_keys
    images = db.relationship('Image', 
        primaryjoin="and_(Image.parent_id==Contribution.id, Image.parent_type=='contribution')",
        foreign_keys="Image.parent_id", overlaps="images", cascade="all, delete-orphan", lazy=True)

class ContributionReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    time_of_creation = db.Column(db.DateTime, default=datetime.now, nullable=False)
    contribution_id = db.Column(db.Integer, db.ForeignKey('contribution.id'), nullable=False)

class Sighting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500), nullable=False, default='default_sighting.jpg')
    description = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Sighting('{self.title}', '{self.date_posted}')"

class FeatureStat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_visits = db.Column(db.Integer, default=0)
    program_visits = db.Column(db.Integer, default=0)
    common_room_visits = db.Column(db.Integer, default=0)