#!/usr/bin/env python
"""
Debug script to test button detection and clicking without full automation
Run this to see what's on the page and if XPaths can find elements.
"""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.browser_manager import BrowserManager

def test_detection():
    """Test button detection"""
    print("=" * 60)
    print("BUTTON DETECTION DEBUG TEST")
    print("=" * 60)
    print("\nStarting browser...")
    
    browser = BrowserManager()
    
    # Create window but don't start full automation
    browser.create_window()
    
    # Note: window.evaluate_js only works after window is started in webview
    print("\n⚠️  This test runs within the webview context.")
    print("The debug output will appear in the console and in page_handler logs.")
    print("\nStarting webview in 3 seconds...")
    time.sleep(3)
    
    try:
        browser.start()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_detection()

