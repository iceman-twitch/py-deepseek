"""
Keyboard automation module for typing credentials
"""
import keyboard
import time
from config import (
    INITIAL_DELAY,
    FIELD_FOCUS_DELAY,
    TYPING_DELAY
)
from .logger import log


class KeyboardAutomation:
    """Handle keyboard input automation"""

    @staticmethod
    def type_text(text, delay=0.1):
        """
        Type text using keyboard module

        Args:
            text: Text to type
            delay: Delay between characters
        """
        try:
            keyboard.write(text)
            time.sleep(TYPING_DELAY)
        except Exception as e:
            log(f"[ERROR] Error typing text: {e}")
            return False
        return True

    @staticmethod
    def press_key(key):
        """
        Press a specific key

        Args:
            key: Key to press (e.g., 'enter', 'tab', 'esc')
        """
        try:
            keyboard.press(key)
            time.sleep(0.1)
        except Exception as e:
            log(f"[ERROR] Error pressing key {key}: {e}")
            return False
        return True

    @staticmethod
    def type_email(window, email):
        """
        Focus email field and type email.

        Only types if the email field was actually focused, so credentials are
        never typed into the wrong element.
        """
        log("[KEYBOARD] Focusing email field...")
        focus_js = """
        (function focusEmailField() {
            const emailInput = document.querySelector('input[type="text"]') ||
                             document.querySelector('input[type="email"]') ||
                             document.querySelector('input[placeholder*="email"]') ||
                             document.evaluate('/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/div/input', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (emailInput) {
                emailInput.focus();
                emailInput.select();
                // Clear any existing value so nothing gets appended/duplicated.
                emailInput.value = '';
                return true;
            }
            return false;
        })();
        """

        try:
            focused = window.evaluate_js(focus_js)
            if not focused:
                log("[ERROR] Email field not found - aborting to avoid typing in the wrong place")
                return False
            time.sleep(FIELD_FOCUS_DELAY)

            log(f"[KEYBOARD] Typing email: {email}")
            return KeyboardAutomation.type_text(email)
        except Exception as e:
            log(f"[ERROR] Error typing email: {e}")
            return False

    @staticmethod
    def type_password(window, password):
        """
        Focus password field and type password.

        Verifies the password field is actually focused before typing so the
        password is never accidentally entered into the email input.
        """
        log("[KEYBOARD] Focusing password field...")
        focus_password_js = """
        (function focusPasswordField() {
            // Snapshot every input on the page for diagnostics.
            var all = document.querySelectorAll('input');
            var inputs = [];
            for (var i = 0; i < all.length; i++) {
                inputs.push({
                    type: all[i].type || '',
                    name: all[i].name || '',
                    placeholder: all[i].placeholder || '',
                    visible: !!(all[i].offsetParent)
                });
            }

            var passwordInput = document.querySelector('input[type="password"]') ||
                                document.evaluate('/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[3]/div[1]/div/input', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

            if (!passwordInput) {
                return {focused: false, reason: 'no_password_input', inputs: inputs};
            }
            if (!passwordInput.offsetParent) {
                return {focused: false, reason: 'password_input_hidden', inputs: inputs};
            }
            passwordInput.focus();
            passwordInput.select();
            // Clear any existing value so nothing gets appended/duplicated.
            passwordInput.value = '';
            var ok = document.activeElement === passwordInput;
            return {
                focused: ok,
                reason: ok ? 'ok' : 'focus_did_not_land',
                inputs: inputs
            };
        })();
        """

        try:
            result = window.evaluate_js(focus_password_js)
            focused = bool(result and result.get('focused'))
            if not focused:
                reason = result.get('reason', 'unknown') if result else 'no_result'
                log(f"[ERROR] Password field not focused (reason: {reason}) - "
                    f"skipping to avoid typing password into the email input")
                if result and result.get('inputs') is not None:
                    log(f"[DEBUG] Inputs found on page: {result.get('inputs')}")
                return False
            time.sleep(FIELD_FOCUS_DELAY)

            log("[KEYBOARD] Typing password...")
            return KeyboardAutomation.type_text(password)
        except Exception as e:
            log(f"[ERROR] Error typing password: {e}")
            return False
