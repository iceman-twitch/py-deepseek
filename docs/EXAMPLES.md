# Usage Examples & Best Practices

## Basic Usage

### Example 1: Simple Login Automation
```bash
# Setup (first time only)
python main.py
# Edit credentials.json with your email/password

# Run
python main.py
```

### Example 2: Using Legacy Entry Point
```bash
python form.py
```

---

## Configuration Examples

### Example 1: Speed Up for Fast Websites
**Scenario**: Website loads quickly, buttons appear immediately

Edit `config.py`:
```python
# Reduce delays for faster response
INITIAL_DELAY = 0.2
FIELD_FOCUS_DELAY = 0.2
TYPING_DELAY = 0.2
COOKIE_PROCESSING_DELAY = 0.5
LOGIN_BUTTON_SEARCH_TIMEOUT = 5  # Shorter timeout
LOGIN_BUTTON_DETECTION_INTERVAL = 0.2  # Check more frequently
```

### Example 2: Slow Down for Complex Websites
**Scenario**: Website needs time to render, buttons appear late

Edit `config.py`:
```python
# Increase delays for complex pages
INITIAL_DELAY = 2.0
FIELD_FOCUS_DELAY = 1.0
TYPING_DELAY = 1.0
COOKIE_PROCESSING_DELAY = 3.0
LOGIN_BUTTON_SEARCH_TIMEOUT = 20  # Longer timeout
LOGIN_BUTTON_DETECTION_INTERVAL = 1.0  # Check less frequently
```

### Example 3: Custom Button Selectors
**Scenario**: Website has custom login button styling

Edit `config.py`:
```python
LOGIN_BUTTON_SELECTORS = [
    # Add your custom selectors first
    'button#my-login-btn',
    'div.custom-button[data-action="login"]',
    'a.btn-primary.login',
    
    # Keep defaults as fallback
    'button:contains("Login")',
    'button:contains("Sign in")',
    'button[type="submit"]',
]
```

---

## Credential Management Examples

### Example 1: Using Environment Variables (Secure)
**Scenario**: Don't want credentials in file

Modify `credentials_manager.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

def load_credentials(self):
    """Load from environment variables"""
    self.username = os.getenv('DEEPSEEK_EMAIL')
    self.password = os.getenv('DEEPSEEK_PASSWORD')
    
    if not self.username or not self.password:
        print("Error: Set DEEPSEEK_EMAIL and DEEPSEEK_PASSWORD env vars")
        return False
    return True
```

### Example 2: Multiple Accounts
**Scenario**: Automate login for multiple user accounts

Create `multi_account.py`:
```python
import json
from browser_manager import BrowserManager
import time

def login_multiple_accounts(accounts_file):
    """Login to multiple accounts sequentially"""
    with open(accounts_file) as f:
        accounts = json.load(f)
    
    for account in accounts:
        # Update credentials
        with open('credentials.json', 'w') as f:
            json.dump(account, f)
        
        # Run automation
        manager = BrowserManager()
        manager.run()
        
        # Wait between accounts
        time.sleep(30)

if __name__ == '__main__':
    login_multiple_accounts('accounts.json')
```

With `accounts.json`:
```json
[
    {"username": "user1@example.com", "password": "pass1"},
    {"username": "user2@example.com", "password": "pass2"}
]
```

---

## Advanced Customization Examples

### Example 1: Add 2FA/MFA Handling
**Scenario**: Website requires two-factor authentication

Modify `page_handler.py`:
```python
def enter_credentials_and_login(self):
    """Extended flow with 2FA"""
    # Existing steps...
    
    # NEW: Handle 2FA
    print("🔐 Waiting for 2FA code...")
    mfa_code = input("Enter 2FA code: ")
    
    # Type 2FA code
    keyboard.write(mfa_code)
    time.sleep(0.5)
    
    # Continue with login button click
    self.login_detector.auto_click_after_credentials(...)
```

### Example 2: Add Logging to File
**Scenario**: Keep detailed logs of automation

Create `logger_config.py`:
```python
import logging
from datetime import datetime

def setup_logging():
    """Setup file logging"""
    log_file = f"logs/automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()
```

