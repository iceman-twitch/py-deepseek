"""
Browser manager module for creating and managing the webview window
"""
import webview
import traceback
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MIN_WIDTH,
    MIN_HEIGHT,
    DEEPSEEK_URL,
    WINDOW_TITLE
)
from .page_handler import PageHandler
from .credentials_manager import CredentialsManager


def log_error(message):
    """Log error to file for debugging"""
    try:
        from datetime import datetime
        with open('deepseek_error.log', 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass


class BrowserManager:
    """Manage browser window creation and lifecycle"""
    
    def __init__(self):
        """Initialize browser manager"""
        self.window = None
        self.page_handler = None
    
    def check_credentials_file(self):
        """Check if credentials file exists, create template if not"""
        try:
            log_error("[BrowserManager] Checking credentials file...")
            credentials_manager = CredentialsManager()
            result = credentials_manager.create_template()
            if not result:
                log_error("[BrowserManager] Credentials template check failed - please set up credentials.json")
                print("Please set up credentials.json first")
                return False
            log_error("[BrowserManager] Credentials file check passed")
            return True
        except Exception as e:
            log_error(f"[BrowserManager] Error in check_credentials_file: {e}\n{traceback.format_exc()}")
            return False
    
    def create_window(self):
        """
        Create the webview window
        
        Returns:
            window object if successful, None otherwise
        """
        try:
            log_error("[BrowserManager] Creating webview window...")
            self.window = webview.create_window(
                WINDOW_TITLE,
                DEEPSEEK_URL,
                width=WINDOW_WIDTH,
                height=WINDOW_HEIGHT,
                min_size=(MIN_WIDTH, MIN_HEIGHT)
            )
            
            log_error("[BrowserManager] Window created successfully")
            
            # Initialize page handler
            self.page_handler = PageHandler(self.window)
            
            # Register loaded event
            self.window.events.loaded += self.on_window_loaded
            
            log_error("[BrowserManager] Page handler initialized")
            return self.window
        except Exception as e:
            log_error(f"[BrowserManager] Error creating window: {e}\n{traceback.format_exc()}")
            print(f"Error creating window: {e}")
            return None
    
    def on_window_loaded(self):
        """Handle window loaded event"""
        if self.page_handler:
            self.page_handler.on_page_loaded()
    
    def start(self):
        """Start the browser"""
        if self.window:
            try:
                log_error("[BrowserManager] Starting webview...")
                webview.start()
                log_error("[BrowserManager] Webview started successfully")
            except Exception as e:
                log_error(f"[BrowserManager] Error starting webview: {e}\n{traceback.format_exc()}")
                print(f"Error starting webview: {e}")
        else:
            log_error("[BrowserManager] Cannot start - window not created")
            print("Window not created")
    
    def run(self):
        """Run the browser manager"""
        try:
            log_error("[BrowserManager] Starting run() method")
            
            # Check credentials
            log_error("[BrowserManager] Step 1: Checking credentials...")
            if not self.check_credentials_file():
                log_error("[BrowserManager] Credentials check failed, aborting")
                return False
            
            # Create window
            log_error("[BrowserManager] Step 2: Creating window...")
            if not self.create_window():
                log_error("[BrowserManager] Window creation failed, aborting")
                return False
            
            # Start browser
            log_error("[BrowserManager] Step 3: Starting browser...")
            self.start()
            
            log_error("[BrowserManager] Run completed successfully")
            return True
        except Exception as e:
            log_error(f"[BrowserManager] Exception in run(): {e}\n{traceback.format_exc()}")
            return False
