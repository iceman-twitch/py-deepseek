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
            print(f"Error typing text: {e}")
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
            print(f"Error pressing key {key}: {e}")
            return False
        return True
    
    @staticmethod
    def type_email(window, email):
        """
        Focus email field and type email
        
        Args:
            window: pywebview window object
            email: Email address to type
        """
        print("Focusing email field...")
        focus_js = """
        function focusEmailField() {
            const emailInput = document.querySelector('input[type="text"]') || 
                             document.querySelector('input[type="email"]') ||
                             document.querySelector('input[placeholder*="email"]') ||
                             document.evaluate('/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/div/input', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (emailInput) {
                emailInput.focus();
                emailInput.select();
                return true;
            }
            return false;
        }
        focusEmailField();
        """
        
        try:
            window.evaluate_js(focus_js)
            time.sleep(FIELD_FOCUS_DELAY)
            
            print(f"Typing email: {email}")
            KeyboardAutomation.type_text(email)
            return True
        except Exception as e:
            print(f"Error typing email: {e}")
            return False
    
    @staticmethod
    def type_password(window, password):
        """
        Focus password field and type password
        
        Args:
            window: pywebview window object
            password: Password to type
        """
        print("Focusing password field...")
        focus_password_js = """
        function focusPasswordField() {
            const passwordInput = document.querySelector('input[type="password"]') ||
                                document.evaluate('/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[3]/div[1]/div/input', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (passwordInput) {
                passwordInput.focus();
                passwordInput.select();
                return true;
            }
            return false;
        }
        focusPasswordField();
        """
        
        try:
            window.evaluate_js(focus_password_js)
            time.sleep(FIELD_FOCUS_DELAY)
            
            print("Typing password...")
            KeyboardAutomation.type_text(password)
            return True
        except Exception as e:
            print(f"Error typing password: {e}")
            return False
