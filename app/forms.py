from app import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField, SelectField, TextAreaField, MultipleFileField, FileField, DateTimeLocalField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo, Regexp, DataRequired, NumberRange
from app.models import User
from flask_wtf.file import FileAllowed

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

class CreateTaskForm(FlaskForm):
    name = StringField('Task Name', validators=[DataRequired()])
    due_date = DateTimeLocalField('Due Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Create Assignment')
    
class SubmissionForm(FlaskForm):
    file = FileField('Upload File', validators=[FileAllowed(['pdf', 'docx', 'txt', 'zip']), DataRequired()])
    submit = SubmitField('Submit Assignment')

class MaterialForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    text = TextAreaField('Content', validators=[DataRequired(), Length(max=10000)])
    images = MultipleFileField('Upload Images', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    documents = MultipleFileField('Upload Documents', validators=[
        FileAllowed(['pdf', 'docx', 'txt', 'zip'], 'Documents only!')
    ])
    submit = SubmitField('Create Material')


class AddUserCourseForm(FlaskForm):
    email = EmailField('Email',validators=[InputRequired(),Email(),Length(max=100)])
    submit = SubmitField('Add User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user or not user.is_verified:
            raise ValidationError('Invalid Email')
        
    

class CommonRoomMessageForm(FlaskForm):
    text = TextAreaField('Message', validators=[
        DataRequired(), 
        Length(min=1, max=10000, message="Message is too long or empty")
    ])
    
    # Allows users to select more than one image
    images = MultipleFileField('Upload Images', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    
    submit = SubmitField('Post')

class CommonRoomReplyForm(FlaskForm):
    text = StringField('Reply', validators=[
        DataRequired(), 
        Length(min=1, max=5000)
    ])
    
    submit = SubmitField('Reply')

class WorkshopActivityForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    text = TextAreaField('Content', validators=[DataRequired(), Length(max=10000)])
    images = MultipleFileField('Upload Images', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    documents = MultipleFileField('Upload Documents', validators=[
        FileAllowed(['pdf', 'docx', 'txt', 'zip'], 'Documents only!')
    ])
    submit = SubmitField('Create Activity')

class ContributionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    text = TextAreaField('Content', validators=[DataRequired(), Length(max=10000)])
    images = MultipleFileField('Upload Images', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Post')

class ContributionReplyForm(FlaskForm):
    text = StringField('Reply', validators=[
        DataRequired(), 
        Length(min=1, max=5000)
    ])
    
    submit = SubmitField('Reply')

class AddUserOrganisationForm(FlaskForm):
    email = EmailField('Email',validators=[InputRequired(),Email(),Length(max=100)])
    first_name = StringField('First Name',validators=[InputRequired(),Length(max=100)])
    last_name = StringField('Last Name',validators=[InputRequired(),Length(max=100)])
    role = SelectField(label= 'Role', 
                         choices= ["Student", "Teacher", "Admin"], 
                         validators= [InputRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            if user.is_verified or user.organization:
                raise ValidationError('Email already in use.')
            
class CreateCourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    icon = FileField('Course Icon (Optional)', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Create Course')

class SightingForm(FlaskForm):
    title = StringField('What did you see?', validators=[DataRequired()])
    description = TextAreaField('Additional Details')
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'jpeg']), DataRequired()])
    submit = SubmitField('Post Sighting')

class UpdateProfileForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[
        # Removed DataRequired so users can change just the pattern
        FileAllowed(['jpg', 'png', 'jpeg'])
    ])
    pattern = SelectField('Card Style', choices=[
        ('none', 'Classic (Default)'),
        ('pattern-dots', 'Polka Dots'),
        ('pattern-waves', 'Ocean Waves'),
        ('pattern-geo', 'Geometric Green')
    ])
    submit = SubmitField('Update')


class GradeTaskForm(FlaskForm):
    grade = IntegerField('Grade (0-100)', validators=[
        DataRequired(), 
        NumberRange(min=0, max=100)
    ])
    feedback = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Post Grade & Feedback')

class ReplyTaskForm(FlaskForm):
    text = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Send Reply')


class OrganizationForm(FlaskForm):
    name = StringField('Organization Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    org_type = SelectField('Organization Type', choices=[
        ('School', 'School'),
        ('Community', 'Community')
    ])
    icon = FileField('Organisation Icon', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'])
    ])
    submit_btn = SubmitField('Create Organization')
    
