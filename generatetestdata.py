from app import app,db,bcrypt
from app.models import User, Organization, Task, UserTask, UserCourse, Course, FeatureStat
from datetime import datetime, timedelta

with app.app_context():
    db.create_all()

    org_komodo = Organization(
        name="Komodo Hub", 
        org_type="Komodo", 
        description="The central administrative hub overseeing all community projects and educational workshops."
    )
    db.session.add(org_komodo)

    #Schools
    school1 = Organization(
        name="Coventry University", 
        org_type="School", 
        description="A public research university known for its focus on innovation, engineering, and automotive design."
    )
    school2 = Organization(
        name="Oakwood Secondary School", 
        org_type="School", 
        description="A high-performing academy dedicated to holistic student development and creative arts."
    )
    school3 = Organization(
        name="St. Andrews Primary", 
        org_type="School", 
        description="A local primary school focused on early-years literacy and community-based learning initiatives."
    )

    db.session.add_all([school1, school2, school3])

    #Communities
    comm1 = Organization(
        name="Solihull Tech Collective", 
        org_type="Community", 
        description="A grassroots group of developers and hobbyists sharing knowledge on AI, robotics, and open-source software."
    )
    comm2 = Organization(
        name="Green Heart Gardening Club", 
        org_type="Community", 
        description="A local urban gardening initiative focused on sustainable food growth and improving neighborhood green spaces."
    )

    db.session.add_all([comm1, comm2])    
    db.session.commit()



    #PASSWORD FOR EVERY USER
    hashed_pw = "$2b$12$uBbyy.3QHgfkZO.eHCn30OxkOPchwYTVL5oc5fxaqri1NLF8.Oqjy"  # Password: 12345678a@
    unverified_pw = "$2b$12$6JMRwXbRe0ThFH8Qm6/o1.O78lJqcaymo5NR1nXT2fitf69y3drue"



    #STAFF FOR KOMODO HUB

    sysadmin = User(
        email="sysadmin@example.com",
        first_name="System",
        last_name="Admin",
        password=hashed_pw,
        organization_id=org_komodo.id,
        role="Sysadmin",
        is_verified=True
    )

    manager = User(
        email="manager@example.com",
        first_name="Komodo",
        last_name="Manager",
        password=hashed_pw,
        organization_id=org_komodo.id,
        role="Manager",
        is_verified=True
    )


    db.session.add_all([sysadmin,manager])
    db.session.commit()

    #STAFF FOR COVENTRY UNIVERSITY
    admin_1 = User(
        email="admin@example.com",
        first_name="School",
        last_name="Admin",
        password=hashed_pw,
        organization_id=school1.id,
        role="Admin",
        is_verified=True
    )
    
    teacher_1 = User(
        email="teacher1@example.com",
        first_name="Bintang",
        last_name="Akbar",
        password=hashed_pw,
        organization_id=school1.id,
        role="Teacher",
        is_verified=True
    )

    student_1 = User(
        email="student1@example.com",
        first_name="First",
        last_name="Student",
        password=hashed_pw,
        organization_id=school1.id,
        role="Student",
        is_verified=True
    )

    student_2 = User(
        email="student2@example.com",
        first_name="Second",
        last_name="Student",
        password=hashed_pw,
        organization_id=school1.id,
        role="Student",
        is_verified=True
    )

    student_3 = User(
        email="student3@example.com",
        first_name="Third",
        last_name="Student",
        password=hashed_pw,
        organization_id=school1.id,
        role="Student",
        is_verified=False,
        uniqueAccessCode="12345678"
    )

    db.session.add_all([student_1, student_2, student_3, admin_1, teacher_1])
    db.session.commit()


    #Staff for Oakwood Secondary School
    admin_2 = User(
        email="admin2@example.com",
        first_name="School2",
        last_name="Admin",
        password=hashed_pw,
        organization_id=school2.id,
        role="Admin",
        is_verified=True
    )
    
    teacher_2 = User(
        email="teacher2@example.com",
        first_name="Bintang2",
        last_name="Akbar",
        password=hashed_pw,
        organization_id=school2.id,
        role="Teacher",
        is_verified=True
    )

    student_4 = User(
        email="student4@example.com",
        first_name="Fourth",
        last_name="Student",
        password=hashed_pw,
        organization_id=school2.id,
        role="Student",
        is_verified=True
    )

    db.session.add_all([admin_2,teacher_2,student_4])
    db.session.commit()



    #Staff for Solihull Tech Collective
    admin_3 = User(
        email="admin3@example.com",
        first_name="Community",
        last_name="Admin",
        password=hashed_pw,
        organization_id=comm1.id,
        role="Admin",
        is_verified=True
    )
    
    teacher_4 = User(
        email="teacher4@example.com",
        first_name="Bintang3",
        last_name="Akbar",
        password=hashed_pw,
        organization_id=comm1.id,
        role="Teacher",
        is_verified=True
    )

    member_1 = User(
        email="member1@example.com",
        first_name="Community",
        last_name="Member",
        password=hashed_pw,
        organization_id=comm1.id,
        role="Student",
        is_verified=True
    )

    db.session.add_all([admin_3,teacher_4,member_1])
    db.session.commit()

    #Individual Account (no org)
    individual = User(
        email="individual@example.com",
        first_name="Individual",
        last_name="Person",
        password=hashed_pw,
        is_verified=True
    )

    db.session.add(individual)
    db.session.commit()

    #Courses for Coventry university
    course_rhinos = Course(
    name="Wildlife Conservation: The Rhino Project", 
    description="A deep dive into the biological and environmental challenges facing modern rhinoceros populations and the global efforts to prevent their extinction.", 
    organization_id=school1.id
    )

    course_automotive = Course(
        name="Sustainable Automotive Design", 
        description="Exploring the future of transport through electric vehicle architecture, aerodynamics, and eco-friendly manufacturing processes.", 
        organization_id=school1.id
    )

    #Course for Solihull Tech Collective
    course_iot = Course(
        name="Smart Cities & IoT Workshop", 
        description="A hands-on community course focused on building low-cost environmental sensors using Arduino and Raspberry Pi to track local air quality.", 
        organization_id=comm1.id
    )

# Add and Commit
    db.session.add_all([course_rhinos, course_automotive, course_iot])
    db.session.commit()


    #Student 1 and Teacher 1 to Rhino Course
    enroll_1 = UserCourse(user_id=student_1.id, course_id=course_rhinos.id)
    enroll_2 = UserCourse(user_id=teacher_1.id, course_id=course_rhinos.id)

    #Student 2 to Automotive Course
    enroll_3 = UserCourse(user_id=student_2.id, course_id=course_automotive.id)

    #Member 1 to IoT Workshop
    enroll_4 = UserCourse(user_id=member_1.id, course_id=course_iot.id)

    db.session.add_all([enroll_1, enroll_2, enroll_3, enroll_4])
    db.session.commit()

#Remember to delete database before running this file to make sure all changes save
    

    