Then use in `page_handler.py`:
```python
from logger_config import logger

class PageHandler:
    def on_page_loaded(self):
        logger.info("Page loaded, starting automation")
        # ...
```

### Example 3: Add Screenshot on Error
**Scenario**: Debug failed logins with screenshots

Modify `browser_manager.py`:
```python
def screenshot_on_error(self):
    """Take screenshot before attempting login"""
    if self.window:
        try:
            screenshot_data = self.window.get_elements('*')[0]
            # Save screenshot
            filename = f"screenshots/error_{time.time()}.png"
            print(f"Screenshot saved to {filename}")
        except Exception as e:
            print(f"Could not take screenshot: {e}")
```

---

## Testing Examples

### Example 1: Unit Test - Credentials Manager
```python
# test_credentials_manager.py
import unittest
from credentials_manager import CredentialsManager

class TestCredentialsManager(unittest.TestCase):
    def test_validate_empty_credentials(self):
        manager = CredentialsManager()
        manager.username = None
        manager.password = None
        self.assertFalse(manager.is_valid())
    
    def test_validate_valid_credentials(self):
        manager = CredentialsManager()
        manager.username = "test@example.com"
        manager.password = "password123"
        self.assertTrue(manager.is_valid())

if __name__ == '__main__':
    unittest.main()
```

### Example 2: Integration Test - Full Flow
```python
# test_integration.py
import time
from browser_manager import BrowserManager

def test_full_login_flow():
    """Test complete automation flow"""
    manager = BrowserManager()
    
    # Override credentials for testing
    manager.page_handler.credentials_manager.username = "test@example.com"
    manager.page_handler.credentials_manager.password = "testpass123"
    
    # Run
    success = manager.run()
    
    # Verify
    assert success, "Login flow failed"
    print("✅ Full login flow test passed")

if __name__ == '__main__':
    test_full_login_flow()
```

---

## Debugging Examples

### Example 1: Enable Debug Logging
```python
# In page_handler.py
def enter_credentials_and_login(self):
    # Add debug output
    print(f"DEBUG: Starting credential entry")
    print(f"DEBUG: Email: {self.credentials_manager.get_username()}")
    
    # Type email
    success = self.keyboard_automation.type_email(...)
    print(f"DEBUG: Email typing success: {success}")
    
    # Type password
    success = self.keyboard_automation.type_password(...)
    print(f"DEBUG: Password typing success: {success}")
    
    # Validate
    validated = self.validate_credentials_entered()
    print(f"DEBUG: Credentials validated: {validated}")
    
    # Click button
    success = self.login_detector.click_login_button()
    print(f"DEBUG: Login button click success: {success}")
```

### Example 2: Check Button Position Manually
```python
# In Python console
from page_handler import PageHandler
from browser_manager import BrowserManager

manager = BrowserManager()
manager.run()

# After page loads
coords = manager.page_handler.login_detector.get_button_coordinates()
print(f"Button at: {coords}")
```

### Example 3: Test JavaScript Selectors
```python
# In browser console (F12)
// Test email selector
document.querySelector('input[type="email"]')

// Test password selector
document.querySelector('input[type="password"]')

// Test login button selector
document.querySelector('button:contains("Login")')

// If not found, try alternatives
Array.from(document.querySelectorAll('button'))
    .find(btn => btn.textContent.includes('Login'))
```

---

## Performance Optimization Examples

### Example 1: Cache Button Coordinates
**Scenario**: Don't re-detect button if page hasn't changed

Modify `login_button_detector.py`:
```python
class LoginButtonDetector:
    def __init__(self, window):
        self.window = window
        self.cached_coordinates = None
        self.cache_valid = False
    
    def get_button_coordinates(self, use_cache=True):
        if use_cache and self.cache_valid:
            print("Using cached coordinates")
            return self.cached_coordinates
        
        # Fresh detection
        coords = self.detect_button_position()
        if coords:
            self.cached_coordinates = coords
            self.cache_valid = True
        return coords
    
    def invalidate_cache(self):
        self.cache_valid = False
```

### Example 2: Parallel Button Detection
**Scenario**: Search for button while typing credentials

