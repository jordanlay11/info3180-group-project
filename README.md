# LuvIsland - Dating Application

This is dating site built with Vue 3 for the frontend and Flask for the backend. Users can create profiles, discover compatible matches, like/pass on profiles, and connect with mutual matches.

## Team Members

- Ashley Chung - Project Lead
- Tamarica Shaw - Backend Lead
- Jordan Laylor - Frontend Lead
- Gavril Williams - QA Lead
- William Whitelocke - Deployment Lead



## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 
- Git

---

## Setup Instructions

### Step 1: Clone the Repository

git clone https://github.com/jordanlay11/info3180-group-project.git
cd info3180-group-project


### Step 2: Clone the Repository

#### 2.1 Create and Activate Virtual Environment

For Windows

python -m venv venv
venv\Scripts\activate

For Mac

python3 -m venv venv
source venv/bin/activate

#### 2.2 Install backend dependencies
pip install -r requirements.txt

#### 2.3 Configure environment variables
Create a .env file in the root of the project
Copy the below and change the database and ports


FLASK_DEBUG=True
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=8081
SECRET_KEY="some_secret_key"
UPLOAD_FOLDER =uploads
DATABASE_URL=postgresql://user:password@localhost/database_name


VITE_BACKEND_PORT=8081

# Frontend settings 
VITE_API_URL=http://localhost:8081

NB. All ports must be the same number


#### 2.4 Initialize database 
flask db upgrade

#### 2.5 Seed database with test data
flask seed-db


#### Start backend server
flask --app app --debug run


### Setup Frontend

#### 3.1 Install dependencies
open a new terminal and run 

npm install

#### 3.2 Start frontend server
npm run dev


### Step 4
Go to your browser at this url 

http://localhost:5173

Test user credentials:

Email	            Password	   
alice@example.com	password123	   
bob@example.com	    password123	




## API Endpoints


### Authentication Endpoints
Most endpoints require authentication via session cookie. Login first to establish a session.

#### Register a new user
**POST** `/register`

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "gender": "M",
  "date_of_birth": "1995-06-15"
}
Response (201 Created):

json
{
  "message": "User created successfully"
}
Error Responses:

400 Bad Request - Missing required fields

400 Bad Request - Invalid date format

400 Bad Request - Username already exists

400 Bad Request - Email already exists

Login
POST /login

Request Body:

json
{
  "email": "john@example.com",
  "password": "securepassword"
}
Response (200 OK):

json
{
  "success": "User logged in successfully"
}
Error Responses:

400 Bad Request - Incorrect email or password

401 Unauthorized - Invalid credentials

Logout
POST /logout

Response (200 OK):

json
{
  "success": "Logged out successfully"
}
User Endpoints
Get current user basic info
GET /api/user/me

Response (200 OK):

json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "fname": "John",
    "lname": "Doe"
  }
}
Get current user full profile
GET /api/user/info

Response (200 OK):

json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "johndoe",
    "fname": "John",
    "lname": "Doe",
    "email": "john@example.com",
    "gender": "M",
    "date_of_birth": "1995-06-15",
    "bio": "I love hiking and coding!",
    "location": "Kingston, Jamaica",
    "occupation": "Software Developer",
    "zodiac_sign": "Virgo",
    "interests": ["Hiking", "Music", "Coding"],
    "profile_photo": "20250101_120000_photo.jpg",
    "visibility": true,
    "preferred_age_min": 22,
    "preferred_age_max": 35,
    "preferred_location_radius": 50,
    "match_count": 3,
    "likes_received": 10,
    "looking_for_gender": "all",
    "profile_views": 45
  }
}
Get another user's profile
GET /api/profile/{user_id}

Parameters:

Name	Type	Description
user_id	integer	ID of the user to view
Response (200 OK):

json
{
  "success": true,
  "data": {
    "id": 2,
    "username": "janedoe",
    "fname": "Jane",
    "lname": "Doe",
    "gender": "F",
    "date_of_birth": "1998-03-20",
    "age": 27,
    "bio": "Love traveling and photography",
    "location": "Mona, Jamaica",
    "occupation": "Designer",
    "zodiac_sign": "Pisces",
    "interests": ["Travel", "Photography", "Music"],
    "profile_photo": "20250101_120000_photo.jpg",
    "preferred_age_min": 22,
    "preferred_age_max": 35,
    "preferred_location_radius": 50,
    "looking_for_gender": "all",
    "match_count": 5,
    "likes_received": 8,
    "profile_views": 32
  }
}
Error Responses:

