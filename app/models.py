# Add any model classes for Flask-SQLAlchemy here
from . import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'users'
    #id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    fname = db.Column(db.String(60), nullable = False)
    lname = db.Column(db.String(60), nullable = False)
    gender = db.Column(db.String(1), nullable = False)
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    #updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, email, username, password, fname, lname, gender, date_of_birth):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
        
        
class location(db.Model):
    __tablename__= 'location'
    username = db.Column(db.String(80), primary_key=True)
    location = db.Column(db.String(120))
    
    def __init__(self, username, location):
        self.username = username
        self.location = location


class Profile_Picure(db.Model):
    __tablename__ = 'profile_picture'
    
    username = db.Column(db.String(80), primary_key=True)
    profile_pic = db.Column(db.String(300))
    
    def __init__(self, username, profile_pic):
        self.username = username
        self.prifile_pic = profile_pic
        
        
class visibility(db.Model):
    __tablename__ = 'profile_visibility'
    
    username = db.Column(db.String(80), primary_key=True)
    visibility = db.Column(db.Boolean, default=True)
    
    def __init__(self, username, visibility):
        self.username = username
        self.visibility = visibility


class Bio(db.Model):
    __tablename__ = 'user_bio'
    username = db.Column(db.String(80), primary_key=True)
    #id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #first_name = db.Column(db.String(80))
    #last_name = db.Column(db.String(80))
    #date_of_birth = db.Column(db.Date)
    #gender = db.Column(db.String(20))
    #looking_for = db.Column(db.String(50))
    bio = db.Column(db.Text)
    #location = db.Column(db.String(120))
    #latitude = db.Column(db.Float)
    #longitude = db.Column(db.Float)
    #profile_photo = db.Column(db.String(300))
    #visibility = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    #updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, username, bio, location, latitude, longitude, profile_photo, visibility=True):
        self.username = username
        #self.user_id = user_id
        #self.first_name = first_name
        #self.last_name = last_name
        #self.date_of_birth = date_of_birth
        #self.gender = gender
        #self.looking_for = looking_for
        self.bio = bio
        self.location = location
        #self.latitude = latitude
        #self.longitude = longitude
        self.profile_photo = profile_photo
        self.visibility = visibility


class Interest(db.Model):
    __tablename__ = 'interests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), db.ForeignKey('users.username'))
    interest = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, username, interest):
        self.username = username
        self.interest = interest


#class ProfileInterest(db.Model):
    #__tablename__ = 'profile_interests'
    #profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), primary_key=True)
    #interest_id = db.Column(db.Integer, db.ForeignKey('interests.id'), primary_key=True)

    #def __init__(self, profile_id, interest_id):
    #    self.profile_id = profile_id
    #    self.interest_id = interest_id


class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    target_user = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    Suggested_user = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    #action = db.Column(db.String(20))
    #created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, target_user, suggested_user, action):
        self.target_user = target_user
        self.suggested_user = suggested_user
        #self.action = action


class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, db.ForeignKey('likes.id'), primary_key=True)
    user1 = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    user2 = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    #matched_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    sender_name = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    reciever_name =  db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    #is_read = db.Column(db.Boolean, default=False)

    def __init__(self, match_id, sender_id, content):
        self.match_id = match_id
        self.sender_id = sender_id
        self.content = content


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    reporter = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    reported_user = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, reporter_id, reported_id, reason, status='pending'):
        self.reporter_id = reporter_id
        self.reported_id = reported_id
        self.reason = reason
        self.status = status
