from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm, ContactForm, OTPForm
import os
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message
import secrets      # for otp generation
from datetime import datetime, timedelta
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///komodohub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.secret_key = "secret-key-for-csrf-tokens"
csrf = CSRFProtect(app)     # enable CSRF protection globally on the 'app' instance
load_dotenv()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# email configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("PASSWORD")

mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    acc_type = db.Column(db.String(20), nullable=False)
    is_verified = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return f"User('{self.id}','{self.email}','{self.first_name}', '{self.last_name}', '{self.password}', '{self.acc_type}', '{self.is_verified}')"
    
class Organization(db.Model,UserMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    og_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Organization('{self.id}','{self.name}')"

class ContactMessage(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key= True)
    first_name = db.Column(db.String(20), nullable= False)
    last_name = db.Column(db.String(20), nullable= False)
    email = db.Column(db.String(120), nullable= False)
    region = db.Column(db.String(60), nullable= False)
    userMessage = db.Column(db.Text, nullable= False)
    time_of_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ContactMessage({self.first_name} {self.last_name}: {self.userMessage})"

with app.app_context():
    if not os.path.exists('komodohub.db'):
        db.create_all()

# Todo: implement DB storage for OTPs
otp_storage = {}    # stores OTPs for verification of user entered OTP

def generate_otp(email):
    otp = f"{secrets.randbelow(1000000):06}"
    expiration_time = datetime.now() + timedelta(minutes=5)    # OTP stays valid for 5 minutes from time of generation
    otp_storage[email] = {'otp': otp, 'expires': expiration_time}
    return otp

def send_otp_email(recipient_email, otp):
    if not otp_storage.get(recipient_email):
        return
    expires_in = int((otp_storage.get(recipient_email).get('expires') - datetime.now()).total_seconds() // 60)
    msg = Message(subject="OTP Code for verification",
                  recipients=[recipient_email],
                  body= f"Your OTP is {otp}. It will expire in {expires_in} minutes.",
                  sender= os.getenv("EMAIL"))
    mail.send(msg)

def verify_email_otp(email, entered_otp):
    otp_record = otp_storage.get(email, None)

    if not otp_record:      # check if record exists
        return False

    if datetime.now() > otp_record['expires']:      # check if OTP has expired
        otp_storage.pop(email, None)
        return False

    # check if user entered OTP matches the OTP in records sent to the user
    if entered_otp == otp_record['otp']:
        otp_storage.pop(email, None)
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
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                if user.is_verified:
                    login_user(user)
                    return redirect(url_for('home'))
                else:       # unverified user
                    flash('User not verified. Enter valid OTP', 'failure')
                    return redirect(url_for('verify_registration'))
            else:       # password does not match
                flash("Invalid password. Try again", 'failure')
                return redirect(url_for('login'))
        else:       # non-existent user --> redirect to registration page
            flash("User does not exist. Register now", 'failure')
            return redirect(url_for('register'))

    if form.errors:
        print(f"Login Form Errors: {form.errors}")

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
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        new_user = User(email= email,
                        first_name= form.first_name.data.strip(),
                        last_name= form.last_name.data.strip(),
                        password= hashed_password,
                        acc_type= "Student",
                        is_verified= False)

        new_user_exists = User.query.filter_by(email= email,
                                               acc_type="Student").first()

        if new_user_exists:
            flash("Email already in use", "failure")
            #return redirect(url_for('login'))
            return render_template('register.html', form=form)

        session['verify_registration_email'] = email
        db.session.add(new_user)
        db.session.commit()

        # send email with OTP for verification
        otp = generate_otp(email)
        send_otp_email(recipient_email=email, otp=otp)
        flash("OTP sent to email. Please enter OTP", 'notification')

        return redirect(url_for('verify_registration'))     # redirect to OTP form

    return render_template('register.html', form=form)

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

if __name__ == '__main__':
    app.run(debug=True, port=2222)