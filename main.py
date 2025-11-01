"""
DeepSeek Automation - Main entry point

This application automates login to DeepSeek chat by:
1. Handling cookie banners
2. Detecting and filling email field
3. Detecting and filling password field
4. Validating both fields are filled
5. Detecting login button location on screen
6. Clicking the login button
"""

import sys
import traceback
from datetime import datetime
from src.browser_manager import BrowserManager


def log_error(message):
    """Log error to file for debugging exe issues"""
    try:
        with open('deepseek_error.log', 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass  # Silently fail if we can't write log


def main_method():
    """Main entry point"""
    try:
        log_error("=== Application Starting ===")
        print("=" * 60)
        print("DeepSeek Chat Automation")
        print("=" * 60)
        
        manager = BrowserManager()
        success = manager.run()
        
        if not success:
            log_error("[ERROR] Failed to start application")
            print("\n[ERROR] Failed to start application")
            return 1
        
        log_error("[SUCCESS] Application closed normally")
        print("\n[SUCCESS] Application closed")
        return 0
        
    except KeyboardInterrupt:
        log_error("[INFO] Application interrupted by user")
        print("\n\n[INFO] Application interrupted by user")
        return 0
    except Exception as e:
        error_msg = f"[ERROR] Fatal error: {e}\n{traceback.format_exc()}"
        log_error(error_msg)
        print(f"\n[ERROR] Fatal error: {e}")
        return 1


if __name__ == '__main__':
    main_method()
