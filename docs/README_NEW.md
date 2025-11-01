# DeepSeek Automation - Project Documentation

## Overview

A Python automation tool that automatically logs into DeepSeek Chat by:
1. Handling cookie banners
2. Detecting and filling email field
3. Detecting and filling password field
4. Validating credentials are entered
5. **Detecting login button location on screen** (NEW!)
6. Automatically clicking the login button

## New Features

### 🎯 Intelligent Login Button Detection
The new `LoginButtonDetector` class automatically:
- Searches for the login button on the page using multiple selectors
- Calculates exact screen coordinates based on window position
- Validates button visibility before attempting to click
- Waits for button to appear with configurable timeout
- Only clicks after credentials are validated as entered

## Project Structure

```
py-deepseek/
├── main.py                    # ⭐ New main entry point (recommended)
├── form.py                    # Legacy entry point (for backward compatibility)
├── config.py                  # Centralized configuration
├── credentials_manager.py     # Credentials loading and validation
├── keyboard_automation.py     # Keyboard input automation
├── login_button_detector.py   # NEW: Login button detection and clicking
├── browser_manager.py         # Browser window creation
├── page_handler.py            # Page event handling and flows
├── credentials.json           # User credentials (create via template)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

1. Install Python 3.9+
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create credentials file:
```bash
python main.py
```
This will create a `credentials.json` template.

4. Edit `credentials.json` with your credentials:
```json
{
    "username": "your_email@example.com",
    "password": "your_password"
}
```

## Usage

### Method 1: Using New Main Entry Point (Recommended)
```bash
python main.py
```

### Method 2: Using Legacy Entry Point
```bash
python form.py
```

## Module Documentation

### 📋 config.py
Central configuration file with all settings:
- Window dimensions and timing
- UI element selectors
- Login button search timeout
- Credentials file path

**Key Settings:**
```python
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
LOGIN_BUTTON_SEARCH_TIMEOUT = 10  # seconds
LOGIN_BUTTON_DETECTION_INTERVAL = 0.5  # seconds
```

### 🔐 credentials_manager.py
Manages credentials loading and validation.

**Main Methods:**
- `load_credentials()` - Load from credentials.json
- `validate_credentials()` - Check if username/password are valid
- `get_username()` / `get_password()` - Retrieve credentials
- `is_valid()` - Check if credentials are ready to use

### ⌨️ keyboard_automation.py
Handles keyboard input for filling forms.

**Main Methods:**
- `type_text(text, delay)` - Type text with optional delay
- `press_key(key)` - Press specific keys
- `type_email(window, email)` - Focus and type email field
- `type_password(window, password)` - Focus and type password field

### 🎯 login_button_detector.py (NEW!)
Intelligent login button detection and clicking.

**Main Methods:**
- `detect_button_position()` - Find button and get position/size
- `get_button_coordinates()` - Get calculated X,Y coordinates
- `wait_for_button(timeout)` - Wait for button to appear
- `click_login_button()` - Click the button via JavaScript
- `auto_click_after_credentials(callback)` - Auto-click after validation

**How It Works:**
1. Uses JavaScript to search for login button by multiple selectors
2. Calculates exact screen coordinates from element bounding box
3. Validates button is visible (not hidden/disabled)
4. Reports button position and size for debugging
5. Only clicks after credentials validation callback returns True

**Button Detection Strategy:**
Searches for buttons in this priority order:
```javascript
1. Button with text "Login"
2. Button with text "Sign in"
3. Button[type="submit"]
4. Button.login-button or .sign-in-button
5. Link.login-button
6. Div[role="button"] with aria-label
7. Any button element
8. Button containing "login" or "sign in" text (case-insensitive)
```

### 🌐 browser_manager.py
Creates and manages the webview window.

**Main Methods:**
- `check_credentials_file()` - Verify credentials.json exists
- `create_window()` - Create webview window
- `start()` - Start the browser
- `run()` - Run complete workflow

### 📄 page_handler.py
Handles page events and automation flows.

**Main Methods:**
- `handle_cookie_banner()` - Accept cookie consent
- `validate_credentials_entered()` - Check if form fields are filled
- `on_page_loaded()` - Handle page load event
- `enter_credentials_and_login()` - Complete login flow

**Key Features:**
- Validates form fields are filled BEFORE clicking login
- Waits for button to appear
- Handles errors gracefully with detailed logging

## Automation Flow

```
1. Window Created
   ↓
2. Page Loaded
   ├─ Cookie Banner Handled
   ├─ Credentials Loaded
   ├─ Email Typed
   ├─ Password Typed
   ├─ Credentials Validated ✓
   ├─ Login Button Detected ✓
   └─ Login Button Clicked ✓
```

## Configuration

Edit `config.py` to customize:

### Timing
```python
INITIAL_DELAY = 0.5              # Wait before starting
FIELD_FOCUS_DELAY = 0.5          # Wait after focusing field
TYPING_DELAY = 0.5               # Wait after typing
LOGIN_BUTTON_SEARCH_TIMEOUT = 10 # Max wait for button
```

### UI Selectors
Add custom selectors for your target website:
```python
LOGIN_BUTTON_SELECTORS = [
    'button:contains("Login")',
    'button.my-custom-class',
    'div[id="login-btn"]',
    # ... more selectors
]
```

## Troubleshooting

### Issue: Credentials not being filled
- Check `credentials.json` format
- Verify email/password are not empty
- Check browser console for JavaScript errors

### Issue: Login button not detected
- Inspect the login button HTML
- Add appropriate selector to `LOGIN_BUTTON_SELECTORS` in config.py
- Increase `LOGIN_BUTTON_SEARCH_TIMEOUT` if page is slow

### Issue: Login button not clicked
- Check browser console for JavaScript errors
- Verify button is visible and not disabled
- Try adding custom selector in config.py

### Debug Mode
Add verbose logging:
```python
# In page_handler.py
print(f"Debug: Button coords = {self.login_detector.get_button_coordinates()}")
```

## Development

### Adding Support for New Websites

1. Update selectors in `config.py`:
```python
EMAIL_INPUT_SELECTORS = [...]      # Add email input selectors
PASSWORD_INPUT_SELECTORS = [...]   # Add password selectors
LOGIN_BUTTON_SELECTORS = [...]     # Add login button selectors
```

2. Adjust timing if needed:
```python
FIELD_FOCUS_DELAY = 1.0  # Increase if page is slow
```

3. Test with:
```bash
python main.py
```

### Error Handling
All modules include try-except blocks with descriptive error messages. Check console output for details.

## Requirements

- Python 3.9+
- pywebview 4.2.2
- pyinstaller 5.13.0
- requests 2.31.0
- keyboard 0.13.5
- PIL/Pillow 9.5.0

See `requirements.txt` for complete list.

## Building Executable

```bash
pyinstaller -F --add-data "credentials.json:." main.py
```

## License

See LICENSE file for details.

## Support

For issues or feature requests, please check existing GitHub issues or create a new one.

---

**Last Updated:** November 1, 2025
**Version:** 2.0 (Modular Architecture with Login Button Detection)