401 Unauthorized - Not logged in

403 Forbidden - Profile is private

404 Not Found - User or profile not found

Update current user profile
PUT /api/profile/update

Request Body:

json
{
  "bio": "Updated bio text",
  "location": "Kingston, Jamaica",
  "occupation": "Senior Developer",
  "zodiac_sign": "Leo",
  "interests": ["Hiking", "Music", "Travel", "Photography"],
  "visibility": true,
  "looking_for_gender": "all",
  "preferred_age_min": 25,
  "preferred_age_max": 40,
  "preferred_location_radius": 75
}
Response (200 OK):

json
{
  "success": true,
  "message": "Profile updated successfully"
}
Upload profile photo
POST /api/profile/photo

Request: multipart/form-data with field photo

Response (200 OK):

json
{
  "success": true,
  "message": "Profile photo uploaded",
  "photo_url": "/api/uploads/20250101_120000_photo.jpg"
}
Serve profile photo
GET /api/uploads/{filename}

Returns the image file directly.

Matching & Recommendations
Get match recommendations
GET /api/matching/recommendations

Response (200 OK):

json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "profile": {
        "id": 3,
        "username": "alice",
        "name": "Alice Johnson",
        "age": 28,
        "gender": "F",
        "location": "Kingston, Jamaica",
        "bio": "Love hiking and coffee",
        "interests": ["Hiking", "Coffee", "Reading"],
        "occupation": "Engineer",
        "photo_url": "/api/uploads/alice.jpg"
      },
      "match_score": 85,
      "match_reasons": [
        "📍 Same location",
        "⭐ 2 shared interests: Hiking, Coffee",
        "💼 Same occupation"
      ],
      "shared_interests": ["Hiking", "Coffee"]
    }
  ]
}
Get latest matching profiles
GET /api/matching/latest

Response (200 OK):

json
{
  "success": true,
  "data": [
    {
      "id": 3,
      "name": "Alice Johnson",
      "age": 28,
      "location": "Kingston, Jamaica",
      "bio": "Love hiking and coffee",
      "interests": ["Hiking", "Coffee", "Reading"],
      "photo_url": "/api/uploads/alice.jpg",
      "occupation": "Engineer"
    }
  ]
}
Likes & Matches
Like a profile
POST /api/like/{profile_id}

Response (201 Created):

json
{
  "success": true,
  "message": "Liked!",
  "mutual_match": false,
  "match_id": null,
  "match_user": null
}
Mutual match response:

json
{
  "success": true,
  "message": "Liked!",
  "mutual_match": true,
  "match_id": 123,
  "match_user": {
    "id": 3,
    "name": "Alice"
  }
}
Error Responses:

409 Conflict - Already liked this profile

Unlike a profile
DELETE /api/unlike/{profile_id}

Response (200 OK):

json
{
  "success": true,
  "message": "Like removed",
  "was_mutual": false
}
Check if user liked a profile
GET /api/liked/check/{profile_id}

Response (200 OK):

json
{
  "success": true,
  "is_liked": true
}
Pass on a profile
POST /api/pass/{profile_id}

Response (200 OK):

json
{
  "success": true,
  "message": "Passed"
}
Get mutual matches
GET /api/matches

Response (200 OK):

json
{
  "success": true,
  "data": [
    {
      "id": 3,
      "username": "alice",
      "name": "Alice Johnson",
      "age": 28,
      "location": "Kingston, Jamaica",
      "bio": "Love hiking and coffee",
      "interests": ["Hiking", "Coffee", "Reading"],
      "photo_url": "/api/uploads/alice.jpg",
      "matched_at": "2025-01-15T10:30:00"
    }
  ]
}
Get match count
GET /api/matches/count

Response (200 OK):

json
{
  "success": true,
  "count": 5
}
Search & Discovery
Search profiles
GET /api/search

Query Parameters:

Name	Type	Description
location	string	Filter by location (partial match)
min_age	integer	Minimum age filter
max_age	integer	Maximum age filter
interests	string	Comma-separated interests
sort_by	string	newest, oldest, age_asc, age_desc, location_asc, location_desc
Example:

