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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///komodohub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.secret_key = "secret-key-for-csrf-tokens"
csrf = CSRFProtect(app)     # enable CSRF protection globally on the 'app' instance

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# email configuration
app.config['MAIL_SERVER'] = 'selected_mail_server_like_smtp'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'sender_username'
app.config['MAIL_PASSWORD'] = 'sender_password'
app.config['MAIL_DEFAULT_SENDER'] = 'example_email@gmail.com'

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

    def __repr__(self):
        return f"User('{self.id}','{self.first_name}', '{self.last_name}')"
    
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

# TODO: implement DB storage for OTPs
otp_storage = {}    # stores OTPs for verification of user entered OTP

def generate_otp(email):
    otp = f"{secrets.randbelow(1000000):06}"
    expiration_time = datetime.now() + timedelta(minutes=5);    # OTP stays valid for 5 minutes from time of generation
    otp_storage[email] = {'otp': otp, 'expires': expiration_time}
    return otp

def send_otp_email(recipient_email, otp):
    if not otp_storage.get(recipient_email):
        return
    expires_in = int((otp_storage.get(recipient_email).get('expires') - datetime.now()).total_seconds() // 60)
    msg = Message(subject="OTP Code for verification",
                  recipients=[recipient_email],
                  body= f"Your OTP is {otp}. It will expire in {expires_in} minutes.",
                  sender= app.config['MAIL_USERNAME'])
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
    return render_template('landing.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
    return render_template('login.html',form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/contact', methods= ['GET', 'POST'])
def contact():
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
            acknowledge_contact_email(email);

            #render contact form to get user OTP
            return redirect(url_for('verify_contact_otp'))

        except Exception as e:
            db.session.rollback()
            # TODO: needs to send an email status update instead
            flash("Something went wrong. Please try again", "failure")
            return redirect(url_for('contact'))

    else:
        """  show validation errors (in HTML template) in case of form validation failure """
        return render_template('contactForm.html', form=form)

@app.route('/register/verify', methods= ['GET', 'POST'])
def verify_contact_otp():              # get otp entered by user in the form
    form = OTPForm()
    recipient_email = session.get('contact_email')

    # send email with OTP for verification
    otp = generate_otp(email)
    send_otp_email(recipient_email=email, otp=otp)
    session['contact_email'] = email

    if not recipient_email:
        flash("Please submit the contact form again.")
        return redirect('contact')

    if form.validate_on_submit():
        otp = form.user_entered_OTP.data
        if verify_email_otp(email= recipient_email, entered_otp= otp):
            flash("OTP verified. Your message has been confirmed", 'success')
            session.pop('contact_email', None)              # clear session after successful verification

            if current_user.is_authenticated:
                return redirect(url_for('home'))            # if the user in current session if logged in, redirect to homepage
            else:
                return redirect(url_for('index'))           # otherwise redirect to landing page

        else:
            flash("Incorrect or expired OTP. Please try again", 'danger')
            return redirect(url_for('verify_contact_otp'))

    return render_template('otp_form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)