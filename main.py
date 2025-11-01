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

from src.browser_manager import BrowserManager


def main():
    """Main entry point"""
    print("=" * 60)
    print("DeepSeek Chat Automation")
    print("=" * 60)
    
    try:
        manager = BrowserManager()
        success = manager.run()
        
        if not success:
            print("\n❌ Failed to start application")
            return 1
        
        print("\n✅ Application closed")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Application interrupted by user")
        return 0
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
