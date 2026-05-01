

"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, session
import os
from app.models import Favorite, User, Profile, Interest, Like, Match, Message, Report 
#from . import db
from app.forms import LoginForm, SignupForm
from datetime import date, datetime  



###
# Routing for your application.
###

def calculate_age(birth_date):
    """Calculate age from date of birth"""
    if not birth_date:
        return None
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))







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
            
            session['user_id'] = user.id
            session['username'] = user.username
            
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


##########################################################################


@app.route('/api/search', methods=['GET'])
def search_profiles():
    """
    Search profiles with filters
   
    """
    
 
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required. Please log in.'
        }), 401
    
   
    location = request.args.get('location', '').strip()
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    interests_param = request.args.get('interests', '').strip()
    occupation = request.args.get('occupation', '').strip()
    sort_by = request.args.get('sort_by', 'newest')
    
  
    query = User.query.join(Profile, User.id == Profile.user_id).filter(
        User.id != current_user_id,
        Profile.visibility == True  
    )
    
   
    if location:
        query = query.filter(Profile.location.ilike(f'%{location}%'))
    
    # Filter 2: Occupation (partial match, case-insensitive)
    if occupation:
        query = query.filter(Profile.occupation.ilike(f'%{occupation}%'))
    
    # Filter 3: Age Range (using date_of_birth)
    if min_age or max_age:
        today = date.today()
        
        
        if max_age:
            min_birth_date = date(today.year - max_age, today.month, today.day)
            query = query.filter(User.date_of_birth >= min_birth_date)
        
       
        if min_age:
            max_birth_date = date(today.year - min_age, today.month, today.day)
            query = query.filter(User.date_of_birth <= max_birth_date)
    
    
    if interests_param:
        interest_list = [i.strip() for i in interests_param.split(',')]

        query = query.join(User.interests).filter(
            Interest.interest.in_(interest_list)
        ).distinct()
    
   
    if sort_by == 'newest':
        query = query.order_by(User.created_at.desc())
    elif sort_by == 'oldest':
        query = query.order_by(User.created_at.asc())
    elif sort_by == 'location_asc':
        query = query.order_by(Profile.location.asc())
    elif sort_by == 'location_desc':
        query = query.order_by(Profile.location.desc())
    
    
   
    users = query.all()
    
    results = []
    for user in users:
        profile = user.profile
        interests = [i.interest for i in user.interests]
        age = calculate_age(user.date_of_birth)
        
        # Apply age filters in Python (for cases where age calculation is complex)
        if min_age and age and age < min_age:
            continue
        if max_age and age and age > max_age:
            continue
        
        results.append({
            'id': user.id,
            'username': user.username,
            'fname': user.fname,
            'lname': user.lname,
            'name': f"{user.fname} {user.lname}",
            'age': age,
            'gender': user.gender,
            'location': profile.location if profile else None,
            'bio': profile.bio if profile else None,
            'interests': interests,
            'occupation': profile.occupation if profile else None,
            'zodiac_sign': profile.zodiac_sign if profile else None,
            'photo_url': profile.profile_photo if profile else None,
            'created_at': user.created_at.isoformat() if user.created_at else None
        })
    
    # Apply age sorting in Python (since age is calculated)
    if sort_by == 'age_asc':
        results.sort(key=lambda x: x['age'] if x['age'] is not None else 999)
    elif sort_by == 'age_desc':
        results.sort(key=lambda x: x['age'] if x['age'] is not None else 0, reverse=True)
   

    return jsonify({
        'success': True,
        'count': len(results),
        'filters_applied': {
            'location': location if location else None,
            'min_age': min_age,
            'max_age': max_age,
            'interests': interests_param if interests_param else None,
            'occupation': occupation if occupation else None,
            'sort_by': sort_by
        },
        'data': results
    }), 200


@app.route('/api/search/interests', methods=['GET'])
def get_all_interests():
    """
    
    """
    interests = db.session.query(Interest.interest).distinct().order_by(Interest.interest).all()
    interest_list = [i[0] for i in interests]
    
    return jsonify({
        'success': True,
        'count': len(interest_list),
        'data': interest_list
    }), 200






@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """
    Get all favorited profiles for the current user
    Returns list of profile objects with full details
    """
    # Get current logged-in user
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Get all favorites for this user
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    
    # Build response with profile details
    results = []
    for fav in favorites:
        profile = fav.profile
        user = profile.user if profile else None
        
        if profile and user:
            # Get interests for this user
            interests = [i.interest for i in user.interests]
            
            results.append({
                'favorite_id': fav.id,
                'profile_id': profile.id,
                'user_id': user.id,
                'username': user.username,
                'name': f"{user.fname} {user.lname}",
                'age': user.age,
                'location': profile.location,
                'bio': profile.bio,
                'interests': interests,
                'occupation': profile.occupation,
                'zodiac_sign': profile.zodiac_sign,
                'photo_url': profile.profile_photo,
                'favorited_at': fav.created_at.isoformat() if fav.created_at else None
            })
    
    return jsonify({
        'success': True,
        'count': len(results),
        'data': results
    }), 200


@app.route('/api/favorites/<int:profile_id>', methods=['POST'])
def add_favorite(profile_id):
    """
    Add a profile to favorites
    """
    # Get current logged-in user
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Check if profile exists
    profile = Profile.query.get(profile_id)
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    # Check if already favorited
    existing = Favorite.query.filter_by(
        user_id=current_user_id,
        profile_id=profile_id
    ).first()
    
    if existing:
        return jsonify({
            'success': False,
            'message': 'Profile already in favorites',
            'favorite_id': existing.id
        }), 409  # 409 Conflict
    
    # Create new favorite
    favorite = Favorite(
        user_id=current_user_id,
        profile_id=profile_id
    )
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Profile added to favorites',
        'favorite_id': favorite.id,
        'profile_id': profile_id
    }), 201


@app.route('/api/favorites/<int:profile_id>', methods=['DELETE'])
def remove_favorite(profile_id):
    """
    Remove a profile from favorites
    """
    # Get current logged-in user
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Find the favorite
    favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        profile_id=profile_id
    ).first()
    
    if not favorite:
        return jsonify({
            'success': False,
            'error': 'Favorite not found'
        }), 404
    
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Profile removed from favorites',
        'profile_id': profile_id
    }), 200


@app.route('/api/favorites/check/<int:profile_id>', methods=['GET'])
def check_favorite(profile_id):
    """
    Check if a profile is favorited by current user
    Useful for frontend to show correct star/heart state
    """
    # Get current logged-in user
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Check if favorited
    favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        profile_id=profile_id
    ).first()
    
    return jsonify({
        'success': True,
        'is_favorited': favorite is not None,
        'favorite_id': favorite.id if favorite else None
    }), 200





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