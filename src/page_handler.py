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
from .logger import log


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

        # Guard so credentials are only entered once. The webview 'loaded'
        # event fires on every navigation/reload, and without this guard each
        # fire spawns another typing thread, causing doubled/duplicated input.
        self._automation_started = False
        self._automation_lock = threading.Lock()
        
        # Load credentials
        if not self.credentials_manager.load_credentials():
            print("Failed to load credentials")
    
    def handle_cookie_banner(self):
        """Handle cookie banner - multiple detection methods"""
        js_code = """
        (function() {
            try {
                // Phrases (lowercase) that identify the "only necessary cookies"
                // / terms-accept button. Hungarian variants included first so the
                // correct button ("csak szükséges sütik") wins over generic ones.
                var phrases = [
                    'csak szükséges sütik',
                    'csak a szükséges',
                    'csak szükséges',
                    'szükséges sütik',
                    'csak az elengedhetetlen',
                    'only necessary',
                    'necessary only',
                    'accept necessary',
                    'accept only necessary',
                    'reject all',
                    'accept essential'
                ];

                // Collect every clickable-ish element and its trimmed text.
                var candidates = document.querySelectorAll(
                    'button, div, span, a, [role="button"]'
                );

                // Pass 1: exact/priority text match on the clickable itself.
                for (var p = 0; p < phrases.length; p++) {
                    for (var i = 0; i < candidates.length; i++) {
                        var el = candidates[i];
                        var text = (el.textContent || '').trim().toLowerCase();
                        // Keep it short so we match the button, not a whole banner.
                        if (text.length > 0 && text.length < 60 &&
                            text.indexOf(phrases[p]) !== -1) {
                            el.click();
                            return {
                                found: true,
                                method: 'text_match',
                                phrase: phrases[p],
                                text: (el.textContent || '').trim()
                            };
                        }
                    }
                }

                // Pass 2: known essential-cookie CSS class.
                var essential = document.querySelector('.cookie_banner-accept-essential-button');
                if (essential) {
                    essential.click();
                    return {found: true, method: 'css_essential', text: (essential.textContent || '').trim()};
                }

                // Not found - gather the visible button texts for diagnostics.
                var texts = [];
                for (var j = 0; j < candidates.length; j++) {
                    var t = (candidates[j].textContent || '').trim();
                    if (t.length > 0 && t.length < 60) texts.push(t);
                }
                // Deduplicate and cap the list.
                var seen = {}, uniq = [];
                for (var k = 0; k < texts.length && uniq.length < 25; k++) {
                    if (!seen[texts[k]]) { seen[texts[k]] = 1; uniq.push(texts[k]); }
                }
                return {found: false, method: 'not_found', buttonTexts: uniq};

            } catch (e) {
                return {method: 'error', found: false, error: e.message};
            }
        })();
        """
        
        try:
            try:
                current_url = self.window.get_current_url()
            except Exception:
                current_url = 'unknown'
            log(f"[SITE] Fetched page: {current_url}")
            log("[COOKIE] Detecting cookie/terms accept banner (trying all methods)...")
            result = self.window.evaluate_js(js_code)

            if result and result.get('found'):
                log("[COOKIE] Cookie/terms accept banner clicked!")
                log(f"[COOKIE] Method used: {result.get('method', 'unknown')}")
                if result.get('text'):
                    log(f"[COOKIE] Button text: \"{result.get('text')}\"")
                if result.get('phrase'):
                    log(f"[COOKIE] Matched phrase: \"{result.get('phrase')}\"")
                time.sleep(COOKIE_PROCESSING_DELAY)
                time.sleep(1.0)
                return True
            else:
                log("[COOKIE] Cookie banner not found with any method (continuing anyway)")
                if result and result.get('error'):
                    log(f"[COOKIE] JS error: {result.get('error')}")
                if result and result.get('buttonTexts'):
                    log(f"[COOKIE] Clickable texts seen on page: {result.get('buttonTexts')}")
                return True  # Continue anyway

        except Exception as e:
            log(f"[ERROR] Cookie banner handling error: {e}")
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
            log(f"[ERROR] Error validating credentials: {e}")
            return False
    
    def on_page_loaded(self):
        """Handle page loaded event"""
        # Only run the automation once, even if 'loaded' fires multiple times.
        with self._automation_lock:
            if self._automation_started:
                log("[INFO] Automation already ran, skipping duplicate page-load event")
                return
            self._automation_started = True

        time.sleep(COOKIE_HANDLER_DELAY)
        
        # Handle cookie banner
        self.handle_cookie_banner()
        
        # Start credential entry in a separate thread
        if self.credentials_manager.is_valid():
            log("[AUTH] Starting credential entry automation...")
            threading.Thread(
                target=self.enter_credentials_and_login,
                daemon=True
            ).start()
        else:
            log("[ERROR] Credentials are not valid")
    
    def enter_credentials_and_login(self):
        """Enter credentials and attempt to login"""
        try:
            # Get credentials
            email = self.credentials_manager.get_username()
            password = self.credentials_manager.get_password()
            
            if not email or not password:
                log("[ERROR] Missing email or password")
                return

            # Type email
            success = self.keyboard_automation.type_email(self.window, email)
            if not success:
                log("[ERROR] Failed to enter email")
                return

            log("[SUCCESS] Email entered")
            # Give the form a moment before moving to the password field.
            time.sleep(0.5)

            # Type password. type_password() verifies the password field is
            # actually focused before typing, so the password can never end up
            # in the email input.
            success = self.keyboard_automation.type_password(self.window, password)
            if not success:
                log("[ERROR] Failed to enter password (password field not focused) - aborting")
                return

            log("[SUCCESS] Password entered")

            # Wait 1 second after typing password (async wait, no validation check)
            log("[INFO] Waiting 1 second for form to process...")
            time.sleep(1.0)

            log("[SUCCESS] All credentials entered successfully!")
            log("[INFO] Attempting to locate and click login button...")
            
            # Try to auto-click login button (no validation, just click)
            self.login_detector.auto_click_after_credentials(
                lambda: True  # Always return True, skip validation check
            )
            
        except Exception as e:
            log(f"[ERROR] Error during credential entry and login: {e}")
