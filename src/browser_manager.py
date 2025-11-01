"""
Browser manager module for creating and managing the webview window
"""
import webview
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


class BrowserManager:
    """Manage browser window creation and lifecycle"""
    
    def __init__(self):
        """Initialize browser manager"""
        self.window = None
        self.page_handler = None
    
    def check_credentials_file(self):
        """Check if credentials file exists, create template if not"""
        credentials_manager = CredentialsManager()
        if not credentials_manager.create_template():
            print("Please set up credentials.json first")
            return False
        return True
    
    def create_window(self):
        """
        Create the webview window
        
        Returns:
            window object if successful, None otherwise
        """
        try:
            self.window = webview.create_window(
                WINDOW_TITLE,
                DEEPSEEK_URL,
                width=WINDOW_WIDTH,
                height=WINDOW_HEIGHT,
                min_size=(MIN_WIDTH, MIN_HEIGHT)
            )
            
            # Initialize page handler
            self.page_handler = PageHandler(self.window)
            
            # Register loaded event
            self.window.events.loaded += self.on_window_loaded
            
            return self.window
        except Exception as e:
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
                webview.start()
            except Exception as e:
                print(f"Error starting webview: {e}")
        else:
            print("Window not created")
    
    def run(self):
        """Run the browser manager"""
        # Check credentials
        if not self.check_credentials_file():
            return False
        
        # Create window
        if not self.create_window():
            return False
        
        # Start browser
        self.start()
        return True
