"""
LuvIsland API Test Suite
Run with: python test_app.py
"""

import json
import time
import http.client
import urllib.parse
import os
from datetime import datetime
import sys

def find_backend_port():
    
    # Priority 1: Command line argument
   
    for arg in sys.argv:
        if arg.startswith('--port='):
            return int(arg.split('=')[1])
    
    # Priority 2: Environment variable VITE_BACKEND_PORT
    backend_port = os.environ.get('VITE_BACKEND_PORT')
    if backend_port:
        return int(backend_port)
    
    # Priority 3: Environment variable VITE_API_URL
    api_url = os.environ.get('VITE_API_URL')
    if api_url:
        # Extract port from URL like http://localhost:8081
        if ':' in api_url:
            parts = api_url.split(':')
            if len(parts) >= 3:
                port = parts[2].split('/')[0]
                return int(port)
    
    # Priority 4: Check .env file in current directory
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Check for VITE_BACKEND_PORT
                if line.startswith('VITE_BACKEND_PORT='):
                    return int(line.split('=')[1])
                # Check for VITE_API_URL
                if line.startswith('VITE_API_URL='):
                    url = line.split('=')[1]
                    if ':' in url:
                        parts = url.split(':')
                        if len(parts) >= 3:
                            port = parts[2].split('/')[0]
                            return int(port)
    
    # Priority 5: Check .flaskenv file for FLASK_RUN_PORT
    flaskenv_file = os.path.join(os.path.dirname(__file__), '.flaskenv')
    if os.path.exists(flaskenv_file):
        with open(flaskenv_file, 'r') as f:
            for line in f:
                if line.startswith('FLASK_RUN_PORT='):
                    return int(line.split('=')[1])
    
    # Priority 6: Default to 8081
    return 8081

def get_api_url():
    """Get full API URL from various sources"""
    port = find_backend_port()
    return f"http://localhost:{port}"

# Get configuration
API_URL = get_api_url()
BACKEND_PORT = find_backend_port()

print(f"\n{'='*60}")
print(f"🔧 Test Configuration")
print(f"{'='*60}")
print(f"  API URL: {API_URL}")
print(f"  Backend Port: {BACKEND_PORT}")
print(f"{'='*60}\n")

# Extract host and port from URL
if "://" in API_URL:
    parts = API_URL.split("://")[1].split(":")
    BASE_HOST = parts[0]
    BASE_PORT = int(parts[1].split("/")[0])
else:
    BASE_HOST = "localhost"
    BASE_PORT = BACKEND_PORT

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

