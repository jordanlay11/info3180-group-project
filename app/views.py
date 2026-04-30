

"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file
import os
from app.models import User, Profile, Interest, Like, Match, Message, Report 
#from . import db
from app.forms import LoginForm, SignupForm
from datetime import datetime  # ADDED: for date handling


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


#login route 
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password')
        email = data.get('email')

        if not email or not password:
            return jsonify({'error': 'incorrect Email or Password'}), 400

        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            return jsonify({'success': 'User logged in successfully'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401


#signup route 
@app.route('/register', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        age = data.get('age')  
        email = data.get('email')
        gender = data.get('gender') 
        date_of_birth = data.get('date_of_birth') 

        
        if not username or not password or not first_name or not last_name or not email or not gender or not date_of_birth:
            return jsonify({'error': 'Missing required fields'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
            
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400

        
        try:
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        new_user = User(
            username=username,
            email=email,
            password=password,  
            fname=first_name,
            lname=last_name,
            gender=gender,
            date_of_birth=dob
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Create empty profile for the new user
        new_profile = Profile(user_id=new_user.id)
        db.session.add(new_profile)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    else:
        return jsonify({'error': 'Invalid request method'}), 405


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404