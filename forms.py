from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo, Regexp, DataRequired

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