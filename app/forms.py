from app import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo, Regexp, DataRequired
from app.models import User

class RegistrationForm(FlaskForm):
    email = EmailField('Email',validators=[InputRequired(),Email(),Length(max=100)])
    first_name = StringField('First Name',validators=[InputRequired(),Length(max=100)])
    last_name = StringField('Last Name',validators=[InputRequired(),Length(max=100)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=100)])
    confirm_password = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            if user.is_verified or user.organization:
                raise ValidationError('Email already in use.')


class LoginForm(FlaskForm):
    email = EmailField('Email',validators=[InputRequired(),Email(),Length(max=100)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=100)])
    submit = SubmitField('Login')

    def validate_password(self,password):
        user = User.query.filter_by(email=self.email.data.strip()).first()
        if user and bcrypt.check_password_hash(user.password, password.data):
            pass
        else:
            raise ValidationError("Incorrect email or password")


class ContactForm(FlaskForm):
    first_name = StringField(label= 'First Name', validators=[InputRequired(), Length(min=4, max=15)])
    last_name = StringField(label= 'Last Name', validators=[InputRequired(), Length(min=4, max=15)])
    company_email = EmailField(label= 'Company Email', validators=[Email(), InputRequired()])
    ph_number = TelField(label= 'Phone Number', validators=[InputRequired(), DataRequired(), Length(min=11, max=11), Regexp(regex='^07[0-9]{3}[-\][0-9]{6}$')])
    region = SelectField(label= 'Region', 
                         choices= [('java', 'Java'), ('sumatra', 'Sumatra'), ('kalimantan/borneo', 'Kalimantan / Borneo'), ('sulawesi', 'Sulawesi'), ('nusaTenggara', 'Nusa Tenggara (Lesser Sunda Islands)'), ('malukuIslands', 'Maluku Islands'), ('papua', 'Papua')], 
                         validators= [InputRequired()])
    userQuery = TextAreaField(label= 'Query', default= "Enter Your query and concerns here...")
    submit_btn = SubmitField('Submit')
    # reset and goBack buttons handled in HTML code

class OTPForm(FlaskForm):
    user_entered_OTP = StringField(label= "Enter OTP", validators=[InputRequired(), Length(min=6, max=6)])
    submit_btn = SubmitField(label= 'Verify OTP')

class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email',validators=[InputRequired(),Email(),Length(max=100)])
    submit = SubmitField('Reqest Password Reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user or not user.is_verified:
            raise ValidationError('Invalid Email')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=100)])
    confirm_password = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')

class UniqueAccessCodeForm(FlaskForm):
    uniqueAccessCode = StringField(label= "Unique Access Code", validators=[InputRequired(), Length(min=8, max=8)])
    submit = SubmitField('Set Up')