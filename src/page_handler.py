"""
Page handler module for managing page load events and automation flows
"""
import time
import threading
import mouse
from config import COOKIE_HANDLER_DELAY, COOKIE_PROCESSING_DELAY
from .credentials_manager import CredentialsManager
from .keyboard_automation import KeyboardAutomation
from .login_button_detector import LoginButtonDetector


class PageHandler:
    """Handle page load events and automation flows"""
    
    def __init__(self, window):
        """
        Initialize page handler
        
        Args:
            window: pywebview window object
        """
        self.window = window
        self.credentials_manager = CredentialsManager()
        self.keyboard_automation = KeyboardAutomation()
        self.login_detector = LoginButtonDetector(window)
        
        # Load credentials
        if not self.credentials_manager.load_credentials():
            print("Failed to load credentials")
    
    def handle_cookie_banner(self):
        """Handle cookie banner - multiple detection methods"""
        js_code = """
        (function() {
            try {
                console.log('=== COOKIE DETECTION DEBUG ===');
                
                // Method 1: Direct XPath and click
                var element = document.evaluate('/html/body/div[1]/div/div[2]/div[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) {
                    element.click();
                    console.log('✅ Method 1 (XPath) - Element clicked successfully');
                    return {method: 'xpath', found: true};
                }
                console.log('❌ Method 1 (XPath) - Element not found');
                
                // Method 2: CSS Selector - div.ds-button
                var elem2 = document.querySelector('div.ds-button');
                if (elem2) {
                    elem2.click();
                    console.log('✅ Method 2 (CSS div.ds-button) - clicked');
                    return {method: 'css_selector', found: true};
                }
                console.log('❌ Method 2 - not found');
                
                // Method 3: Cookie banner class
                var elem3 = document.querySelector('.cookie_banner-accept-essential-button');
                if (elem3) {
                    elem3.click();
                    console.log('✅ Method 3 (cookie_banner class) - clicked');
                    return {method: 'css_class', found: true};
                }
                console.log('❌ Method 3 - not found');
                
                // Method 4: Button with "necessary" text
                var buttons = document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {
                    var text = buttons[i].textContent.toLowerCase();
                    if (text.includes('necessary') || text.includes('only')) {
                        buttons[i].click();
                        console.log('✅ Method 4 (button text) - clicked');
                        return {method: 'button_text', found: true};
                    }
                }
                console.log('❌ Method 4 - no button with necessary text');
                
                // Method 5: Any DIV with "necessary" text
                var allDivs = document.querySelectorAll('div');
                for (var i = 0; i < allDivs.length; i++) {
                    var text = allDivs[i].textContent.toLowerCase();
                    if (text.includes('necessary') && text.length < 100) {
                        allDivs[i].click();
                        console.log('✅ Method 5 (div text) - clicked');
                        return {method: 'div_text', found: true};
                    }
                }
                console.log('❌ Method 5 - no div with necessary text');
                
                console.log('⚠️ No cookie banner found with any method');
                return {method: 'not_found', found: false};
                
            } catch (e) {
                console.error('Error:', e.message);
                return {method: 'error', found: false, error: e.message};
            }
        })();
        """
        
        try:
            print("🍪 Detecting cookie banner (trying all methods)...")
            result = self.window.evaluate_js(js_code)
            
            if result and result.get('found'):
                print(f"✅ Cookie banner clicked!")
                print(f"   Method: {result.get('method', 'unknown')}")
                time.sleep(COOKIE_PROCESSING_DELAY)
                time.sleep(1.0)
                return True
            else:
                print("⚠️  Cookie banner not found with any method")
                return True  # Continue anyway
                
        except Exception as e:
            print(f"⚠️  Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def validate_credentials_entered(self):
        """
        Validate that credentials have been entered in the form fields
        
        Returns:
            True if both email and password fields have content, False otherwise
        """
        check_js = """
        function validateCredentialsEntered() {
            const emailInputs = [
                document.querySelector('input[type="text"]'),
                document.querySelector('input[type="email"]'),
                document.querySelector('input[placeholder*="email"]')
            ];
            
            const passwordInputs = [
                document.querySelector('input[type="password"]')
            ];
            
            let emailHasValue = false;
            let passwordHasValue = false;
            
            for (let input of emailInputs) {
                if (input && input.value && input.value.trim().length > 0) {
                    emailHasValue = true;
                    break;
                }
            }
            
            for (let input of passwordInputs) {
                if (input && input.value && input.value.trim().length > 0) {
                    passwordHasValue = true;
                    break;
                }
            }
            
            return {
                emailFilled: emailHasValue,
                passwordFilled: passwordHasValue,
                bothFilled: emailHasValue && passwordHasValue
            };
        }
        return validateCredentialsEntered();
        """
        
        try:
            result = self.window.evaluate_js(check_js)
            if result:
                print(f"📝 Email field filled: {result.get('emailFilled', False)}")
                print(f"📝 Password field filled: {result.get('passwordFilled', False)}")
                return result.get('bothFilled', False)
            return False
        except Exception as e:
            print(f"Error validating credentials: {e}")
            return False
    
    def on_page_loaded(self):
        """Handle page loaded event"""
        time.sleep(COOKIE_HANDLER_DELAY)
        
        # Handle cookie banner
        self.handle_cookie_banner()
        
        # Start credential entry in a separate thread
        if self.credentials_manager.is_valid():
            print("🔐 Starting credential entry automation...")
            threading.Thread(
                target=self.enter_credentials_and_login,
                daemon=True
            ).start()
        else:
            print("❌ Credentials are not valid")
    
    def enter_credentials_and_login(self):
        """Enter credentials and attempt to login"""
        try:
            # Get credentials
            email = self.credentials_manager.get_username()
            password = self.credentials_manager.get_password()
            
            if not email or not password:
                print("❌ Missing email or password")
                return
            
            # Type email
            success = self.keyboard_automation.type_email(self.window, email)
            if not success:
                print("❌ Failed to enter email")
                return
            
            print("✅ Email entered")
            time.sleep(0.5)
            
            # Type password
            success = self.keyboard_automation.type_password(self.window, password)
            if not success:
                print("❌ Failed to enter password")
                return
            
            print("✅ Password entered")
            
            # Wait 1 second after typing password (async wait, no validation check)
            print("⏳ Waiting 1 second for form to process...")
            time.sleep(1.0)
            
            print("✅ All credentials entered successfully!")
            print("👉 Attempting to locate and click login button...")
            
            # Try to auto-click login button (no validation, just click)
            self.login_detector.auto_click_after_credentials(
                lambda: True  # Always return True, skip validation check
            )
            
        except Exception as e:
            print(f"Error during credential entry and login: {e}")