class LuvIslandTester:
    def __init__(self):
        self.conn = None
        self.cookies = ""
        self.test_user = None
        self.test_user2 = None
        self.user1_id = None
        self.user2_id = None
        self.match_id = None
        self.passed = 0
        self.failed = 0
        self.timestamp = int(time.time())
    
    def _request(self, method, path, body=None):
        """Make HTTP request and return response"""
        self.conn = http.client.HTTPConnection(BASE_HOST, BASE_PORT)
        headers = {'Content-Type': 'application/json'}
        if self.cookies:
            headers['Cookie'] = self.cookies
        
        if body:
            body_str = json.dumps(body)
            self.conn.request(method, path, body_str, headers)
        else:
            self.conn.request(method, path, None, headers)
        
        response = self.conn.getresponse()
        data = response.read().decode()
        
        # Save cookies from response
        if response.getheader('Set-Cookie'):
            self.cookies = response.getheader('Set-Cookie')
        
        self.conn.close()
        
        return {
            'status': response.status,
            'data': json.loads(data) if data else {}
        }
    
    def print_header(self, text):
        print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.CYAN}{text}{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    def print_result(self, test_name, passed, details=""):
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"  {status} {test_name}")
        if details:
            print(f"      {Colors.CYAN}→{Colors.RESET} {details}")
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.YELLOW}📊 TEST SUMMARY{Colors.RESET}")
        print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"  ✅ Passed: {self.passed}")
        print(f"  ❌ Failed: {self.failed}")
        print(f"  📈 Total:  {self.passed + self.failed}")
        
        if self.failed == 0:
            print(f"\n{Colors.GREEN}🎉 ALL TESTS PASSED!{Colors.RESET}\n")
        else:
            print(f"\n{Colors.RED}⚠️ {self.failed} test(s) failed.{Colors.RESET}\n")
    
    # ==========================================
    # 1. USER AUTHENTICATION TESTS
    # ==========================================
    def test_authentication(self):
        self.print_header("🔐 1. USER AUTHENTICATION TESTS")
        
        # 1.1 Register User 1
        self.test_user = {
            "username": f"tester1_{self.timestamp}",
            "email": f"tester1_{self.timestamp}@test.com",
            "password": "TestPass123!",
            "first_name": "Test",
            "last_name": "User1",
            "gender": "M",
            "date_of_birth": "1995-06-15"
        }
        
        resp = self._request("POST", "/register", self.test_user)
        passed = resp['status'] == 201
        self.print_result("1.1 User Registration", passed, self.test_user['username'])
        
        # 1.2 Register User 2
        self.test_user2 = {
            "username": f"tester2_{self.timestamp}",
            "email": f"tester2_{self.timestamp}@test.com",
            "password": "TestPass123!",
            "first_name": "Test",
            "last_name": "User2",
            "gender": "F",
            "date_of_birth": "1998-03-20"
        }
        
        resp = self._request("POST", "/register", self.test_user2)
        passed = resp['status'] == 201
        self.print_result("1.2 Register Second User", passed, self.test_user2['username'])
        
        # 1.3 Duplicate Registration (should fail)
        resp = self._request("POST", "/register", self.test_user)
        passed = resp['status'] == 400
        self.print_result("1.3 Duplicate Registration (should fail)", passed, "Email/Username already exists")
        
        # 1.4 Login User 1
        login_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        }
        resp = self._request("POST", "/login", login_data)
        passed = resp['status'] == 200 and resp['data'].get('success') == 'User logged in successfully'
        
        # Get user ID
        me_resp = self._request("GET", "/api/user/me")
        if me_resp['status'] == 200:
            self.user1_id = me_resp['data'].get('data', {}).get('id')
        
        self.print_result("1.4 User Login", passed, f"User {self.user1_id} logged in")
        
        # 1.5 Invalid Login (should fail)
        bad_login = {"email": "wrong@email.com", "password": "wrongpass"}
        resp = self._request("POST", "/login", bad_login)
        passed = resp['status'] == 401
        self.print_result("1.5 Invalid Login (should fail)", passed, "Returns 401 Unauthorized")
        
        # 1.6 Logout
        resp = self._request("POST", "/logout")
        passed = resp['status'] == 200
        self.print_result("1.6 Logout", passed, "Session cleared")
    
    # ==========================================
    # 2. PROFILE MANAGEMENT TESTS
    # ==========================================
    def test_profile_management(self):
        self.print_header("👤 2. PROFILE MANAGEMENT TESTS")
        
        # Login first
        login_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        }
        self._request("POST", "/login", login_data)
        
        # 2.1 Get Current User Info
        resp = self._request("GET", "/api/user/info")
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        
        if passed:
            self.print_result("2.1 Get User Info", passed, f"User: {resp['data']['data'].get('fname')} {resp['data']['data'].get('lname')}")
        else:
            self.print_result("2.1 Get User Info", passed, str(resp['data'].get('error', 'Unknown error')))
        
        # 2.2 Update Profile
        profile_data = {
            "bio": "I love hiking, coding, and meeting new people!",
            "location": "Kingston, Jamaica",
            "occupation": "Software Developer",
            "zodiac_sign": "Virgo",
            "interests": ["Hiking", "Music", "Travel", "Coding"],
            "visibility": True,
            "looking_for_gender": "all",
            "preferred_age_min": 22,
            "preferred_age_max": 35,
            "preferred_location_radius": 50
        }
        resp = self._request("PUT", "/api/profile/update", profile_data)
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        self.print_result("2.2 Update Profile", passed, "Bio, location, interests updated")
        
        # 2.3 Verify Profile Updates
        resp = self._request("GET", "/api/user/info")
        profile = resp['data'].get('data', {})
        passed = (profile.get('bio') == "I love hiking, coding, and meeting new people!" and
                 profile.get('location') == "Kingston, Jamaica")
        self.print_result("2.3 Verify Profile Updates", passed, "Changes persisted")
    
    # ==========================================
    # 3. MATCHING SYSTEM TESTS
    # ==========================================
    def test_matching_system(self):
        self.print_header("💕 3. MATCHING SYSTEM TESTS")
        
        # 3.1 Get Recommendations
        resp = self._request("GET", "/api/matching/recommendations")
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        self.print_result("3.1 Get Recommendations", passed, f"Found {resp['data'].get('count', 0)} recommendations")
        
        # 3.2 Get Latest Matching Profiles
        resp = self._request("GET", "/api/matching/latest")
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        self.print_result("3.2 Get Latest Profiles", passed, f"Found {len(resp['data'].get('data', []))} profiles")
        
        # 3.3 Get Match Count
        resp = self._request("GET", "/api/matches/count")
        passed = resp['status'] == 200 and 'count' in resp['data']
        self.print_result("3.3 Get Match Count", passed, f"Current matches: {resp['data'].get('count', 0)}")
    
    # ==========================================
    # 4. LIKES AND MUTUAL MATCHES TESTS
    # ==========================================
    def test_likes_and_matches(self):
        self.print_header("❤️ 4. LIKES & MUTUAL MATCHES TESTS")
        
        # Login as User 2 to get their ID
        login_data = {
            "email": self.test_user2["email"],
            "password": self.test_user2["password"]
        }
        self._request("POST", "/login", login_data)
        
        # Get User 2 ID
        me_resp = self._request("GET", "/api/user/me")
        if me_resp['status'] == 200:
            self.user2_id = me_resp['data'].get('data', {}).get('id')
        
        # Switch back to User 1
        login_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        }
        self._request("POST", "/login", login_data)
        
        if self.user2_id:
            # 4.1 Like another user
            resp = self._request("POST", f"/api/like/{self.user2_id}")
            passed = resp['status'] == 201 and resp['data'].get('success') == True
            self.print_result("4.1 Like User", passed, f"Liked user {self.user2_id}")
            
            # 4.2 Check if already liked (should return 409)
            resp = self._request("POST", f"/api/like/{self.user2_id}")
            passed = resp['status'] == 409
            self.print_result("4.2 Duplicate Like (should fail)", passed, "Already liked")
            
            # 4.3 Check like status
            resp = self._request("GET", f"/api/liked/check/{self.user2_id}")
            passed = resp['status'] == 200 and resp['data'].get('is_liked') == True
            self.print_result("4.3 Check Like Status", passed, "Like confirmed")
        
        # 4.4 Create mutual match
        if self.user2_id:
            # Login as User 2
            login_data = {
                "email": self.test_user2["email"],
                "password": self.test_user2["password"]
            }
            self._request("POST", "/login", login_data)
            
            resp = self._request("POST", f"/api/like/{self.user1_id}")
            passed = resp['status'] == 201 and resp['data'].get('mutual_match') == True
            if passed and resp['data'].get('match_id'):
                self.match_id = resp['data'].get('match_id')
            self.print_result("4.4 Mutual Match Creation", passed, "🎉 It's a match!")
            
            # 4.5 Get matches list
            resp = self._request("GET", "/api/matches")
            passed = resp['status'] == 200 and resp['data'].get('success') == True
            self.print_result("4.5 Get Matches List", passed, f"Found {len(resp['data'].get('data', []))} matches")
    
    # ==========================================
    # 5. MESSAGING TESTS
    # ==========================================
    def test_messaging(self):
        self.print_header("💬 5. MESSAGING TESTS")
        
        if not self.match_id:
            self.print_result("5.x Messaging Tests", False, "No match available (skip)")
            return
        
        # 5.1 Send message
        message_data = {"content": "Hello! Great to match with you!"}
        resp = self._request("POST", f"/api/messages/send/{self.match_id}", message_data)
        passed = resp['status'] == 201 and resp['data'].get('success') == True
        self.print_result("5.1 Send Message", passed, "Message sent")
        
        # 5.2 Get conversation
        resp = self._request("GET", f"/api/messages/conversation/{self.match_id}")
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        message_count = len(resp['data'].get('data', []))
        self.print_result("5.2 Get Conversation", passed, f"Retrieved {message_count} messages")
        
        # 5.3 Get chats list
        resp = self._request("GET", "/api/messages/chats")
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        self.print_result("5.3 Get Chats List", passed, f"Found {len(resp['data'].get('data', []))} chats")
        
        # 5.4 Send second message
        message_data = {"content": "How are you today?"}
        resp = self._request("POST", f"/api/messages/send/{self.match_id}", message_data)
        passed = resp['status'] == 201
        self.print_result("5.4 Send Second Message", passed, "Message persisted")
    
    # ==========================================
    # 6. SEARCH & DISCOVERY TESTS
    # ==========================================
    def test_search_and_discovery(self):
        self.print_header("🔍 6. SEARCH & DISCOVERY TESTS")
        
        # 6.1 Search by location
        resp = self._request("GET", "/api/search?location=Kingston")
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        self.print_result("6.1 Search by Location", passed, f"Found {resp['data'].get('count', 0)} results")
        
        # 6.2 Search by age range
        resp = self._request("GET", "/api/search?min_age=25&max_age=35")
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        self.print_result("6.2 Search by Age Range", passed, f"Found {resp['data'].get('count', 0)} results")
        
        # 6.3 Search by interests
        resp = self._request("GET", "/api/search?interests=Music,Travel")
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        self.print_result("6.3 Search by Interests", passed, f"Found {resp['data'].get('count', 0)} results")
        
        # 6.4 Sort by newest
        resp = self._request("GET", "/api/search?sort_by=newest")
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        self.print_result("6.4 Sort by Newest", passed, f"First result: {resp['data'].get('data', [{}])[0].get('name', 'N/A') if resp['data'].get('data') else 'None'}")
        
        # 6.5 Sort by age (youngest first)
        resp = self._request("GET", "/api/search?sort_by=age_asc")
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        self.print_result("6.5 Sort by Age (Youngest)", passed, "Sorting working")
        
        # 6.6 Get all interests
        resp = self._request("GET", "/api/search/interests")
        passed = resp['status'] == 200 and resp['data'].get('success') == True
        self.print_result("6.6 Get Interests List", passed, f"Found {resp['data'].get('count', 0)} unique interests")
    
    # ==========================================
    # 7. FAVORITES TESTS
    # ==========================================
    def test_favorites(self):
        self.print_header("⭐ 7. FAVORITES TESTS")
        
        # Need a profile to favorite
        resp = self._request("GET", "/api/matching/latest")
        profiles = resp['data'].get('data', [])
        
        if profiles:
            test_profile_id = profiles[0].get('id')
            
            # 7.1 Add to favorites
            resp = self._request("POST", f"/api/favorites/{test_profile_id}")
            passed = resp['status'] == 201 and resp['data'].get('success') == True
            self.print_result("7.1 Add to Favorites", passed, f"Added profile {test_profile_id}")
            
            # 7.2 Check if favorited
            resp = self._request("GET", f"/api/favorites/check/{test_profile_id}")
            passed = resp['status'] == 200 and resp['data'].get('is_favorited') == True
            self.print_result("7.2 Check Favorite Status", passed, "Profile is favorited")
            
            # 7.3 Get favorites list
            resp = self._request("GET", "/api/favorites")
            passed = resp['status'] == 200 and resp['data'].get('success') == True
            self.print_result("7.3 Get Favorites List", passed, f"Found {resp['data'].get('count', 0)} favorites")
            
            # 7.4 Remove from favorites
            resp = self._request("DELETE", f"/api/favorites/{test_profile_id}")
            passed = resp['status'] == 200 and resp['data'].get('success') == True
            self.print_result("7.4 Remove from Favorites", passed, "Profile unfavorited")
        else:
            self.print_result("7.x Favorites Tests", False, "No profiles available to favorite")
    
    # ==========================================
    # RUN ALL TESTS
    # ==========================================
    def run_all_tests(self):
        print(f"\n{Colors.YELLOW}🚀 Starting LuvIsland API Tests{Colors.RESET}")
        print(f"{Colors.BLUE}Base URL: {API_URL}{Colors.RESET}")
        
        # Check if server is running
        try:
            self._request("GET", "/")
            print(f"{Colors.GREEN}✓ Server is reachable{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Cannot connect to server at {API_URL}{Colors.RESET}")
            print(f"{Colors.YELLOW}Error: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}Please make sure your Flask server is running{Colors.RESET}")
            return
        
        self.test_authentication()
        self.test_profile_management()
        self.test_matching_system()
        self.test_likes_and_matches()
        self.test_messaging()
        self.test_search_and_discovery()
        self.test_favorites()
        
        self.print_summary()

if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1].startswith('--port='):
        pass  
    else:
        print(f"\n{Colors.CYAN}💡 Tip: You can specify port with: python test_app.py --port=5000{Colors.RESET}")
    
    tester = LuvIslandTester()
    tester.run_all_tests()