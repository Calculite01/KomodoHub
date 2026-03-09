from app import app,db,bcrypt
from app.models import User, Organization, Classroom, Task, UserTask, UserClassroom, Announcement
from datetime import datetime, timedelta

with app.app_context():
    # user = User.query.get(1)
    # usertasks = UserTask.query.filter_by(user_id=user.id,task_id=1)
    # for ut in usertasks:
    #     print(ut.task.name,ut.submitted)
    db.create_all()
    org = Organization(name="Coventry University",org_type="School")
    db.session.add(org)
    db.session.commit()
    classroom = Classroom(name="Nature and allat",organization_id = org.id)
    db.session.add(classroom)
    db.session.commit()
    task = Task(name="finish this app bruh",classroom_id = classroom.id, due_date=datetime.now() + timedelta(minutes=5))
    db.session.add(task)
    db.session.commit()
    user = User(email= "saadwajid401@gmail.com",
                    first_name= "Saad",
                    last_name= "Wajid",
                    password= "$2b$12$uBbyy.3QHgfkZO.eHCn30OxkOPchwYTVL5oc5fxaqri1NLF8.Oqjy",
                    organization_id = org.id,
                    role = "Student",
                    is_verified = True)
    db.session.add(user)
    db.session.commit()
    usertask = UserTask(user_id=user.id,task_id=task.id)
    userclassroom = UserClassroom(user_id=user.id,classroom_id=classroom.id)
    db.session.add_all([usertask,userclassroom])
    db.session.commit()
    announcement = Announcement(title="Hello",text="Welcome to Coventry University",time_of_creation=datetime.now(), organization_id = org.id, user_id = user.id)
    db.session.add(announcement)
    db.session.commit()

#Remember to delete database before running this file to make sure all changes save
    

    