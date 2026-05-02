"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, session, url_for
import os
from app.models import Favorite, Pass, User, Profile, Interest, Like, Match, Message, Report 
#from . import db
from app.forms import LoginForm, SignupForm
from datetime import date, datetime  
from werkzeug.utils import secure_filename
from flask import send_from_directory
from datetime import datetime
from flask import  redirect, url_for


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
        
    return jsonify({'message': 'Please use POST to login'}), 405


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


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': 'Logged out successfully'}), 200


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
    
    # Get IDs of passed profiles
    passed_ids = [p.to_user_id for p in Pass.query.filter_by(from_user_id=current_user_id).all()]
    
    location = request.args.get('location', '').strip()
    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    interests_param = request.args.get('interests', '').strip()
    occupation = request.args.get('occupation', '').strip()
    sort_by = request.args.get('sort_by', 'newest')
    
    query = User.query.join(Profile, User.id == Profile.user_id).filter(
        User.id != current_user_id,
        User.id.notin_(passed_ids),
        Profile.visibility == True  
    )
    
    if location:
        query = query.filter(Profile.location.ilike(f'%{location}%'))
    
    if occupation:
        query = query.filter(Profile.occupation.ilike(f'%{occupation}%'))
    
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
        
        if min_age and age and age < min_age:
            continue
        if max_age and age and age > max_age:
            continue
        
        # Build photo URL using url_for()
        photo_url = None
        if profile and profile.profile_photo:
            photo_url = url_for('get_profile_photo', filename=profile.profile_photo)
        
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
            'photo_url': photo_url,
            'created_at': user.created_at.isoformat() if user.created_at else None
        })
    
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
            
            # Build photo URL using url_for()
            photo_url = None
            if profile.profile_photo:
                photo_url = url_for('get_profile_photo', filename=profile.profile_photo)
            
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
                'photo_url': photo_url,
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


# MATCHING SYSTEM ENDPOINTS
# ================================================

@app.route('/api/matching/recommendations', methods=['GET'])
def get_recommendations():
    """
    Get recommended profiles based on matching algorithm
    """
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    current_user = User.query.get(current_user_id)
    current_profile = current_user.profile if current_user else None
    
    # Get IDs of users already liked or passed
    liked_ids = [like.to_user_id for like in Like.query.filter_by(from_user_id=current_user_id).all()]
    passed_ids = [p.to_user_id for p in Pass.query.filter_by(from_user_id=current_user_id).all()]
    excluded_ids = set(liked_ids + passed_ids + [current_user_id])
    
    # Base query - exclude self, liked, passed
    query = User.query.join(Profile).filter(
        User.id.notin_(excluded_ids),
        Profile.visibility == True
    )
    
    recommendations = []
    
    for user in query.all():
        profile = user.profile
        if not profile:
            continue
            
        match_score = 0
        match_reasons = []
        
       
        if current_profile and profile.location == current_profile.location:
            match_score += 25
            match_reasons.append('📍 Same location')
        elif current_profile and profile.location:
            match_score += 10
            match_reasons.append('📍 Nearby')
        
        # ii) Age range preferences
        user_age = user.age
        if user_age:
            
            pref_min = current_profile.preferred_age_min if current_profile else 18
            pref_max = current_profile.preferred_age_max if current_profile else 99
            
            if pref_min <= user_age <= pref_max:
                match_score += 20
                match_reasons.append(f'📅 Age {user_age} (within {pref_min}-{pref_max})')
        
        # iii) Shared interests
        user_interests = set([i.interest for i in user.interests])
        current_interests = set([i.interest for i in current_user.interests])
        shared = user_interests & current_interests
        shared_count = len(shared)
        
        if shared_count > 0:
            match_score += shared_count * 10
            match_reasons.append(f'⭐ {shared_count} shared interests: {", ".join(list(shared)[:3])}')
        
        # iv) Additional matching criterion: Occupation
        if current_profile and profile.occupation:
            if current_profile.occupation == profile.occupation:
                match_score += 15
                match_reasons.append('💼 Same occupation')
        
        # Build photo URL using url_for()
        photo_url = None
        if profile.profile_photo:
            photo_url = url_for('get_profile_photo', filename=profile.profile_photo)
       
        if match_score > 0:
            recommendations.append({
                'profile': {
                    'id': user.id,
                    'username': user.username,
                    'name': f"{user.fname} {user.lname}",
                    'age': user_age,
                    'gender': user.gender,
                    'location': profile.location,
                    'bio': profile.bio,
                    'interests': list(user_interests),
                    'occupation': profile.occupation,
                    'photo_url': photo_url
                },
                'match_score': match_score,
                'match_reasons': match_reasons,
                'shared_interests': list(shared)
            })
    
    # Sort by match score (highest first)
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    
    return jsonify({
        'success': True,
        'count': len(recommendations),
        'data': recommendations
    }), 200