text
GET /api/search?location=Kingston&min_age=25&max_age=35&interests=Music,Travel&sort_by=newest
Response (200 OK):

json
{
  "success": true,
  "count": 10,
  "filters_applied": {
    "location": "Kingston",
    "min_age": 25,
    "max_age": 35,
    "interests": "Music,Travel",
    "occupation": null,
    "sort_by": "newest"
  },
  "data": [
    {
      "id": 3,
      "username": "alice",
      "fname": "Alice",
      "lname": "Johnson",
      "name": "Alice Johnson",
      "age": 28,
      "gender": "F",
      "location": "Kingston, Jamaica",
      "bio": "Love hiking and coffee",
      "interests": ["Hiking", "Music", "Travel"],
      "occupation": "Engineer",
      "zodiac_sign": "Virgo",
      "photo_url": "/api/uploads/alice.jpg",
      "created_at": "2025-01-10T12:00:00"
    }
  ]
}
Get all interests
GET /api/search/interests

Response (200 OK):

json
{
  "success": true,
  "count": 18,
  "data": ["Art", "Coding", "Coffee", "Gaming", "Hiking", "Music", "Photography", "Reading", "Travel"]
}
Favorites
Get favorites list
GET /api/favorites

Response (200 OK):

json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "favorite_id": 1,
      "profile_id": 5,
      "user_id": 5,
      "username": "bob",
      "name": "Bob Smith",
      "age": 32,
      "location": "Kingston",
      "bio": "Movie enthusiast",
      "interests": ["Movies", "Gaming"],
      "occupation": "Teacher",
      "zodiac_sign": "Leo",
      "photo_url": "/api/uploads/bob.jpg",
      "favorited_at": "2025-01-20T14:30:00"
    }
  ]
}
Add to favorites
POST /api/favorites/{profile_id}

Response (201 Created):

json
{
  "success": true,
  "message": "Profile added to favorites",
  "favorite_id": 10,
  "profile_id": 5
}
Remove from favorites
DELETE /api/favorites/{profile_id}

Response (200 OK):

json
{
  "success": true,
  "message": "Profile removed from favorites",
  "profile_id": 5
}
Check favorite status
GET /api/favorites/check/{profile_id}

Response (200 OK):

json
{
  "success": true,
  "is_favorited": true,
  "favorite_id": 10
}
Messaging
Get chat list
GET /api/messages/chats

Response (200 OK):

json
{
  "success": true,
  "data": [
    {
      "match_id": 123,
      "name": "Alice Johnson",
      "receiver_id": 3,
      "last_message": "Hey! How are you?",
      "sent_at": "2025-01-20T15:45:00"
    }
  ]
}
Get conversation
GET /api/messages/conversation/{match_id}

Response (200 OK):

json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "content": "Hello! Great to match with you!",
      "from_user_id": 1,
      "to_user_id": 3,
      "sent_at": "2025-01-20T15:30:00",
      "is_read": true
    },
    {
      "id": 2,
      "content": "Hey! How are you?",
      "from_user_id": 3,
      "to_user_id": 1,
      "sent_at": "2025-01-20T15:45:00",
      "is_read": false
    }
  ]
}
Send message
POST /api/messages/send/{match_id}

Request Body:

json
{
  "content": "Hello! Great to match with you!"
}
Response (201 Created):

json
{
  "success": true,
  "data": {
    "id": 3,
    "content": "Hello! Great to match with you!",
    "from_user_id": 1,
    "to_user_id": 3,
    "sent_at": "2025-01-20T16:00:00"
  }
}
Get matches without messages (for new conversations)
GET /api/messages/matches

Response (200 OK):

json
{
  "success": true,
  "data": [
    {
      "match_id": 456,
      "name": "Bob Smith",
      "receiver_id": 5
    }
  ]
}
Moderation
Block a user
POST /api/block/{user_id}

Response (201 Created):

json
{
  "success": true,
  "message": "User blocked"
}
Unblock a user
POST /api/unblock/{user_id}

Response (200 OK):

json
{
  "success": true,
  "message": "User unblocked"
}
Report a user
POST /api/report/{user_id}

Request Body:

json
{
  "reason": "Inappropriate behavior"
}
Response (201 Created):

json
{
  "success": true,
  "message": "User reported"
}



## Known Limitations