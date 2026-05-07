

# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Email, Length, Optional


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = StringField('Password', validators=[InputRequired()])


class SignupForm(FlaskForm):
    """Matches your Vue registration form fields"""
    fname = StringField('First Name', validators=[InputRequired(), Length(max=60)])
    lname = StringField('Last Name', validators=[InputRequired(), Length(max=60)])
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = StringField('Password', validators=[InputRequired(), Length(min=6)])
    gender = SelectField('Gender', choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other')], validators=[InputRequired()])
    date_of_birth = StringField('Date of Birth', validators=[InputRequired()])


class ProfileForm(FlaskForm):
    """Profile form for later use"""
    bio = TextAreaField('Bio', validators=[Optional()])
    location = StringField('Location', validators=[Optional(), Length(max=200)])
    profile_photo = FileField('Profile Photo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!'),
        Optional()
    ])
    visibility = SelectField('Profile Visibility', choices=[('true', 'Public'), ('false', 'Private')], default='true')
    occupation = StringField('Occupation', validators=[Optional(), Length(max=100)])
    zodiac_sign = StringField('Zodiac Sign', validators=[Optional(), Length(max=20)])