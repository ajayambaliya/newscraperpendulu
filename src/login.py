"""
Authentication module for pendulumedu.com
Handles login and session management
"""

import os
import json
import requests
from typing import Optional, Dict
from pathlib import Path


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass


class LoginManager:
    """Manages authentication with pendulumedu.com with online session storage"""
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None, 
                 session_file: str = "data/session.json", use_online: bool = True):
        """
        Initialize LoginManager with credentials
        
        Args:
            email: Login email (defaults to LOGIN_EMAIL env var)
            password: Login password (defaults to LOGIN_PASSWORD env var)
            session_file: Path to store session cookies locally
            use_online: Whether to use online storage (GitHub Gist) for session
        """
        self.email = email or os.environ.get('LOGIN_EMAIL')
        self.password = password or os.environ.get('LOGIN_PASSWORD')
        
        if not self.email or not self.password:
            raise AuthenticationError(
                "Credentials not provided. Set LOGIN_EMAIL and LOGIN_PASSWORD environment variables."
            )
        
        self.login_url = "https://pendulumedu.com/login"
        self.session_file = session_file
        self.session: Optional[requests.Session] = None
        self.use_online = use_online
        
        # GitHub Gist configuration for online session storage
        self.gist_token = os.getenv('GIST_TOKEN')
        self.session_gist_id = os.getenv('SESSION_GIST_ID')
        
        # If online storage is enabled but not configured, fall back to local
        if self.use_online and (not self.gist_token or not self.session_gist_id):
            print("Info: Online session storage not configured. Using local storage only.")
            self.use_online = False
    
    def _load_session_from_gist(self) -> Optional[Dict[str, str]]:
        """
        Load session cookies from GitHub Gist.
        
        Returns:
            Dictionary of cookies or None if failed
        """
        if not self.use_online:
            return None
        
        try:
            headers = {
                'Authorization': f'token {self.gist_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(
                f'https://api.github.com/gists/{self.session_gist_id}',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                gist_data = response.json()
                files = gist_data.get('files', {})
                if files:
                    file_content = list(files.values())[0]['content']
                    cookies = json.loads(file_content)
                    print("Loaded session from online storage")
                    return cookies
            else:
                print(f"Info: Could not load session from Gist (status {response.status_code})")
                return None
        except Exception as e:
            print(f"Info: Could not load session from online storage: {e}")
            return None
    
    def _save_session_to_gist(self, cookies: Dict[str, str]) -> bool:
        """
        Save session cookies to GitHub Gist.
        
        Args:
            cookies: Dictionary of cookies to save
            
        Returns:
            True if successful, False otherwise
        """
        if not self.use_online:
            return False
        
        try:
            headers = {
                'Authorization': f'token {self.gist_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            content = json.dumps(cookies, indent=2)
            
            payload = {
                'files': {
                    'session.json': {
                        'content': content
                    }
                }
            }
            
            response = requests.patch(
                f'https://api.github.com/gists/{self.session_gist_id}',
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print("Session saved to online storage")
                return True
            else:
                print(f"Info: Could not save session to Gist (status {response.status_code})")
                return False
        except Exception as e:
            print(f"Info: Could not save session to online storage: {e}")
            return False
    
    def _save_session(self) -> None:
        """
        Save session cookies to both local file and online storage
        """
        if not self.session:
            return
        
        # Extract important cookies
        cookies = {}
        for cookie in self.session.cookies:
            if cookie.name in ['PHPSESSID', 'pendulum_session']:
                cookies[cookie.name] = cookie.value
        
        if not cookies:
            return
        
        # Save to local file
        session_path = Path(self.session_file)
        session_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save local session file: {e}")
        
        # Save to online storage if enabled
        if self.use_online:
            self._save_session_to_gist(cookies)
    
    def _load_session(self) -> Optional[Dict[str, str]]:
        """
        Load session cookies from online storage or local file
        
        Returns:
            Dictionary of cookies or None if not found
        """
        # Try online storage first
        if self.use_online:
            online_cookies = self._load_session_from_gist()
            if online_cookies:
                # Also save to local file as backup
                try:
                    session_path = Path(self.session_file)
                    session_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(self.session_file, 'w', encoding='utf-8') as f:
                        json.dump(online_cookies, f, indent=2)
                except IOError:
                    pass
                return online_cookies
        
        # Fall back to local file
        session_path = Path(self.session_file)
        
        if not session_path.exists():
            return None
        
        try:
            with open(self.session_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                return cookies if cookies else None
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load local session file: {e}")
            return None
    
    def _validate_session(self, session: requests.Session) -> bool:
        """
        Validate if the session is still active by making a test request
        
        Args:
            session: Session to validate
            
        Returns:
            True if session is valid, False otherwise
        """
        try:
            # Try to access a protected page to verify session
            test_url = "https://pendulumedu.com/quiz/current-affairs"
            response = session.get(test_url, timeout=10, allow_redirects=False)
            
            # If we're redirected to login, session is invalid
            if response.status_code == 302 and 'login' in response.headers.get('Location', '').lower():
                return False
            
            # If we get a successful response, session is valid
            if response.status_code == 200:
                return True
            
            return False
        except Exception:
            return False
    
    def get_session(self) -> requests.Session:
        """
        Get authenticated session, using stored cookies if available
        
        Returns:
            requests.Session: Authenticated session object
            
        Raises:
            AuthenticationError: If login fails
        """
        # Try to restore session from stored cookies
        stored_cookies = self._load_session()
        
        if stored_cookies:
            # Create session with stored cookies
            self.session = requests.Session()
            for name, value in stored_cookies.items():
                self.session.cookies.set(name, value, domain='pendulumedu.com')
            
            # Validate the session
            if self._validate_session(self.session):
                print("Using stored session cookies")
                return self.session
            else:
                print("Stored session expired, logging in again")
        
        # If no stored session or validation failed, perform fresh login
        return self.login()
    
    def login(self) -> requests.Session:
        """
        Authenticate with pendulumedu.com and return session with cookies
        
        Returns:
            requests.Session: Authenticated session object
            
        Raises:
            AuthenticationError: If login fails
        """
        try:
            # Create new session
            self.session = requests.Session()
            
            # Prepare login payload (matching the form fields)
            payload = {
                'emailId': self.email,
                'password': self.password,
                'submit': 'Sign in'
            }
            
            # First, get the login page to establish session
            login_page = self.session.get(self.login_url, timeout=30)
            
            # Set headers to mimic browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': self.login_url,
                'Origin': 'https://pendulumedu.com'
            }
            
            # Perform login request
            response = self.session.post(
                self.login_url,
                data=payload,
                headers=headers,
                timeout=30,
                allow_redirects=True
            )
            
            # Check if login was successful
            if response.status_code != 200:
                raise AuthenticationError(
                    f"Login failed with status code: {response.status_code}"
                )
            
            # Verify authentication by checking for session cookies
            if not self.session.cookies:
                raise AuthenticationError(
                    "Login failed: No session cookies received"
                )
            
            # Additional validation: check if we're redirected to dashboard or logged in page
            # Most sites redirect to a different page after successful login
            if 'login' in response.url.lower() and 'error' in response.text.lower():
                raise AuthenticationError(
                    "Login failed: Invalid credentials or authentication error"
                )
            
            # Save session cookies for future use
            self._save_session()
            print("Login successful, session cookies saved")
            
            return self.session
            
        except requests.exceptions.Timeout:
            raise AuthenticationError("Login request timed out")
        except requests.exceptions.ConnectionError:
            raise AuthenticationError("Failed to connect to pendulumedu.com")
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Login request failed: {str(e)}")
        except Exception as e:
            raise AuthenticationError(f"Unexpected error during login: {str(e)}")
