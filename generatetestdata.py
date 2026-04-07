import os

db_path = os.path.join("instance", "komodohub.db")

#Delete the database file if it exists
if os.path.exists(db_path):
    os.remove(db_path)


from app import app,db,bcrypt
from app.models import User, Organization, Task, UserTask, UserCourse, Course, FeatureStat, Contribution, Sighting, Material, CommonRoomMessage
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

    db.session.add_all([school1, school2])

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
    #Password: 12345678a@
    hashed_pw = "$2b$12$uBbyy.3QHgfkZO.eHCn30OxkOPchwYTVL5oc5fxaqri1NLF8.Oqjy"

    #IGNORE THIS
    unverified_pw = "$2b$12$6JMRwXbRe0ThFH8Qm6/o1.O78lJqcaymo5NR1nXT2fitf69y3drue" 

# STAFF FOR KOMODO HUB
    sysadmin = User(
        email="sysadmin@example.com",
        first_name="Marcus",
        last_name="Vance",
        password=hashed_pw,
        organization_id=org_komodo.id,
        role="Sysadmin",
        is_verified=True
    )

    manager = User(
        email="manager@example.com",
        first_name="Elena",
        last_name="Rodriguez",
        password=hashed_pw,
        organization_id=org_komodo.id,
        role="Manager",
        is_verified=True
    )

    db.session.add_all([sysadmin, manager])
    db.session.commit()

    # STAFF FOR COVENTRY UNIVERSITY (school1)
    admin_1 = User(
        email="admin@example.com",
        first_name="Sarah",
        last_name="Jenkins",
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
        first_name="Liam",
        last_name="Thompson",
        password=hashed_pw,
        organization_id=school1.id,
        role="Student",
        is_verified=True
    )

    student_2 = User(
        email="student2@example.com",
        first_name="Chloe",
        last_name="Whitaker",
        password=hashed_pw,
        organization_id=school1.id,
        role="Student",
        is_verified=True
    )

    student_3 = User(
        email="student3@example.com",
        first_name="Amara",
        last_name="Okonjo",
        password=hashed_pw,
        organization_id=school1.id,
        role="Student",
        is_verified=False,
        uniqueAccessCode="12345678"
    )

    db.session.add_all([student_1, student_2, student_3, admin_1, teacher_1])
    db.session.commit()

    # STAFF FOR OAKWOOD SECONDARY SCHOOL (school2)
    admin_2 = User(
        email="admin2@example.com",
        first_name="David",
        last_name="Sterling",
        password=hashed_pw,
        organization_id=school2.id,
        role="Admin",
        is_verified=True
    )
    
    teacher_2 = User(
        email="teacher2@example.com",
        first_name="Maya",
        last_name="Patel",
        password=hashed_pw,
        organization_id=school2.id,
        role="Teacher",
        is_verified=True
    )

    student_4 = User(
        email="student4@example.com",
        first_name="Ethan",
        last_name="Hunt",
        password=hashed_pw,
        organization_id=school2.id,
        role="Student",
        is_verified=True
    )

    student_5 = User(
        email="student5@example.com",
        first_name="Sophie",
        last_name="Bennett",
        password=hashed_pw,
        organization_id=school2.id,
        role="Student",
        is_verified=True
    )

    db.session.add_all([admin_2, teacher_2, student_4, student_5])
    db.session.commit()

    # STAFF FOR SOLIHULL TECH COLLECTIVE (comm1)
    admin_3 = User(
        email="admin3@example.com",
        first_name="Julian",
        last_name="Thorne",
        password=hashed_pw,
        organization_id=comm1.id,
        role="Admin",
        is_verified=True
    )
    
    teacher_4 = User(
        email="teacher4@example.com",
        first_name="Siddharth",
        last_name="Nair",
        password=hashed_pw,
        organization_id=comm1.id,
        role="Teacher",
        is_verified=True
    )

    member_1 = User(
        email="member1@example.com",
        first_name="Nora",
        last_name="Kemp",
        password=hashed_pw,
        organization_id=comm1.id,
        role="Student",
        is_verified=True
    )

    member_2 = User(
        email="member2@example.com",
        first_name="Oscar",
        last_name="Isaac",
        password=hashed_pw,
        organization_id=comm1.id,
        role="Student",
        is_verified=True
    )

    db.session.add_all([admin_3, teacher_4, member_1, member_2])
    db.session.commit()

    # INDIVIDUAL ACCOUNT
    individual = User(
        email="individual@example.com",
        first_name="Grace",
        last_name="Hopper",
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

    #Course for Oakwood
    course_agriculture = Course(
        name="Regenerative Agriculture & Land Management", 
        description="An essential study of soil health, biodiversity, and sustainable farming techniques designed to restore ecosystems while maintaining food security.", 
        organization_id=school2.id
    )





    # Contributions for Coventry University Students (Wildlife & Auto)
    cont1 = Contribution(
        title="Rhino Tracking Techniques",
        text="Researching how GPS tagging helps in monitoring white rhino migration patterns in protected areas.",
        user_id=student_1.id,
        moderated=True
    )

    cont2 = Contribution(
        title="Aerodynamics in EVs",
        text="A look at how reducing the drag coefficient can significantly extend the range of electric vehicles.",
        user_id=student_2.id,
        moderated=True
    )

    # Contribution for Oakwood (Agriculture)
    cont3 = Contribution(
        title="Vertical Farming Trial",
        text="Initial results from our indoor lettuce growth experiment using hydroponic systems. Efficiency is up 20%!",
        user_id=student_4.id,
        moderated=True
    )
    
    cont4 = Contribution(
        title="Soil pH and Biodiversity",
        text="A study on how keeping soil acidity balanced encourages the return of local earthworm populations.",
        user_id=student_5.id,
        moderated=True
    )

    # Contributions for Solihull Tech Collective
    cont5 = Contribution(
        title="AI in Local Governance",
        text="Could we use simple LLMs to help citizens navigate council planning applications more easily?",
        user_id=member_1.id,
        moderated=True
    )

    cont6 = Contribution(
        title="The Right to Repair",
        text="Why we should be running workshops to help people fix their own smartphones and laptops.",
        user_id=member_2.id,
        moderated=True
    )

    # Contribution for the Individual Account
    cont7 = Contribution(
        title="Freelance Sustainability",
        text="Tips for maintaining a zero-waste office while working as a remote developer.",
        user_id=individual.id,
        moderated=True
    )

    # Contribution from a Teacher
    cont8 = Contribution(
        title="Intro to Wildlife Biology",
        text="Reading list for the first-year conservation module. Please check the library for these titles.",
        user_id=teacher_1.id,
        moderated=True
    )

    # Add and Commit
    db.session.add_all([cont1, cont2, cont3, cont4, cont5, cont6, cont7, cont8])
    db.session.commit()




    # Sighting for Student 1 (Coventry Wildlife Student)
    sight1 = Sighting(
        title="White Rhino",
        image="sighting1.jpg",
        description="Observed a rhino in northern Java Island ",
        user_id=student_1.id
    )
    
    # Sighting for Member 1 (Solihull Tech Collective)
    sight2 = Sighting(
        title="Komodo Dragon",
        image="sighting2.jpg",
        description="Incredible detail on this mature Komodo Dragon. Captured this during a conservation trek.",
        user_id=member_1.id
    )

    # Adding both to the database
    db.session.add_all([sight1, sight2])
    db.session.commit()


# Add and Commit
    db.session.add_all([course_rhinos, course_automotive, course_agriculture])
    db.session.commit()

    #Student 1 and Teacher 1 to Rhino Course
    enroll_1 = UserCourse(user_id=student_1.id, course_id=course_rhinos.id)
    enroll_2 = UserCourse(user_id=teacher_1.id, course_id=course_rhinos.id)

    #Student 2 to Automotive Course
    enroll_3 = UserCourse(user_id=student_2.id, course_id=course_automotive.id)

    db.session.add_all([enroll_1, enroll_2, enroll_3])
    db.session.commit()



    # --- MORE MATERIALS ---
    
    # Additional Material for Coventry (Rhino Course)
    material2 = Material(
        title="Conservation Strategies",
        text="Modern conservation involves community-led anti-poaching units and habitat restoration. In Ujung Kulon, the focus is on removing invasive species that crowd out the rhino's food sources.",
        course_id=course_rhinos.id
    )

    # Material for Coventry (Automotive Course)
    material3 = Material(
        title="Battery Chemistry 101",
        text="Understanding the difference between Lithium-ion and Solid-State batteries is crucial for the next generation of sustainable transport.",
        course_id=course_automotive.id
    )

    # Material for Oakwood (Agriculture Course)
    material4 = Material(
        title="The Nitrogen Cycle",
        text="A deep dive into how nitrogen fixation works in organic farming without the use of synthetic fertilizers.",
        course_id=course_agriculture.id
    )

    db.session.add_all([material2, material3, material4])
    db.session.commit()

    # --- MORE COMMON ROOM MESSAGES ---

    # Coventry: Rhino Course Discussion
    msg2 = CommonRoomMessage(
        user_id=teacher_1.id,
        text="Welcome everyone! Please read the 'Introduction to Rhinos' material before our seminar on Friday.",
        course_id=course_rhinos.id
    )

    # Coventry: Automotive Course Discussion
    msg3 = CommonRoomMessage(
        user_id=student_2.id,
        text="Does anyone have resources on regenerative braking systems? I'm struggling with the efficiency calculations.",
        course_id=course_automotive.id
    )

    # Oakwood: Agriculture Course Discussion
    msg4 = CommonRoomMessage(
        user_id=teacher_2.id,
        text="The vertical farming sensors are now live. Students can check the dashboard for real-time moisture levels.",
        course_id=course_agriculture.id
    )

    msg5 = CommonRoomMessage(
        user_id=student_4.id,
        text="I just posted my lettuce growth results in the library if anyone wants to see the data!",
        course_id=course_agriculture.id
    )

    db.session.add_all([msg2, msg3, msg4, msg5])
    db.session.commit()

    # --- ADDITIONAL ENROLLMENTS ---
    # Ensuring Oakwood students are actually in their Agriculture course
    enroll_4 = UserCourse(user_id=student_4.id, course_id=course_agriculture.id)
    enroll_5 = UserCourse(user_id=student_5.id, course_id=course_agriculture.id)
    enroll_6 = UserCourse(user_id=teacher_2.id, course_id=course_agriculture.id)

    db.session.add_all([enroll_4, enroll_5, enroll_6])
    db.session.commit()
    
    

    