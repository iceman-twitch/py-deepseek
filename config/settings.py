"""
Configuration settings for the DeepSeek application
"""
import os

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Window configuration
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
MIN_WIDTH = 800
MIN_HEIGHT = 600

# Timing configuration (in seconds)
INITIAL_DELAY = 0.5
FIELD_FOCUS_DELAY = 0.5
TYPING_DELAY = 0.5
COOKIE_HANDLER_DELAY = 1
COOKIE_PROCESSING_DELAY = 2

# URL configuration
DEEPSEEK_URL = 'https://chat.deepseek.com'
WINDOW_TITLE = 'DeepSeek Chat - Automation'

# Credentials file (in project root, not in config folder)
CREDENTIALS_FILE = os.path.join(PROJECT_ROOT, 'credentials.json')

# Login button detection
LOGIN_BUTTON_SEARCH_TIMEOUT = 10  # seconds to wait for login button
LOGIN_BUTTON_DETECTION_INTERVAL = 0.5  # how often to check for button in seconds

# UI Elements selectors
EMAIL_INPUT_SELECTORS = [
    'input[type="text"]',
    'input[type="email"]',
    'input[placeholder*="email"]',
    '/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/div/input'
]

PASSWORD_INPUT_SELECTORS = [
    'input[type="password"]',
    '/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[3]/div[1]/div/input'
]

LOGIN_BUTTON_SELECTORS = [
    'button:contains("Log in")',
    'button[type="submit"]',
    'button.login-button',
    'a.login-button',
    'div[role="button"][aria-label*="Login"]',
    '/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[5]'
]

COOKIE_BANNER_SELECTORS = [
    'div.cookie_banner-accept-essential-button',
    'button.cookie-accept',
    'button[aria-label*="Accept"]',
    '/html/body/div[1]/div/div[2]/div[3]'
]