@app.route('/api/matches', methods=['GET'])
def get_matches():
    """Get mutual matches (users who liked you back)"""
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Users who liked current user
    liked_by_others = Like.query.filter_by(to_user_id=current_user_id).all()
    liked_by_others_ids = [like.from_user_id for like in liked_by_others]
    
    # Users that current user liked
    current_user_likes = Like.query.filter_by(from_user_id=current_user_id).all()
    current_user_likes_ids = [like.to_user_id for like in current_user_likes]
    
    # Mutual matches = both conditions
    mutual_match_ids = set(liked_by_others_ids) & set(current_user_likes_ids)
    
    matches = []
    for user_id in mutual_match_ids:
        user = User.query.get(user_id)
        profile = user.profile if user else None
        
        if user and profile and profile.visibility:
            
            like = Like.query.filter_by(from_user_id=user_id, to_user_id=current_user_id).first()
            
            # Build photo URL using url_for()
            photo_url = None
            if profile.profile_photo:
                photo_url = url_for('get_profile_photo', filename=profile.profile_photo)
            
            matches.append({
                'id': user.id,
                'username': user.username,
                'name': f"{user.fname} {user.lname}",
                'age': user.age,
                'location': profile.location,
                'bio': profile.bio,
                'interests': [i.interest for i in user.interests],
                'photo_url': photo_url,
                'matched_at': like.created_at.isoformat() if like else None
            })
    
    return jsonify({'success': True, 'data': matches}), 200


@app.route('/api/like/<int:profile_id>', methods=['POST'])
def like_profile(profile_id):
    """Like a profile"""
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    
    existing = Like.query.filter_by(
        from_user_id=current_user_id,
        to_user_id=profile_id
    ).first()
    
    if existing:
        return jsonify({'success': False, 'message': 'Already liked'}), 409
    
    
    new_like = Like(from_user_id=current_user_id, to_user_id=profile_id)
    db.session.add(new_like)
    db.session.commit()
    
    
    mutual = Like.query.filter_by(
        from_user_id=profile_id,
        to_user_id=current_user_id
    ).first()
    
    return jsonify({
        'success': True,
        'message': 'Liked!',
        'mutual_match': mutual is not None,
        'match_user': {
            'id': mutual.from_user_id if mutual else None,
            'name': User.query.get(profile_id).fname if mutual else None
        } if mutual else None
    }), 201


@app.route('/api/unlike/<int:profile_id>', methods=['DELETE'])
def unlike_profile(profile_id):
    """Remove a like from a profile (unlike/unmatch)"""
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Find the like
    like = Like.query.filter_by(
        from_user_id=current_user_id,
        to_user_id=profile_id
    ).first()
    
    if not like:
        return jsonify({'error': 'Like not found'}), 404
    
    # Check if it was a mutual match (they also liked you)
    mutual = Like.query.filter_by(
        from_user_id=profile_id,
        to_user_id=current_user_id
    ).first()
    
    # Delete the like
    db.session.delete(like)
    
    # If it was a mutual match, also delete the match record
    if mutual:
        match = Match.query.filter(
            ((Match.user1_id == current_user_id) & (Match.user2_id == profile_id)) |
            ((Match.user1_id == profile_id) & (Match.user2_id == current_user_id))
        ).first()
        if match:
            db.session.delete(match)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Like removed',
        'was_mutual': mutual is not None
    }), 200


