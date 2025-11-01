"""
Credentials management module
"""
import json
import os
from config import CREDENTIALS_FILE


class CredentialsManager:
    """Manage credentials loading and validation"""
    
    def __init__(self):
        self.credentials = None
        self.username = None
        self.password = None
    
    def load_credentials(self):
        """Load credentials from JSON file"""
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                self.credentials = json.load(f)
            
            self.username = self.credentials.get('username')
            self.password = self.credentials.get('password')
            
            return True
        except FileNotFoundError:
            print(f"Error: {CREDENTIALS_FILE} file not found!")
            return False
        except json.JSONDecodeError:
            print(f"Error: {CREDENTIALS_FILE} is not valid JSON!")
            return False
    
    def create_template(self):
        """Create a template credentials.json file"""
        if not os.path.exists(CREDENTIALS_FILE):
            print(f"Creating {CREDENTIALS_FILE} template...")
            with open(CREDENTIALS_FILE, 'w') as f:
                json.dump({
                    "username": "your_email@example.com",
                    "password": "your_password"
                }, f, indent=4)
            print(f"Please edit {CREDENTIALS_FILE} with your credentials and run again")
            return False
        return True
    
    def validate_credentials(self):
        """Validate that username and password are provided"""
        if not self.username or not self.password:
            print("Error: username or password is empty in credentials.json")
            return False
        return True
    
    def get_username(self):
        """Get the username"""
        return self.username
    
    def get_password(self):
        """Get the password"""
        return self.password
    
    def is_valid(self):
        """Check if credentials are valid"""
        return bool(self.username and self.password)