Modify `page_handler.py`:
```python
def enter_credentials_and_login(self):
    # Start button detection in background
    button_thread = threading.Thread(
        target=self.login_detector.wait_for_button,
        daemon=True
    )
    button_thread.start()
    
    # Type credentials in parallel
    self.keyboard_automation.type_email(...)
    self.keyboard_automation.type_password(...)
    
    # Wait for button detection to complete
    button_thread.join()
    
    # Click button
    self.login_detector.click_login_button()
```

---

## Troubleshooting Examples

### Example 1: Button Not Found - Add Custom Selector
```python
# Step 1: Open browser dev tools (F12)
# Step 2: Inspect login button element
# Step 3: Copy the selector

# Step 4: Add to config.py
LOGIN_BUTTON_SELECTORS = [
    'button#custom-login',      # Your custom selector
    'button:contains("Login")',
    # ... rest of defaults
]

# Step 5: Test
python main.py
```

### Example 2: Credentials Not Entered
```python
# In browser console (F12):
// Check email field
document.querySelector('input[type="email"]').value

// Check password field  
document.querySelector('input[type="password"]').value

// If empty, the selectors might be wrong
// Update in config.py:
EMAIL_INPUT_SELECTORS = [
    'input.email-field',  # Custom selector
    'input[type="email"]',
]
```

### Example 3: Timeout Issues
```python
# In config.py, increase timeouts:
LOGIN_BUTTON_SEARCH_TIMEOUT = 30  # Wait up to 30 seconds
INITIAL_DELAY = 2.0               # Wait 2 seconds at start

# Test with:
python main.py
```

---

## Best Practices

### ✅ DO
- ✅ Store credentials securely (use environment variables in production)
- ✅ Test custom selectors in browser console first
- ✅ Log important events for debugging
- ✅ Handle errors gracefully
- ✅ Use appropriate timeouts for target website
- ✅ Validate before taking action
- ✅ Keep code modular and maintainable

### ❌ DON'T
- ❌ Don't hardcode credentials in code
- ❌ Don't store credentials in version control
- ❌ Don't use extremely short timeouts
- ❌ Don't execute user-provided selectors
- ❌ Don't skip validation steps
- ❌ Don't modify page HTML/CSS
- ❌ Don't ignore error messages

---

## File Organization Best Practices

### Directory Structure
```
py-deepseek/
├── src/                    # Source code
│   ├── __init__.py
│   ├── config.py
│   ├── credentials_manager.py
│   ├── keyboard_automation.py
│   ├── login_button_detector.py
│   ├── browser_manager.py
│   └── page_handler.py
├── tests/                  # Test files
│   ├── test_credentials_manager.py
│   ├── test_keyboard_automation.py
│   └── test_integration.py
├── logs/                   # Log files (auto-created)
├── screenshots/            # Screenshots (auto-created)
├── main.py                 # Entry point
├── credentials.json        # User credentials (don't commit)
├── requirements.txt
└── README.md
```

---

## Common Modifications

### Modification 1: Change Target Website
```python
# In config.py
DEEPSEEK_URL = 'https://your-target-website.com'
WINDOW_TITLE = 'Your App Name'

# Adjust selectors
EMAIL_INPUT_SELECTORS = ['input.email']
PASSWORD_INPUT_SELECTORS = ['input.password']
LOGIN_BUTTON_SELECTORS = ['button.submit']
```

### Modification 2: Add Pre-login Actions
```python
# In page_handler.py
def enter_credentials_and_login(self):
    # Pre-login action
    self.handle_cookies()
    self.close_popups()
    self.accept_terms()
    
    # Continue with login
    self.keyboard_automation.type_email(...)
    # ...
```

### Modification 3: Add Post-login Actions
```python
# In page_handler.py
def enter_credentials_and_login(self):
    # ... existing code ...
    
    # Click login
    self.login_detector.click_login_button()
    
    # Post-login actions
    time.sleep(2)
    self.navigate_to_dashboard()
    self.configure_profile()
    self.save_session()
```

---

**Examples Version**: 1.0  
**Last Updated**: November 1, 2025
