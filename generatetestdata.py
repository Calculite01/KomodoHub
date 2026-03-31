from app import app,db,bcrypt
from app.models import User, Organization, Classroom, Task, UserTask, UserClassroom, Announcement
from datetime import datetime, timedelta

with app.app_context():
    db.create_all()

    # Dummy Organisation
    org = Organization(name="Coventry University", org_type="School")
    db.session.add(org)
    db.session.commit()

    # Dummy classroom
    classroom = Classroom(name="Nature and allat", organization_id = org.id)
    db.session.add(classroom)
    db.session.commit()

    # Dummy task
    task = Task(name="finish this app bruh",classroom_id = classroom.id, due_date=datetime.now() + timedelta(minutes=5))
    db.session.add(task)
    db.session.commit()

    hashed_pw = "$2b$12$uBbyy.3QHgfkZO.eHCn30OxkOPchwYTVL5oc5fxaqri1NLF8.Oqjy"  # Password: 12345678a@

    admin = User(
        email="admin@example.com",
        first_name="School",
        last_name="Admin",
        password=hashed_pw,
        organization_id=org.id,
        role="Admin",
        is_verified=True
    )
    
    teacher = User(
        email="teacher1@example.com",
        first_name="Bintang",
        last_name="Akbar",
        password=hashed_pw,
        organization_id=org.id,
        role="Teacher",
        is_verified=True
    )

    student_1 = User(
        email="student1@example.com",
        first_name="First",
        last_name="Student",
        password=hashed_pw,
        organization_id=org.id,
        role="Student",
        is_verified=True
    )

    student_2 = User(
        email="student2@example.com",
        first_name="Second",
        last_name="Student",
        password=hashed_pw,
        organization_id=org.id,
        role="Student",
        is_verified=True
    )

    db.session.add_all([student_1, student_2, admin, teacher])
    db.session.commit()

    teacher_class = UserClassroom(user_id= teacher.id, classroom_id = classroom.id)
    student1_class = UserClassroom(user_id= student_1.id, classroom_id = classroom.id)
    student2_class = UserClassroom(user_id= student_2.id, classroom_id = classroom.id)
    db.session.add_all([teacher_class, student1_class, student2_class])

    student1_task = UserTask(user_id=student_1.id, task_id=task.id)
    student2_task = UserTask(user_id=student_2.id, task_id=task.id)
    db.session.add_all([student1_task, student2_task])
    db.session.commit()

    announcement = Announcement(title="Hello",text="Welcome to Coventry University",time_of_creation=datetime.now(), organization_id = org.id, user_id = admin.id)
    db.session.add(announcement)
    db.session.commit()

#Remember to delete database before running this file to make sure all changes save
    

    