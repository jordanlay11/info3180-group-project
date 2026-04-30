# Add any form classes for Flask-WTF herefrom flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    #email = StringField('Email', validators=[InputRequired()])

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    age = StringField('Age', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])

class ProfileForm(FlaskForm):
    bio = TextAreaField('Bio')
    profile_photo = FileField('Profile Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    