from flask import render_template, url_for, redirect, flash, session, request, jsonify, current_app
from app import app, login_manager, mail, bcrypt, db
from app.forms import RegistrationForm, LoginForm, ContactForm, OTPForm, ResetPasswordForm, ForgotPasswordForm, UniqueAccessCodeForm, ContributionForm, GradeTaskForm, ReplyTaskForm
from app.models import User, ContactMessage, OTP, Organization, Task, UserTask, Contribution, UserCourse, GlobalMesssages, Course, Material, CommonRoomMessage, CommonRoomMessageReply,Image, File, WorkshopActivity, ContributionReply, Sighting, TaskReply, FeatureStat
from flask import render_template, url_for, redirect, flash, session
from app import app, login_manager, mail, bcrypt, db, socketio
from app.forms import RegistrationForm, LoginForm, ContactForm, OTPForm, ResetPasswordForm, ForgotPasswordForm, UniqueAccessCodeForm, MaterialForm, AddUserCourseForm, CommonRoomMessageForm, CommonRoomReplyForm, WorkshopActivityForm, ContributionReplyForm, AddUserOrganisationForm, CreateCourseForm, SightingForm, UpdateProfileForm, CreateTaskForm, SubmissionForm, OrganizationForm
from app.models import User, Organization, ContactMessage, OTP, Messages
from datetime import datetime, timedelta
import secrets      # for otp generation
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
import os
from flask_socketio import emit, join_room, leave_room, close_room, rooms
from sqlalchemy import or_, and_, desc
from PIL import Image as PILImage
from werkzeug.utils import secure_filename

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def save_file(file, folder):
    """Helper to give files unique names and save them"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    filename = random_hex + f_ext
    filepath = os.path.join(app.root_path, folder, filename)
    file.save(filepath)
    return filename

def generate_otp(email):
    otp = f"{secrets.randbelow(1000000):06}"
    expiration_time = datetime.utcnow() + timedelta(minutes=5)    # OTP stays valid for 5 minutes from time of generation
    otp_object = OTP(email=email,otp=otp,expiration_time=expiration_time)
    db.session.add(otp_object)
    db.session.commit()
    return otp

def send_otp_email(recipient_email, otp):
    otp_object = OTP.query.filter_by(email=recipient_email).first()
    if not otp_object:
        return
    expires_in = int((otp_object.expiration_time - datetime.utcnow()).total_seconds() // 60)
    msg = Message(subject="OTP Code for verification",
                  recipients=[recipient_email],
                  body= f"Your OTP is {otp}. It will expire in {expires_in} minutes.",
                  sender= os.getenv("EMAIL"))
    mail.send(msg)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender= os.getenv("EMAIL"),
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def verify_email_otp(email, entered_otp):
    otp_object = OTP.query.filter_by(email=email).first()

    if not otp_object:      # check if record exists
        return False

    if datetime.now() > otp_object.expiration_time:      # check if OTP has expired
        db.session.delete(otp_object)
        db.session.commit()
        return False

    # check if user entered OTP matches the OTP in records sent to the user
    if entered_otp == otp_object.otp:
        db.session.delete(otp_object)
        db.session.commit()
        return True

    return False    # if entered OTP is incorrect

def acknowledge_contact_email(email):
    ack_msg = Message(subject= "Acknowledgement of Your Query",
                  recipients=email,
                  body= "We have received your query. We will get back to you shortly.",
                  sender= app.config('MAIL_USERNAME'))
    mail.send(ack_msg)

def track_visit(column_name):
    stats = FeatureStat.query.first()
    
    if not stats:
        # Manually set to 0 to avoid the NoneType + int error
        stats = FeatureStat(
            game_visits=0, 
            program_visits=0, 
            common_room_visits=0
        )
        db.session.add(stats)
        db.session.flush() # This pushes the object to the session without a full commit
    
    # Check if the attribute exists
    if hasattr(stats, column_name):
        current_val = getattr(stats, column_name)
        
        # Safety check: if for some reason the DB returned None, treat as 0
        if current_val is None:
            current_val = 0
            
        setattr(stats, column_name, current_val + 1)
        db.session.commit()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('landing.html')

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = OrganizationForm()
    
    if current_user.role == 'Sysadmin' and form.validate_on_submit():
        if form.icon.data:
            icon_file = form.icon.data
            filename = secure_filename(icon_file.filename)
            filepath = os.path.join(current_app.root_path, 'static/images', filename)
            icon_file.save(filepath)
            db_icon_name = filename
        else:
            db_icon_name = 'default_org.jpg'

        # 2. Create and Save the Organization
        new_org = Organization(
            name=form.name.data,
            description=form.description.data,
            org_type=form.org_type.data,
            icon=db_icon_name
        )
        
        db.session.add(new_org)
        db.session.commit()
        flash(f'Organization "{new_org.name}" created successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        if user.is_verified:
            flash(f"Logged in as {user.first_name} {user.last_name}", 'success')
            login_user(user)
            return redirect(url_for('home'))
        else:       # unverified user
            flash('Incorrect username or password', 'failure')
            return redirect(url_for('login'))
    elif request.method == "POST":
        flash('Incorrect username or password', 'failure')
        return redirect(url_for('login'))
    return render_template('login.html',form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "notification")
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    otpform = OTPForm()
    showotpform = False
    if form.submit.data and form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(email= email,
                        first_name= form.first_name.data.strip(),
                        last_name= form.last_name.data.strip(),
                        password= hashed_password)
        session['verify_registration_email'] = email
        db.session.add(new_user)
        db.session.commit()

        otp_object = OTP.query.filter_by(email=email).first()
        if otp_object:
            db.session.delete(otp_object)
            db.session.commit()
            
        # send email with OTP for verification
        showotpform = True
        otp = generate_otp(email) 
        send_otp_email(recipient_email=email, otp=otp)
        flash("OTP sent to email. Please enter OTP", 'notification')

    if otpform.submit_btn.data and otpform.validate_on_submit():
        email = session.get('verify_registration_email')
        otp = otpform.user_entered_OTP.data
        if verify_email_otp(email=email,entered_otp=otp):
            user = User.query.filter_by(email=email).first()   #Set user is_verified to true
            user.is_verified = True
            db.session.commit()
            session.pop('verify_registration_email', None)              # clear session after successful verification
            flash("Account created, you can now log in", 'success')
            return redirect(url_for('login'))
        else:
            session.pop('verify_registration_email', None)              # clear session after unsuccessful verification
            flash("Account registration failed. Invalid code", 'failure')
            return redirect(url_for('register'))
    return render_template('register.html', form=form, otpform=otpform, showotpform=showotpform)

@app.route('/contact', methods= ['GET', 'POST'])
def contact():
    if current_user.is_authenticated:   
        return redirect(url_for('home'))
    form = ContactForm()
    if form.validate_on_submit():
        email = form.company_email.data.strip().lower()
        contact_message = ContactMessage(first_name= form.first_name.data.strip(),
                                         last_name= form.last_name.data.strip(),
                                         region= form.region.data,
                                         email= email,
                                         userMessage= form.userQuery.data.strip())
        try:
            db.session.add(contact_message)      #adds the new data field about a user's query to the db table
            db.session.commit()
            # TODO: needs to send an email status update instead
            flash("Query Submitted! Confirmation email sent to you!", "success")

            # send confirmation email
            acknowledge_contact_email(email)

            # render homepage
            return redirect(url_for('home'))

        except Exception as e:
            db.session.rollback()
            # TODO: needs to send an email status update instead
            flash("Something went wrong. Please try again", "failure")
            return redirect(url_for('contact'))

    else:
        """  show validation errors (in HTML template) in case of form validation failure """
        return render_template('contactForm.html', form=form)
    
@app.route('/about', methods= ['GET'])
def about():
    return render_template("about.html")

@app.route('/register/verify', methods= ['GET', 'POST'])
def verify_registration():              # get otp entered by user in the form
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = OTPForm()
    register_email = session.get('verify_registration_email')

    if not register_email:
        flash("Please register again.", 'failure')
        return redirect('register')

    if form.validate_on_submit():
        otp = form.user_entered_OTP.data
        if verify_email_otp(email= register_email, entered_otp= otp):
            flash("OTP verified. Your message has been confirmed", 'success')
            session.pop('contact_email', None)              # clear session after successful verification

            # update in Database that user has been verified
            user = User.query.filter_by(email=register_email).first()
            user.is_verified = True
            db.session.commit()

            user = User.query.filter_by(email= register_email).first()
            if user and user.is_verified:
                session.pop("verify_registration_email", None)
                return redirect(url_for('login'))

        else:
            flash("Incorrect or expired OTP. Please try again", 'failure')
            return redirect(url_for('verify_contact_otp'))

    return render_template('otp_form.html', form=form)


@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'notification')
        return redirect(url_for('login'))
    return render_template('forgot_password.html', title='Reset Password', form=form)


@app.route("/reset_token/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'failure')
        return redirect(url_for('forgot_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        user.is_verified = True
        user.uniqueAccessCode = ""
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route("/orglogin",methods=["GET","POST"])
def orglogin():
    form = UniqueAccessCodeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(uniqueAccessCode=form.uniqueAccessCode.data).first()
        if not user:
            flash("Invalid Unique Access Code",'failure')
        else:
            send_reset_email(user)
            return redirect(url_for('reset_token', token=user.get_reset_token(), _external=True))  #An email would be sent but isnt since chances are you won't have access to this email
            flash('An email has been sent with instructions to set your password.', 'notification')
            return redirect(url_for('login'))
    return render_template("orglogin.html",form=form)

def get_allowed_contacts(current_user_object, search_query=""):
    # gives a list of users the current user can message

    # all user from the same organisation except the current user
    base_query = User.query.filter(
        User.organization_id == current_user_object.organization_id,
        User.id != current_user_object.id
    )

    if search_query:
        base_query = base_query.filter(
            or_(
                User.first_name.ilike(f"%{search_query}%"),
                User.last_name.ilike(f"%{search_query}%")
                )
        )

    if current_user_object.role == "Admin":     # Admin can see all the user in the organisation
        return base_query.all()     

    my_classrooms_ids = [classroom.course_id for classroom in current_user_object.usercourses]    # all the classrooms the current user is part of

    if current_user_object.role == "Teacher":       # Teacher must see all students and admins
        return base_query.join(UserCourse).filter(
            or_(
                and_(
                    UserCourse.course_id.in_(my_classrooms_ids), 
                    User.role == "Student"
                ),
                User.role == "Admin"
            )
        ).all()

    if current_user_object.role =="Student":    # Student must see all Teachers from the classes they belong to
        return base_query.filter(
            or_(
                User.role == "Teacher",
                UserCourse.course_id.in_(my_classrooms_ids)
            )
        ).all()
    
    return []

@app.route('/chat/<int:orgid>')
@login_required        # chat feature available only to logged in users
def chat(orgid):
    if current_user.organization_id != orgid:
        flash("You do not have access to this organization's chat.", "failure")
        return redirect(url_for('home'))
    
    active_contacts = get_allowed_contacts(current_user)
    global_history = GlobalMesssages.query.join(User).filter(
        User. organization_id == orgid
    ).order_by(GlobalMesssages.timestamp.asc()).all()
          
    return render_template('chat.html', users=active_contacts, global_msgs= global_history)

@socketio.on('connect')
def handle_join():
    if current_user.is_authenticated:
        # join private room for each user
        join_room(f"User_{current_user.id}")
        # join organisation global chatroom
        join_room(f"Organisation_global_{current_user.organization_id}")
        print(f"\nUser {current_user.id} can chat in private & organisation rooms\n")

# Defining event listener
@socketio.on('send_private_message')        # listen for 'send_private_message' event from JavaScript side
def send_pvt_message(data):
    """Triggered when the user hits 'Send' button"""
    friend_id = int(data['friend_id'])
    my_id = current_user.id

    # save data to SQLite DB here
    txt_msg = data.get('text', None)
    if txt_msg and friend_id:
        new_message = Messages(text= txt_msg,
                               sender_id= my_id,
                               receiver_id= friend_id)
        db.session.add(new_message)
        db.session.commit()

        print(f"Sending message [{txt_msg}] from [{my_id}] to [{friend_id}]")
        # send data to sender and receiver's frontend
        emit('receive_private_message', {'text': txt_msg,'sender_id': my_id}, to=f"User_{current_user.id}")
        emit('receive_private_message', {'text': txt_msg,'sender_id': my_id}, to=f"User_{friend_id}")
    else:
        print(f"Failed to send [{txt_msg}].")

@socketio.on('send_global_message')
def handle_global_msgs(data):
    if current_user.role == "Student":  # Students not allowed to message globally
        return
    
    # Teachers and Admins can message globally
    print(f"Server received: {data}")
    
    text = data.get('text', None)
    sender_id = current_user.id
    
    if text and sender_id:
        global_msg = GlobalMesssages(text=text, sender_id=sender_id)
        db.session.add(global_msg)
        db.session.commit()
        # broadcast received msg to everyone in the same organisation
        emit('receive_global_message', 
            {
                'text': text, 
                'sender': f"{current_user.first_name} {current_user.last_name}",
                'sender_id': sender_id
            }, 
            to=f"Organisation_global_{current_user.organization_id}", broadcast= True)

# REST API that returns chat history
@app.route('/api/messages/<int:friend_id>', methods= ['GET'])
@login_required
def get_chat_history(friend_id):
    my_id = current_user.id

    # fetch the chats between 2 specific people
    chat_history = Messages.query.filter(
        or_(
            (Messages.sender_id == my_id) & (Messages.receiver_id == friend_id),
            (Messages.sender_id == friend_id) & (Messages.receiver_id == my_id)
        )
    ).order_by(Messages.timestamp.asc()).all()

    all_chats = []

    # packaging only required chat data from chats history
    for chat in chat_history:
        chat_data = {
            'id': chat.id,
            'sender_name': f"{chat.sender.first_name} {chat.sender.last_name}",
            'receiver_name': f"{chat.receiver.first_name} {chat.receiver.last_name}",
            'message_content': chat.text,
            'sender_id': chat.sender_id,
            'receiver_id': chat.receiver_id
        }
        all_chats.append(chat_data)

    # return the chats as a JSON object
    return jsonify({'messages': all_chats})

@app.route('/api/search_db', methods=['GET'])
@login_required
def search_database():
    search_query = request.args.get('q', '').lower()

    if not search_query:
        return jsonify({'users': []})

    results = get_allowed_contacts(current_user, search_query)
    user_data = [{'id': u.id, 'name': f"{u.first_name} {u.last_name}"} for u in results[:10]]

    return jsonify({'users': user_data})

@app.route("/profilepage", methods=["GET", "POST"])
@login_required
def profilepage():
    form = UpdateProfileForm()
    
    if form.validate_on_submit():
        # 1. Update the Pattern (Always)
        current_user.profile_pattern = form.pattern.data
        
        # 2. Update the Picture (Only if provided)
        if form.picture.data:
            # Delete old picture logic...
            if current_user.image and current_user.image != 'default_profile.jpg':
                old_path = os.path.join(app.root_path, 'static/images', current_user.image)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            # Save new file
            picture_file = save_file(form.picture.data, "static/images")
            current_user.image = picture_file
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profilepage'))
    
    # 3. Populate form with current values on GET request
    elif request.method == 'GET':
        form.pattern.data = current_user.profile_pattern
        
    return render_template("profilepage.html", form=form) # Make sure this matches your filename


@app.route("/organization/<orgid>", methods=["GET", "POST"])
def organization(orgid):
    form = CreateCourseForm()
    
    if form.validate_on_submit():
        icon_file = 'default.png'
        if form.icon.data:
            # Simple unique filename logic
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form.icon.data.filename)
            icon_file = random_hex + f_ext
            path = os.path.join(app.root_path, 'static/images', icon_file)
            form.icon.data.save(path)

        new_course = Course(
            name=form.name.data,
            description=form.description.data,
            icon=icon_file,
            organization_id=orgid
        )
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('organization', orgid=orgid))

    courses = Course.query.filter_by(organization_id=orgid).all()
    return render_template("organisationpage.html", courses=courses, form=form, orgid=orgid, current_org=Organization.query.get(orgid))

@app.route("/members/<orgid>", methods=["GET", "POST"])
def membersorg(orgid):
    form = AddUserOrganisationForm()
    if form.validate_on_submit():
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash("THEPASSWORDFORUNVERIFIEDORGPEOPLE@P123").decode('utf-8')
        uniqueAccessCode = f"{secrets.randbelow(100000000):08}"
        new_user = User(email= email,
                        first_name= form.first_name.data.strip(),
                        last_name= form.last_name.data.strip(),
                        password= hashed_password,
                        organization_id=orgid,
                        role=form.role.data,
                        is_verified=False,
                        uniqueAccessCode=uniqueAccessCode)
        db.session.add(new_user)
        db.session.commit()
        flash("Added new user", "success")
    elif form.is_submitted():
        flash("Could not add user. Please check the email and try again.", "failure")

    # Standard Queries for display
    students = User.query.filter(
        User.organization_id == orgid,
        User.role == "Student",
        User.is_verified == True
    ).all()
    
    teachers = User.query.filter(
        User.organization_id == orgid,
        User.role == "Teacher",
        User.is_verified == True
    ).all()

    unverified_users = []
    if current_user.role == "Admin":
        unverified_users = User.query.filter_by(organization_id=orgid, is_verified=False).all()

    return render_template("membersorg.html", 
                           students=students, 
                           teachers=teachers, 
                           unverified_users=unverified_users,
                           orgid=orgid, 
                           form=form) # Don't forget to pass the form!

@app.route("/organisation/<int:orgid>/remove/<int:userid>", methods=["POST"])
def remove_member(orgid, userid):
    user = User.query.get(userid)

    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Member's account has been deleted.", "success")
    
    return redirect(url_for('membersorg', orgid=orgid))

@app.route("/assignments/<int:orgid>/<int:courseid>", methods=["GET", "POST"])
@login_required
def tasks(orgid, courseid):
    create_form = CreateTaskForm()
    submit_form = SubmissionForm()
    now = datetime.utcnow()

    if request.method == "POST":
        # --- CASE A: Teacher creates a new task ---
        if 'create_task' in request.form and create_form.validate_on_submit():
            new_task = Task(
                name=create_form.name.data,
                due_date=create_form.due_date.data,
                course_id=courseid
            )
            db.session.add(new_task)
            db.session.flush()

            # Assign to all students in the course
            # (Assuming you have a UserCourse or similar enrollment table)
            students = User.query.filter_by(organization_id=orgid, role="Student").all()
            for s in students:
                assignment = UserTask(user_id=s.id, task_id=new_task.id)
                db.session.add(assignment)
            
            db.session.commit()
            flash("Task Created!", "success")
            return redirect(url_for('tasks', orgid=orgid, courseid=courseid))

        # --- CASE B: Student submits a file ---
        if 'submit_work' in request.form:
            ut_id = request.form.get('user_task_id')
            user_task = UserTask.query.get_or_404(ut_id)
            
            if submit_form.file.data:
                file = submit_form.file.data
                filename = secure_filename(f"user_{current_user.id}_{file.filename}")
                file.save(os.path.join(app.root_path, 'static/uploads', filename))
                
                user_task.submission_file = filename
                user_task.submitted = True
                user_task.date_submitted = datetime.utcnow()
                db.session.commit()
                flash("Assignment submitted successfully!", "success")
                return redirect(url_for('tasks', orgid=orgid, courseid=courseid))

    # --- GET LOGIC: Filtered List ---
    if current_user.role == "Teacher":
        # Teachers see ALL tasks created for this course, regardless of "UserTask" table
        tasks_to_show = Task.query.filter_by(course_id=courseid).order_by(Task.due_date.asc()).all()
        # Note: These are 'Task' objects, not 'UserTask' objects
    else:
        # Students see their specific assignments from the UserTask table
        # We use .all() to get the list of UserTask objects
        tasks_to_show = UserTask.query.join(Task).filter(
            UserTask.user_id == current_user.id,
            Task.due_date >= now
        ).order_by(Task.due_date.asc()).all()

    return render_template("tasks.html", 
                           tasks=tasks_to_show, 
                           create_form=create_form, 
                           submit_form=submit_form, 
                           orgid=orgid, 
                           courseid=courseid,
                           course=Course.query.get(courseid))

@app.route("/course/<int:courseid>/submissions")
@login_required
def view_submissions(courseid):
    # Security Check: Only Teachers should see this
    if current_user.role != "Teacher":
        flash("Access denied. Teachers only.", "failure")
        return redirect(url_for('home'))

    # Optional: Filter by a specific Task ID (passed via URL args)
    task_id = request.args.get('task_id', type=int)
    
    query = db.session.query(UserTask).join(Task).join(User).filter(
        Task.course_id == courseid,
        UserTask.submitted == True
    )

    if task_id:
        query = query.filter(UserTask.task_id == task_id)

    submissions = query.order_by(UserTask.date_submitted.desc()).all()

    return render_template("submissions.html", 
                           submissions=submissions, 
                           courseid=courseid)

@app.route("/submission/<int:usertask_id>", methods=["GET", "POST"])
@login_required
def view_single_submission(usertask_id):
    usertask = UserTask.query.get_or_404(usertask_id)
    grade_form = GradeTaskForm()
    reply_form = ReplyTaskForm()

    # SECURITY: Prevent students from seeing other students' submissions
    if current_user.role != "Teacher" and usertask.user_id != current_user.id:
        flash("Access Denied.", "failure")
        return redirect(url_for('home'))

    # Handle Grading (Teacher Only)
    if 'grade' in request.form and grade_form.validate_on_submit():
        if current_user.role == "Teacher":
            usertask.grade = grade_form.grade.data
            new_reply = TaskReply(
                user_id=current_user.id,
                text=f"GRADED: {grade_form.feedback.data}",
                usertask_id=usertask.id
            )
            db.session.add(new_reply)
            db.session.commit()
            flash("Grade and feedback saved!", "success")
            return redirect(url_for('view_single_submission', usertask_id=usertask.id))

    # Handle Replies
    if 'text' in request.form and reply_form.validate_on_submit():
        new_reply = TaskReply(
            user_id=current_user.id,
            text=reply_form.text.data,
            usertask_id=usertask.id
        )
        db.session.add(new_reply)
        db.session.commit()
        return redirect(url_for('view_single_submission', usertask_id=usertask.id))

    return render_template("view_submission.html", 
                           usertask=usertask, 
                           grade_form=grade_form, 
                           reply_form=reply_form)

@login_required
@app.route("/course/<orgid>/<courseid>",methods=["GET"])
def course(orgid,courseid):
    course = Course.query.get_or_404(courseid)
    is_enrolled = UserCourse.query.filter_by(
        user_id=current_user.id, 
        course_id=courseid
    ).first()

    if not is_enrolled and current_user.role not in ["Teacher", "Admin"] and current_user.organization_id != orgid:
        flash("You are not enrolled in this course.", "failure")
        return redirect(url_for('organization', orgid=orgid))

    # 3. Security: Ensure the course actually belongs to the organization in the URL
    if str(course.organization_id) != str(orgid):
        return redirect(url_for('organization', orgid=orgid))
    return render_template("course.html", course=course)

# @app.route("/materials/<orgid>/<courseid>", methods=["GET"])
# def materials(orgid,courseid):
#     materials = Material.query.filter_by(course_id=courseid).all()
#     return render_template("materials.html",materials=materials, courseid=courseid)

@app.route("/courses", methods=["GET"])
@login_required
def courses():
    courses = Course.query.join(UserCourse).filter(UserCourse.user_id == current_user.id).all()
    return render_template("courses.html", courses=courses)

@app.route("/materials/<orgid>/<courseid>/<int:selected_id>", methods=["GET", "POST"])
@app.route("/materials/<orgid>/<courseid>", methods=["GET", "POST"])
def materials(orgid, courseid, selected_id=None):
    form = MaterialForm()  
    if form.validate_on_submit():
        # 1. Create and Save the main Material object
        new_material = Material(title=form.title.data, text=form.text.data, course_id=courseid)
        db.session.add(new_material)
        db.session.commit()  # Commit so we have an ID for the foreign keys below

        # 2. Process Multiple Images
        if form.images.data:
            for file in form.images.data:
                if file.filename: # Ensure a file was actually uploaded
                    filename = save_file(file, 'static/images')
                    img_record = Image(file=filename, parent_id=new_material.id, parent_type="material")
                    db.session.add(img_record)

        # 3. Process Multiple Documents
        if form.documents.data:
            for file in form.documents.data:
                if file.filename:
                    filename = save_file(file, 'static/uploads')
                    file_record = File(file=filename, parent_id=new_material.id, parent_type="material")
                    db.session.add(file_record)

        db.session.commit()
        flash("Material deleted!", "success")
        return redirect(url_for('materials', orgid=orgid, courseid=courseid))
    
    materials_list = Material.query.filter_by(course_id=courseid).all()

    selected_material = None
    if selected_id:
        selected_material = Material.query.get(selected_id)
    elif materials_list:
        # Optional: default to the first material if none selected
        selected_material = materials_list[0]


    return render_template("materials.html", 
                           materials=materials_list, 
                           form=form, 
                           courseid=courseid, 
                           orgid=orgid, selected_material=selected_material)

@app.route("/commonroom/reply/<int:msg_id>", methods=["POST"])
@login_required
def post_reply(msg_id):
    form = CommonRoomReplyForm()
    
    # We check if the form is valid (text is present and under character limit)
    if form.validate_on_submit():
        # 1. Ensure the parent message actually exists
        parent_msg = CommonRoomMessage.query.get_or_404(msg_id)
        
        # 2. Create the reply object
        new_reply = CommonRoomMessageReply(
            text=form.text.data,
            user_id=current_user.id,
            common_room_message_id=parent_msg.id
        )
        
        # 3. Save to database
        db.session.add(new_reply)
        db.session.commit()
        return redirect(request.referrer)

    flash("Reply cannot be empty.", "failure")
    return redirect(request.referrer)

@app.route("/material/<int:material_id>/toggle", methods=["POST"])
def toggle_visibility(material_id):
    material = Material.query.get_or_404(material_id)
    # Check if user is Teacher/Admin before allowing this!
    material.is_visible = not material.is_visible
    db.session.commit()
    flash(f"Visibility updated for {material.title}", "success")
    return redirect(url_for('materials', orgid=current_user.organization_id, courseid=material.course_id, selected_id=material.id))

@app.route("/material/<int:material_id>/delete", methods=["POST"])
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    course_id = material.course_id
    
    # 1. Delete Physical Image Files
    for img in material.images:
        image_path = os.path.join(current_app.root_path, 'static/images', img.file)
        if os.path.exists(image_path):
            os.remove(image_path)
        # The database record for 'img' will be deleted via cascade or manual delete
        db.session.delete(img)

    # 2. Delete Physical Document Files
    for doc in material.files:
        # Adjust 'images' to 'files' if you stored documents in a different subfolder
        file_path = os.path.join(current_app.root_path, 'static/uploads', doc.file)
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(doc)
    
    # 3. Delete the Material itself
    db.session.delete(material)
    db.session.commit()
    
    flash("Material and all associated files deleted.", "notification")
    return redirect(url_for('materials', orgid=current_user.organization_id, courseid=course_id))

@app.route("/commonroom/<orgid>/<courseid>", methods=["GET", "POST"])
def commonroom(orgid, courseid):
    if request.method == "GET":
        track_visit("common_room_visits")
    form = CommonRoomMessageForm()
    reply_form = CommonRoomReplyForm()
    
    if form.validate_on_submit():
        # 1. Create the Main Message
        new_msg = CommonRoomMessage(
            user_id=current_user.id,
            text=form.text.data,
            course_id=courseid
        )
        db.session.add(new_msg)
        db.session.commit()

        if form.images.data:
            for file in form.images.data:
                if file.filename: # Ensure a file was actually uploaded
                    filename = save_file(file, 'static/images')
                    img_record = Image(file=filename, parent_id=new_msg.id, parent_type="common_room_message")
                    db.session.add(img_record)

        db.session.commit()
        flash('Message posted!', 'success')
        return redirect(url_for('commonroom', orgid=orgid, courseid=courseid))

    # Fetch messages (Newest first)
    messages = CommonRoomMessage.query.order_by(CommonRoomMessage.time_of_creation.desc()).all()
    
    return render_template("commonroom.html", 
                           messages=messages, 
                           form=form, 
                           reply_form=reply_form,
                           orgid=orgid, 
                           courseid=courseid)

@app.route("/commonroom/<int:msg_id>/delete", methods=["POST"])
def delete_common_room_msg(msg_id):
    msg = CommonRoomMessage.query.get_or_404(msg_id)
    course_id = msg.course_id
    
    # 1. Delete Physical Image Files
    for img in msg.images:
        image_path = os.path.join(current_app.root_path, 'static/images', img.file)
        if os.path.exists(image_path):
            os.remove(image_path)
        # The database record for 'img' will be deleted via cascade or manual delete
        db.session.delete(img)

    # 2. Delete Physical Document Files
    for reply in msg.replies:
        db.session.delete(reply)
    
    # 3. Delete the Material itself
    db.session.delete(msg)
    db.session.commit()
    
    flash("Post deleted.", "notification")
    return redirect(url_for('commonroom', orgid=current_user.organization_id, courseid=course_id))

@app.route("/commonroom/<int:msg_id>/deletereply", methods=["POST"])
@login_required
def delete_common_room_reply(msg_id):
    reply = CommonRoomMessageReply.query.get_or_404(msg_id)
    
    # Get course info from the parent message for the redirect
    course_id = reply.message.course_id
    
    db.session.delete(reply)
    db.session.commit()
    
    flash("Reply deleted.", "notification")
    return redirect(url_for('commonroom', orgid=current_user.organization_id, courseid=course_id))

@app.route("/members/<orgid>/<courseid>", methods=["GET", "POST"])
def members(orgid, courseid):
    form = AddUserCourseForm()
    course = Course.query.get_or_404(courseid)

    # Handle Form Submission
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if user is already enrolled
        existing_enrollment = UserCourse.query.filter_by(user_id=user.id, course_id=courseid).first()
        
        if existing_enrollment:
            flash('User is already enrolled in this course.', 'failure')
        else:
            new_enrollment = UserCourse(user_id=user.id, course_id=courseid)
            db.session.add(new_enrollment)
            db.session.commit()
            flash(f'{user.first_name} has been added to the course.', 'success')
            return redirect(url_for('members', orgid=orgid, courseid=courseid))
    elif form.is_submitted():
        flash("Could not add user. Please check the email and try again.", "failure")

    # Standard Queries for display
    students = User.query.join(UserCourse).filter(
        UserCourse.course_id == courseid,
        User.organization_id == orgid,
        User.role == "Student"
    ).all()
    
    teachers = User.query.join(UserCourse).filter(
        UserCourse.course_id == courseid,
        User.organization_id == orgid,
        User.role == "Teacher"
    ).all()

    return render_template("members.html", 
                           students=students, 
                           teachers=teachers, 
                           orgid=orgid, 
                           course=course, 
                           form=form) # Don't forget to pass the form!

@app.route("/course/<int:courseid>/remove/<int:userid>", methods=["POST"])
def remove_participant(courseid, userid):
    # Find the link between the user and the course
    enrollment = UserCourse.query.filter_by(course_id=courseid, user_id=userid).first()
    
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        flash("Participant removed from course.", "success")
    
    return redirect(url_for('members', orgid=Course.query.get(courseid).organization_id, courseid=courseid))

# @app.route("/tasks/<orgid>/<courseid>",methods=["GET"])
# def coursetasks(orgid,courseid):
#     tasks = UserTask.query.filter_by(user_id=current_user.id)
#     return render_template("coursetasks.html", tasks=tasks)

@app.route("/workshop/<orgid>/<courseid>", methods=["GET", "POST"])
@login_required
def workshop(orgid, courseid):
    form = WorkshopActivityForm()
    
    if form.validate_on_submit():
        # 1. Create Activity Entry
        new_activity = WorkshopActivity(
            title=form.title.data,
            text=form.text.data,
            course_id=courseid # Ensure your model has this field to filter by course
        )
        db.session.add(new_activity)
        db.session.flush()  # Get the ID before committing

        # 2. Handle Universal Image Uploads
        if form.images.data:
            for file in form.images.data:
                if file.filename:
                    filename = save_file(file, 'static/images')
                    img_record = Image(
                        file=filename, 
                        parent_id=new_activity.id, 
                        parent_type='workshop'
                    )
                    db.session.add(img_record)

        # 3. Handle Universal File Uploads
        if form.documents.data:
            for doc in form.documents.data:
                if doc.filename:
                    doc_name = save_file(doc, 'static/files')
                    file_record = File(
                        file=doc_name, 
                        parent_id=new_activity.id, 
                        parent_type='workshop'
                    )
                    db.session.add(file_record)

        db.session.commit()
        flash('Workshop Activity Created!', 'success')
        return redirect(url_for('workshop', orgid=orgid, courseid=courseid))

    # Fetch activities (filtering by course)
    activities = WorkshopActivity.query.filter_by(course_id=courseid).order_by(WorkshopActivity.time_of_creation.desc()).all()
    
    return render_template("workshop.html", activities=activities, form=form, orgid=orgid, courseid=courseid)

@app.route("/workshop/activity/<int:activity_id>/contributions", methods=["GET", "POST"])
@login_required
def view_contributions(activity_id):
    form = ContributionForm()
    reply_form = ContributionReplyForm() # Add this
    if form.validate_on_submit():
        contribution = Contribution(
            user_id=current_user.id,
            title=form.title.data,
            text=form.text.data,
            workshop_id=activity_id
        )
        db.session.add(contribution)
        db.session.flush() # Gets the ID so we can link images before the final commit

        if form.images.data:
            for file in form.images.data:
                if file.filename: 
                    filename = save_file(file, 'static/images')
                    img_record = Image(file=filename, parent_id=contribution.id, parent_type="contribution")
                    db.session.add(img_record)

        db.session.commit()
        flash('Contribution Posted!', 'success')
        # ADD THIS REDIRECT:
        return redirect(url_for('view_contributions', activity_id=activity_id))

    activity = WorkshopActivity.query.get_or_404(activity_id)
    # Order by newest first for better UX
    contributions = Contribution.query.filter_by(workshop_id=activity_id).order_by(Contribution.time_of_creation.desc()).all()
    
    return render_template("view_contributions.html", 
                           activity=activity, 
                           contributions=contributions,
                           form=form, reply_form=reply_form)

@app.route("/contribution/delete/<int:con_id>", methods=["POST"])
@login_required
def delete_contribution(con_id):
    contribution = Contribution.query.get_or_404(con_id)
    

    # 1. Delete physical image files from the server
    for img in contribution.images:
        file_path = os.path.join(current_app.root_path, 'static/images', img.file)
        if os.path.exists(file_path):
            os.remove(file_path)

    # 2. Delete from Database (Cascades handle the Image table rows)
    db.session.delete(contribution)
    db.session.commit()
    
    flash("Contribution deleted.", "notification")
    return redirect(request.referrer)

@app.route("/workshop/delete/<int:act_id>", methods=["POST"])
@login_required
def delete_workshop(act_id):
    activity = WorkshopActivity.query.get_or_404(act_id)
    
    # 1. Delete physical files for both Images and Documents
    # 1. Delete Physical Image Files
    for img in activity.images:
        image_path = os.path.join(current_app.root_path, 'static/images', img.file)
        if os.path.exists(image_path):
            os.remove(image_path)
        # The database record for 'img' will be deleted via cascade or manual delete
        db.session.delete(img)

    # 2. Database delete (cascades will handle the Image/File rows)
    db.session.delete(activity)
    db.session.commit()
    
    flash("Workshop activity deleted.", "notification")
    return redirect(request.referrer)

@app.route("/contribution/<int:con_id>/reply", methods=["POST"])
@login_required
def add_reply(con_id):
    form = ContributionReplyForm()
    if form.validate_on_submit():
        reply = ContributionReply(
            text=form.text.data,
            user_id=current_user.id,
            contribution_id=con_id
        )
        db.session.add(reply)
        db.session.commit()
        flash('Reply added!', 'success')
    return redirect(request.referrer)

@app.route("/reply/delete/<int:reply_id>", methods=["POST"])
@login_required
def delete_reply(reply_id):
    reply = ContributionReply.query.get_or_404(reply_id)
    db.session.delete(reply)
    db.session.commit()
    flash('Reply deleted.', 'notification')
    return redirect(request.referrer)

@app.route("/moderate", methods=["GET", "POST"])
@login_required
def moderate():
    form=ContributionForm()
    if current_user.role != 'Sysadmin':
        flash('Access denied. Sysadmin privileges required.', 'failure')
        return redirect(url_for('home'))
    if request.method == "POST":
        contribution_id = request.form.get("contribution_id")
        action = request.form.get("action")
        contribution = Contribution.query.get_or_404(contribution_id)
        if action == "approve":
            contribution.moderated = True
            db.session.commit()
            flash(f'Contribution "{contribution.title}" approved!', 'success')   
        elif action == "delete":
            db.session.delete(contribution)
            db.session.commit()
            flash(f'Contribution "{contribution.title}" has been removed.', 'failure')

        return redirect(url_for('moderate'))
    pending_contributions = Contribution.query.filter_by(moderated=False).order_by(Contribution.time_of_creation.desc()).all()
    return render_template("moderate.html", contributions=pending_contributions, form=form)
# @app.route("/createtask",methods=["GET","POST"])
# def createtask():
#     form = TaskForm()
#     readingContent = request.args.get('readingContent')
#     if readingContent:
#         form.readingContent.data = readingContent
#     return render_template("createtask.html",  form=form)

# @app.route("/programs",methods=["GET"])
# def programs():
#     query = request.args.get('taskcreate')
#     taskcreate = bool(query)  #False if None, True if anything else
#     return render_template("programs.html", taskcreate=taskcreate)

# @app.route("/programs/rhino",methods=["GET"])
# def rhino():
#     query = request.args.get('taskcreate')
#     taskcreate = bool(query)  #False if None, True if anything else
#     return render_template("programrhino.html", taskcreate=taskcreate)
@app.route("/library/<orgid>", methods=["GET", "POST"])
@login_required
def library(orgid):
    form = ContributionForm()
    reply_form = ContributionReplyForm() # Add this
    if form.validate_on_submit():
        contribution = Contribution(
            user_id=current_user.id,
            title=form.title.data,
            text=form.text.data
        )
        db.session.add(contribution)
        db.session.flush() # Gets the ID so we can link images before the final commit

        if form.images.data:
            for file in form.images.data:
                if file.filename: 
                    filename = save_file(file, 'static/images')
                    img_record = Image(file=filename, parent_id=contribution.id, parent_type="contribution")
                    db.session.add(img_record)

        db.session.commit()
        flash('Contribution Posted!', 'success')
        # ADD THIS REDIRECT:
        return redirect(url_for('library',orgid=orgid))

    contributions = (Contribution.query
                     .join(User)
                     .filter(User.organization_id == orgid)
                     .order_by(desc(Contribution.time_of_creation))
                     .all())
    
    return render_template("library.html", 
                           contributions=contributions,
                           form=form, reply_form=reply_form, orgid=orgid, current_org=Organization.query.get(orgid))

@app.route("/schools",methods=["GET"])
def schools():
    schools = Organization.query.filter_by(org_type="School")
    return render_template("schools.html", schools=schools)

@app.route("/communities",methods=["GET"])
def communities():
    communities = Organization.query.filter_by(org_type="Community")
    return render_template("communities.html", communities=communities)

@app.route("/publiclibrary",methods=["GET"])
def publiclibrary():
    return render_template("publiclibrary.html")

@app.route("/publiclibrary/contributions",methods=["GET","POST"])
def publiclibrarycontributions():
    form = ContributionForm()
    reply_form = ContributionReplyForm()
    if form.validate_on_submit():
        contribution = Contribution(
            user_id=current_user.id,
            title=form.title.data,
            text=form.text.data
        )
        db.session.add(contribution)
        db.session.flush() # Gets the ID so we can link images before the final commit

        if form.images.data:
            for file in form.images.data:
                if file.filename: 
                    filename = save_file(file, 'static/images')
                    img_record = Image(file=filename, parent_id=contribution.id, parent_type="contribution")
                    db.session.add(img_record)

        db.session.commit()
        flash('Contribution Sent for Moderation!', 'success')
        # ADD THIS REDIRECT:
        return redirect(url_for('publiclibrarycontributions'))

    contributions = Contribution.query.all()
    
    return render_template("publiclibrarycontributions.html", 
                           contributions=contributions,
                           form=form, reply_form=reply_form)

@app.route("/featurepopularity")
@login_required
def featurepopularity():
    if current_user.role != "Manager":
        flash("Not allowed", "failure")
        return redirect(url_for('home'))
        
    stats = FeatureStat.query.first()
    return render_template("featurepopularity.html", stats=stats)

@app.route("/subscriptiondata", methods=["GET", "POST"])
@login_required
def subscriptiondata():
    if current_user.role != 'Manager':
        flash('Access denied.', 'failure')
        return redirect(url_for('home'))

    organisations = Organization.query.all()
    return render_template("subscriptiondata.html", organisations=organisations)

@app.route("/publiclibrary/programs", methods=["GET", "POST"])
def publiclibraryprograms():
    if request.method == "GET":
        track_visit("program_visits")
    form = SightingForm()
    
    if form.validate_on_submit():
        if form.image.data:
            # Reusing the save function from the previous step
            picture_file = save_file(form.image.data, 'static/images')
            new_sighting = Sighting(
                title=form.title.data, 
                description=form.description.data, 
                image=picture_file,
                user_id=current_user.id
            )
            db.session.add(new_sighting)
            db.session.commit()
            flash('Sighting successfully reported!', 'success')
            return redirect(url_for('publiclibraryprograms'))

    # Fetch sightings to display them on the page
    sightings = Sighting.query.order_by(Sighting.date_posted.desc()).all()
    return render_template("publiclibraryprograms.html", form=form, sightings=sightings)


@app.route("/games",methods=["GET"])
def games():
    track_visit("game_visits")
    return render_template("games.html")

@app.route("/wordle",methods=["GET"])
def wordle():
    return render_template("wordle.html")

@app.route("/riddler",methods=["GET"])
def riddler():
    return render_template("riddler.html")


@app.route("/personalcompilationpage", methods=["GET"])
def personalcompilationpage():
    contributions = Contribution.query.filter_by(user_id=current_user.id)
    sightings = Sighting.query.filter_by(user_id=current_user.id)
    return render_template("personalcompilationpage.html", contributions=contributions, sightings=sightings)




@app.route("/publiclibrary/programs/tiger", methods=["GET"])
def programtiger():
    return render_template("programtiger.html")

@app.route("/publiclibrary/programs/seaturtle", methods=["GET"])
def programseaturtle():
    return render_template("programseaturtle.html")

@app.route("/publiclibrary/programs/rhino", methods=["GET"])
def programrhino():
    return render_template("programrhino.html")

@app.route("/publiclibrary/programs/pangolin", methods=["GET"])
def programpangolin():
    return render_template("programpangolin.html")

@app.route("/publiclibrary/programs/myna", methods=["GET"])
def programmyna():
    return render_template("programMyna.html")

@app.route("/publiclibrary/programs/macaque", methods=["GET"])
def programmacaque():
    return render_template("programmacaque.html")

@app.route("/publiclibrary/programs/leopard", methods=["GET"])
def programleopard():
    return render_template("programleopard.html")

@app.route("/publiclibrary/programs/gibbon", methods=["GET"])
def programgibbon():
    return render_template("programgibbon.html")

@app.route("/publiclibrary/programs/dragon", methods=["GET"])
def programdragon():
    return render_template("programdragon.html")

@app.route("/publiclibrary/programs/deer", methods=["GET"])
def programdeer():
    return render_template("programdeer.html")

@app.route("/publiclibrary/programs/bear", methods=["GET"])
def programbear():
    return render_template("programbear.html")

@app.route("/publiclibrary/programs/bat", methods=["GET"])
def programbat():
    return render_template("programbat.html")

