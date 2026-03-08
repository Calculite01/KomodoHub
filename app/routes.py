from flask import render_template, url_for, redirect, flash, session
from app import app, login_manager, mail, bcrypt, db
from app.forms import RegistrationForm, LoginForm, ContactForm, OTPForm, ResetPasswordForm, ForgotPasswordForm, UniqueAccessCodeForm
from app.models import User, Organization, ContactMessage, OTP
from datetime import datetime, timedelta
import secrets      # for otp generation
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
import os

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
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        if user.is_verified:
            flash('User not verified. Enter valid OTP', 'failure')
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
                        password= hashed_password,
                        acc_type= "Individual",
                        is_verified= False)
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