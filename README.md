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

git clone <your-repository-url>
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


FLASK_DEBUG=True
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=8081
SECRET_KEY="some_secret_key"
DATABASE_URL=postgresql://user:password@localhost/database_name


VITE_BACKEND_PORT=8081

# Frontend settings 
VITE_API_URL=http://localhost:8081

NB. All ports must be the same number


#### 2.4 Create uploads folder
mkdir uploads


#### 2.5 Initialize database 
flask db init
flask db migrate
flask db upgrade

#### 2.6 Seed database with test data
flask seed-db

Test user credentials:

Email	            Password	   
alice@example.com	password123	   
bob@example.com	    password123	

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




## API Endpoints




## Known Limitations