from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = EmailField('Email',validators=[InputRequired(),Email(),Length(max=100)])
    first_name = StringField('First Name',validators=[InputRequired(),Length(max=100)])
    last_name = StringField('Last Name',validators=[InputRequired(),Length(max=100)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=100)])
    confirm_password = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField('Email',validators=[InputRequired(),Email(),Length(max=100)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=100)])
    submit = SubmitField('Login')