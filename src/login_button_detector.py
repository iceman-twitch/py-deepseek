"""
Login button detection module for finding and clicking the login button
"""
import time
import threading
import mouse
from config import (
    LOGIN_BUTTON_SEARCH_TIMEOUT,
    LOGIN_BUTTON_DETECTION_INTERVAL
)


class LoginButtonDetector:
    """Detect and click the login button on the screen"""
    
    def __init__(self, window):
        """
        Initialize the detector
        
        Args:
            window: pywebview window object
        """
        self.window = window
        self.login_button_found = False
        self.login_button_coords = None
    
    def detect_button_position(self):
        """
        Detect the login button position using XPath with fallbacks
        
        Returns:
            dict with x, y, width, height if found, None otherwise
        """
        detect_js = """
        (function() {
            try {
                console.log('=== LOGIN BUTTON DETECTION DEBUG ===');
                
                // Method 1: Direct XPath and click
                var element = document.evaluate('/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[5]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) {
                    element.click();
                    console.log('[OK] Method 1 (XPath) - Element clicked successfully');
                    return {method: 'xpath', found: true};
                }
                console.log('[FAIL] Method 1 (XPath) - Element not found');
                
                // Method 2: CSS - div.ds-button
                var btn2 = document.querySelector('div.ds-button');
                if (btn2) {
                    btn2.click();
                    console.log('[OK] Method 2 (CSS div.ds-button) - clicked');
                    return {method: 'css_selector', found: true};
                }
                console.log('[FAIL] Method 2 - not found');
                
                // Method 3: Register button class
                var btn3 = document.querySelector('.ds-sign-up-form__register-button');
                if (btn3) {
                    btn3.click();
                    console.log('[OK] Method 3 (register-button class) - clicked');
                    return {method: 'css_class', found: true};
                }
                console.log('[FAIL] Method 3 - not found');
                
                // Method 4: Search by text "Log in"
                var allElements = document.querySelectorAll('*');
                for (var i = 0; i < allElements.length; i++) {
                    var text = allElements[i].textContent.toLowerCase().trim();
                    if (text === 'log in') {
                        allElements[i].click();
                        console.log('[OK] Method 4 (exact text) - clicked');
                        return {method: 'text_exact', found: true};
                    }
                }
                console.log('[FAIL] Method 4 - not found');
                
                // Method 5: Keywords search
                for (var i = 0; i < allElements.length; i++) {
                    var text = allElements[i].textContent.toLowerCase();
                    if ((text.includes('log') || text.includes('sign') || text.includes('login')) && text.length < 50) {
                        allElements[i].click();
                        console.log('[OK] Method 5 (keyword) - clicked');
                        return {method: 'keyword', found: true};
                    }
                }
                console.log('[FAIL] Method 5 - not found');
                
                console.log('[WARN] No login button found with any method');
                return {method: 'not_found', found: false};
                
            } catch (e) {
                console.error('Error:', e.message);
                return {method: 'error', found: false, error: e.message};
            }
        })();
        """
        
        try:
            result = self.window.evaluate_js(detect_js)
            if result and result.get('found'):
                print(f"[SUCCESS] Login button found and clicked!")
                print(f"   Method: {result.get('method', 'unknown')}")
                self.login_button_found = True
                return True
            else:
                print("[ERROR] Login button not found")
                return False
        except Exception as e:
            print(f"Error detecting button: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_button_coordinates(self):
        """
        Get the calculated coordinates for the login button
        DEPRECATED: Now clicking directly in JavaScript
        
        Returns:
            True if button found and clicked, False otherwise
        """
        return self.detect_button_position()
    
    def wait_for_button(self, timeout=LOGIN_BUTTON_SEARCH_TIMEOUT):
        """
        Wait for login button to appear and click it
        DEPRECATED: Now clicking directly in JavaScript
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if found and clicked, False if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.detect_button_position():
                return True
            time.sleep(LOGIN_BUTTON_DETECTION_INTERVAL)
        
        print(f"⏱️  Timeout: Login button not found within {timeout} seconds")
        return False
    
    def click_login_button(self):
        """
        Click the login button - now using direct JavaScript click
        
        Returns:
            True if click was successful, False otherwise
        """
        return self.detect_button_position()
    
    def auto_click_after_credentials(self, credentials_callback):
        """
        Automatically click login button after credentials are entered
        
        Args:
            credentials_callback: Function that validates if credentials are entered
            
        Returns:
            True if login was successful, False otherwise
        """
        try:
            # Wait for button to appear
            button_coords = self.wait_for_button()
            if not button_coords:
                print("Could not find login button")
                return False
            
            # Validate credentials are entered
            if not credentials_callback():
                print("[ERROR] Credentials not properly entered")
                return False
            
            print("[SUCCESS] Credentials validated, attempting to click login button...")
            
            # Wait a moment before clicking
            time.sleep(0.5)
            
            # Click the button
            return self.click_login_button()
            
        except Exception as e:
            print(f"Error in auto_click_after_credentials: {e}")
            return False
