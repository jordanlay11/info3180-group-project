

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    fname = db.Column(db.String(60), nullable=False)
    lname = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    profile = db.relationship('Profile', back_populates='user', uselist=False)
    interests = db.relationship('Interest', back_populates='user', lazy='dynamic')
    likes_given = db.relationship('Like', foreign_keys='Like.from_user_id', back_populates='from_user')
    likes_received = db.relationship('Like', foreign_keys='Like.to_user_id', back_populates='to_user')
    matches_as_user1 = db.relationship('Match', foreign_keys='Match.user1_id', back_populates='user1')
    matches_as_user2 = db.relationship('Match', foreign_keys='Match.user2_id', back_populates='user2')
    

    def __init__(self, username, email, password, fname, lname, gender, date_of_birth):
        self.username = username
        self.email = email
        self.set_password(password)  
        self.fname = fname
        self.lname = lname
        self.gender = gender
        self.date_of_birth = date_of_birth
    
    def set_password(self, password):
        """Hash and store password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def age(self):
        """Calculate age from date_of_birth"""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    # Login methods
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    bio = db.Column(db.Text)
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    profile_photo = db.Column(db.String(300))
    visibility = db.Column(db.Boolean, default=True)
    occupation = db.Column(db.String(100))
    zodiac_sign = db.Column(db.String(20))
    preferred_location_radius = db.Column(db.Integer, default=50)
    preferred_age_min = db.Column(db.Integer, default=18)
    preferred_age_max = db.Column(db.Integer, default=99)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    user = db.relationship('User', back_populates='profile')
    
    
    def __init__(self, user_id, bio=None, location=None, latitude=None, longitude=None, 
                 profile_photo=None, visibility=True, occupation=None, zodiac_sign=None):
        self.user_id = user_id
        self.bio = bio
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.profile_photo = profile_photo
        self.visibility = visibility
        self.occupation = occupation
        self.zodiac_sign = zodiac_sign
    
    def __repr__(self):
        return f'<Profile for user {self.user_id}>'


class Interest(db.Model):
    __tablename__ = 'interests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interest = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    user = db.relationship('User', back_populates='interests')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'interest', name='unique_user_interest'),
    )
    
    
    def __init__(self, user_id, interest):
        self.user_id = user_id
        self.interest = interest
    
    def __repr__(self):
        return f'<Interest {self.interest} for user {self.user_id}>'


class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    from_user = db.relationship('User', foreign_keys=[from_user_id], back_populates='likes_given')
    to_user = db.relationship('User', foreign_keys=[to_user_id], back_populates='likes_received')
    
    __table_args__ = (
        db.UniqueConstraint('from_user_id', 'to_user_id', name='unique_like'),
    )
    
    
    def __init__(self, from_user_id, to_user_id):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
    
    def __repr__(self):
        return f'<Like from {self.from_user_id} to {self.to_user_id}>'


class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    matched_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    user1 = db.relationship('User', foreign_keys=[user1_id], back_populates='matches_as_user1')
    user2 = db.relationship('User', foreign_keys=[user2_id], back_populates='matches_as_user2')
    
    __table_args__ = (
        db.UniqueConstraint('user1_id', 'user2_id', name='unique_match'),
    )
    
    #
    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id
    
    def __repr__(self):
        return f'<Match between {self.user1_id} and {self.user2_id}>'


class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    match = db.relationship('Match', foreign_keys=[match_id])
    sender = db.relationship('User', foreign_keys=[from_user_id])
    receiver = db.relationship('User', foreign_keys=[to_user_id])
    
    
    def __init__(self, match_id, from_user_id, to_user_id, content):
        self.match_id = match_id
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.content = content
    
    def __repr__(self):
        return f'<Message {self.id}>'


class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reported_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    reporter = db.relationship('User', foreign_keys=[reporter_id])
    reported = db.relationship('User', foreign_keys=[reported_id])
    
    
    def __init__(self, reporter_id, reported_id, reason, status='pending'):
        self.reporter_id = reporter_id
        self.reported_id = reported_id
        self.reason = reason
        self.status = status
    
    def __repr__(self):
        return f'<Report {self.id}>'
    

class Favorite(db.Model):
    """Favorite table - stores profiles that users have saved"""
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    profile = db.relationship('Profile', foreign_keys=[profile_id])
    
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'profile_id', name='unique_favorite'),
    )
    
    def __init__(self, user_id, profile_id):
        self.user_id = user_id
        self.profile_id = profile_id
    
    def __repr__(self):
        return f'<Favorite user={self.user_id} profile={self.profile_id}>'