@app.route('/api/pass/<int:profile_id>', methods=['POST'])
def pass_profile(profile_id):
    """Pass on a profile (won't show again)"""
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    
    existing = Pass.query.filter_by(
        from_user_id=current_user_id,
        to_user_id=profile_id
    ).first()
    
    if not existing:
        new_pass = Pass(from_user_id=current_user_id, to_user_id=profile_id)
        db.session.add(new_pass)
        db.session.commit()
    
    return jsonify({'success': True, 'message': 'Passed'}), 200


@app.route('/api/matches/count', methods=['GET'])
def get_match_count():
    """Get count of mutual matches"""
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    liked_by_others = Like.query.filter_by(to_user_id=current_user_id).all()
    liked_by_others_ids = [like.from_user_id for like in liked_by_others]
    
    current_user_likes = Like.query.filter_by(from_user_id=current_user_id).all()
    current_user_likes_ids = [like.to_user_id for like in current_user_likes]
    
    mutual_match_count = len(set(liked_by_others_ids) & set(current_user_likes_ids))
    
    return jsonify({'success': True, 'count': mutual_match_count}), 200


@app.route('/api/matching/latest', methods=['GET'])
def get_latest_matching_profiles():
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
     # Get IDs of passed profiles
    passed_ids = [p.to_user_id for p in Pass.query.filter_by(from_user_id=current_user_id).all()]
    excluded_ids = set(passed_ids + [current_user_id])

    query = User.query.join(Profile).filter(
        User.id != current_user_id,
        User.id.notin_(excluded_ids),
        Profile.visibility == True
    ).order_by(User.created_at.desc()).limit(20)
    
    results = []
    for user in query.all():
        profile = user.profile
        if profile:
            # Build the full URL for photo using url_for()
            photo_url = None
            if profile.profile_photo:
                photo_url = url_for('get_profile_photo', filename=profile.profile_photo)
            
            results.append({
                'id': user.id,
                'name': f"{user.fname} {user.lname}",
                'age': user.age,
                'location': profile.location,
                'bio': profile.bio,
                'interests': [i.interest for i in user.interests],
                'photo_url': photo_url,
                'occupation': profile.occupation
            })
    
    return jsonify({'success': True, 'data': results}), 200


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
       
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        unique_filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        return unique_filename
    return None


@app.route('/api/liked/check/<int:profile_id>', methods=['GET'])
def check_liked(profile_id):
    """Check if current user has liked a profile"""
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    liked = Like.query.filter_by(
        from_user_id=current_user_id,
        to_user_id=profile_id
    ).first()
    
    return jsonify({
        'success': True,
        'is_liked': liked is not None
    }), 200


# ==========================================
# UPLOAD ENDPOINT
# ==========================================

@app.route('/api/profile/photo', methods=['POST'])
def upload_profile_photo():
    """Upload profile picture for current user"""
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    if 'photo' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['photo']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    filename = save_uploaded_file(file)
    if not filename:
        return jsonify({'error': 'File type not allowed. Use JPG, PNG, or GIF'}), 400
    
    # Update user's profile
    profile = Profile.query.filter_by(user_id=current_user_id).first()
    if profile:
        # Delete old photo if exists
        if profile.profile_photo:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'], profile.profile_photo)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        profile.profile_photo = filename
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile photo uploaded',
            'photo_url': url_for('get_profile_photo', filename=filename)
        }), 200
    
    return jsonify({'error': 'Profile not found'}), 404


@app.route('/api/uploads/<filename>')
def get_profile_photo(filename):
    """Serve profile pictures """
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    return send_from_directory(uploads_dir, filename)










@app.before_request
def check_valid_session():
    """Check if session user_id still exists in database"""
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if not user:
           
            session.clear()
            
            if not request.path.startswith('/api/'):
                return redirect(url_for('login'))
            








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