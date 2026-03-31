from flask import render_template, url_for, redirect, flash, session, request, jsonify
from app import app, login_manager, mail, bcrypt, db
from app.forms import RegistrationForm, LoginForm, ContactForm, OTPForm, ResetPasswordForm, ForgotPasswordForm, UniqueAccessCodeForm, TaskForm
from app.models import User, ContactMessage, OTP, Organization, Announcement, AnnouncementImage, Classroom, Task, Program, Contribution, ContributionImage, UserClassroom, UserTask, GlobalMesssages
from flask import render_template, url_for, redirect, flash, session
from app import app, login_manager, mail, bcrypt, db, socketio
from app.forms import RegistrationForm, LoginForm, ContactForm, OTPForm, ResetPasswordForm, ForgotPasswordForm, UniqueAccessCodeForm
from app.models import User, Organization, ContactMessage, OTP, Messages
from datetime import datetime, timedelta
import secrets      # for otp generation
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
import os
from flask_socketio import emit, join_room, leave_room, close_room, rooms
from sqlalchemy import or_, and_

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



def generate_otp(email):
    otp = f"{secrets.randbelow(1000000):06}"
    expiration_time = datetime.now() + timedelta(minutes=5)    # OTP stays valid for 5 minutes from time of generation
    otp_object = OTP(email=email,otp=otp,expiration_time=expiration_time)
    db.session.add(otp_object)
    db.session.commit()
    return otp

def send_otp_email(recipient_email, otp):
    otp_object = OTP.query.filter_by(email=recipient_email).first()
    if not otp_object:
        return
    expires_in = int((otp_object.expiration_time - datetime.now()).total_seconds() // 60)
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

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('landing.html')

@app.route('/home')
@login_required
def home():
    print(url_for('organization',orgid=1),flush=False)
    return render_template('home.html')

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
            flash('User not verified. Enter valid OTP', 'failure')
            return redirect(url_for('verify_registration'))
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

@app.route('/database')  #This is for testing if you go to this route you can just see the users in the database will remove this at the end
def database():
    return f"<h1>Users</h1><br>{User.query.all()}"


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

    my_classrooms_ids = [classroom.classroom_id for classroom in current_user_object.userclassrooms]    # all the classrooms the current user is part of

    if current_user_object.role == "Teacher":       # Teacher must see all students and admins
        return base_query.join(UserClassroom).filter(
            or_(
                and_(
                    UserClassroom.classroom_id.in_(my_classrooms_ids), 
                    User.role == "Student"
                ),
                User.role == "Admin"
            )
        ).all()

    if current_user_object.role =="Student":    # Student must see all Teachers from the classes they belong to
        return base_query.filter(
            or_(
                User.role == "Teacher",
                UserClassroom.classroom_id.in_(my_classrooms_ids)
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

@app.route("/profilepage",methods=["GET"])
def profilepage():
    return render_template("profilepage.html")

@app.route("/organization/<orgid>",methods=["GET"])
def organization(orgid):
    return render_template("organisationpage.html")

@app.route("/tasks/<orgid>",methods=["GET"])
def tasks(orgid):
    tasks = UserTask.query.filter_by(user_id=current_user.id)
    return render_template("tasks.html",tasks=tasks)

@app.route("/classrooms/<orgid>",methods=["GET"])
def classrooms(orgid):
    classrooms = UserClassroom.query.filter_by(user_id=current_user.id)
    return render_template("classrooms.html",classrooms=classrooms)

@app.route("/class/<orgid>/<classid>",methods=["GET"])
def classroom(orgid,classid):
    return render_template("classroom.html", classid=classid)

@app.route("/announcements/<orgid>",methods=["GET"])
def announcements(orgid):
    announcements = Announcement.query.filter_by(organization_id=current_user.organization_id)
    return render_template("announcements.html", announcements=announcements)

@app.route("/commonroom/<orgid>/<classid>",methods=["GET"])
def commonroom(orgid,classid):
    return render_template("commonroom.html")

@app.route("/members/<orgid>/<classid>",methods=["GET"])
def members(orgid,classid):
    return render_template("members.html")

@app.route("/tasks/<orgid>/<classid>",methods=["GET"])
def classtasks(orgid,classid):
    tasks = UserTask.query.filter_by(user_id=current_user.id)
    return render_template("classtasks.html", tasks=tasks)

@app.route("/createtask",methods=["GET","POST"])
def createtask():
    form = TaskForm()
    readingContent = request.args.get('readingContent')
    if readingContent:
        form.readingContent.data = readingContent
    return render_template("createtask.html",  form=form)

@app.route("/programs",methods=["GET"])
def programs():
    query = request.args.get('taskcreate')
    taskcreate = bool(query)  #False if None, True if anything else
    return render_template("programs.html", taskcreate=taskcreate)

@app.route("/programs/rhino",methods=["GET"])
def rhino():
    query = request.args.get('taskcreate')
    taskcreate = bool(query)  #False if None, True if anything else
    return render_template("programrhino.html", taskcreate=taskcreate)

@app.route("/publiclibrary",methods=["GET"])
def publiclibrary():
    contributions = Contribution.query.all()
    return render_template("publiclibrary.html", contributions=contributions)
