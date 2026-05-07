
"""Script to populate database with test data for search & discovery"""

from app import app, db
from app.models import User, Profile, Interest
from datetime import date
from werkzeug.security import generate_password_hash

# Sample data
test_users = [
    {
        'username': 'alice_j',
        'email': 'alice@example.com',
        'password': 'password123',
        'fname': 'Alice',
        'lname': 'Johnson',
        'gender': 'F',
        'date_of_birth': date(1998, 5, 15),
        'bio': 'Love hiking and outdoor adventures. Software engineer who enjoys coffee and nature.',
        'location': 'Kingston',
        'interests': ['Hiking', 'Coffee', 'Reading', 'Technology'],
        'occupation': 'Software Engineer',
        'zodiac_sign': 'Taurus',
        'profile_photo': 'alice_image.jpg' 
    },
    {
        'username': 'bob_smith',
        'email': 'bob@example.com',
        'password': 'password123',
        'fname': 'Bob',
        'lname': 'Smith',
        'gender': 'M',
        'date_of_birth': date(1995, 8, 22),
        'bio': 'Movie enthusiast and gamer. Looking for someone to binge watch with.',
        'location': 'Mona',
        'interests': ['Movies', 'Gaming', 'Music'],
        'occupation': 'Teacher',
        'zodiac_sign': 'Leo',
        'profile_photo': 'bob-image.jpg' 
    },
    {
        'username': 'carol_w',
        'email': 'carol@example.com',
        'password': 'password123',
        'fname': 'Carol',
        'lname': 'Williams',
        'gender': 'F',
        'date_of_birth': date(2000, 3, 10),
        'bio': 'Foodie and traveler. Love trying new restaurants and exploring new places.',
        'location': 'New Kingston',
        'interests': ['Travel', 'Cooking', 'Photography', 'Food'],
        'occupation': 'Designer',
        'zodiac_sign': 'Pisces',
        'profile_photo': 'carol-image.jpg' 
    },
    {
        'username': 'david_b',
        'email': 'david@example.com',
        'password': 'password123',
        'fname': 'David',
        'lname': 'Brown',
        'gender': 'M',
        'date_of_birth': date(1992, 11, 30),
        'bio': 'Fitness enthusiast and personal trainer. Love the gym and healthy living.',
        'location': 'Kingston',
        'interests': ['Gym', 'Running', 'Health', 'Cooking'],
        'occupation': 'Personal Trainer',
        'zodiac_sign': 'Sagittarius',
        'profile_photo': 'david-image.jpg' 
    },
    {
        'username': 'emma_d',
        'email': 'emma@example.com',
        'password': 'password123',
        'fname': 'Emma',
        'lname': 'Davis',
        'gender': 'F',
        'date_of_birth': date(1997, 7, 18),
        'bio': 'Artist and creative soul. Love painting, drawing and all things creative.',
        'location': 'Spanish Town',
        'interests': ['Art', 'Music', 'Photography', 'Reading'],
        'occupation': 'Graphic Designer',
        'zodiac_sign': 'Cancer',
        'profile_photo': 'emma-image.jpg' 
    },
    {
        'username': 'frank_m',
        'email': 'frank@example.com',
        'password': 'password123',
        'fname': 'Frank',
        'lname': 'Miller',
        'gender': 'M',
        'date_of_birth': date(1994, 4, 5),
        'bio': 'Music producer and DJ. Love electronic music and live events.',
        'location': 'Kingston',
        'interests': ['Music', 'Dancing', 'Technology', 'Travel'],
        'occupation': 'Music Producer',
        'zodiac_sign': 'Aries',
        'profile_photo': 'frank-image.jpg' 
    },
    {
        'username': 'grace_h',
        'email': 'grace@example.com',
        'password': 'password123',
        'fname': 'Grace',
        'lname': 'Harris',
        'gender': 'F',
        'date_of_birth': date(1999, 9, 25),
        'bio': 'Book lover and writer. Enjoy quiet evenings with a good book and tea.',
        'location': 'Mona',
        'interests': ['Reading', 'Writing', 'Coffee', 'Art'],
        'occupation': 'Journalist',
        'zodiac_sign': 'Libra',
        'profile_photo': 'grace-image.jpg' 
    },
    {
        'username': 'henry_t',
        'email': 'henry@example.com',
        'password': 'password123',
        'fname': 'Henry',
        'lname': 'Taylor',
        'gender': 'M',
        'date_of_birth': date(1991, 12, 12),
        'bio': 'Tech entrepreneur and start-up founder. Love building things.',
        'location': 'New Kingston',
        'interests': ['Technology', 'Gaming', 'Reading', 'Coffee'],
        'occupation': 'Entrepreneur',
        'zodiac_sign': 'Sagittarius',
        'profile_photo': 'henry-image.jpg' 
    }
]

def seed_database():
    """Populate database with test users"""
    
    print("🌱 Starting database seed...")
    
    # Check if users already exist
    existing_users = User.query.first()
    if existing_users:
        print("⚠️  Database already has users. Skipping seed.")
        print("   (Delete all users first if you want to re-seed)")
        return
    
    print("📝 Creating test users...")
    
    for user_data in test_users:
        # Create user
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],  
            fname=user_data['fname'],
            lname=user_data['lname'],
            gender=user_data['gender'],
            date_of_birth=user_data['date_of_birth']
        )
        db.session.add(user)
        db.session.flush()  
        
        # Create profile
        profile = Profile(
            user_id=user.id,
            bio=user_data['bio'],
            location=user_data['location'],
            visibility=True,
            occupation=user_data.get('occupation'),
            zodiac_sign=user_data.get('zodiac_sign'),
            profile_photo=user_data.get('profile_photo')
        )
        db.session.add(profile)
        
        # Create interests
        for interest_name in user_data['interests']:
            interest = Interest(
                user_id=user.id,
                interest=interest_name
            )
            db.session.add(interest)
        
        print(f"   ✅ Created user: {user_data['username']} ({user_data['fname']} {user_data['lname']})")
    
    # Commit all changes
    db.session.commit()
    
    print("\n✅ Database seed completed!")
    print(f"   📊 Created {len(test_users)} users with profiles and interests")


def clear_database():
    """Clear all users, profiles, and interests (use with caution!)"""
    print("⚠️  Clearing database...")
    
    # Delete in correct order (due to foreign keys)
    Interest.query.delete()
    Profile.query.delete()
    User.query.delete()
    
    db.session.commit()
    
    print("✅ Database cleared!")


if __name__ == '__main__':

    with app.app_context():
        choice = input("Do you want to (s)eed or (c)lear the database? [s/c]: ").lower()
        if choice == 'c':
            clear_database()
        else:
            seed_database()