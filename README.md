# py-deepseek

Automated login tool for DeepSeek Chat with intelligent button detection and multi-method fallback strategies.

## Features

- 🔐 **Automatic Login** - Automatically fills credentials and submits the login form
- 🍪 **Cookie Banner Handler** - Detects and clicks "necessary cookies only" button
- 🎯 **Smart Detection** - 5 different detection methods for each button (XPath, CSS selectors, text search, etc.)
- 🔄 **Automatic Fallback** - If one detection method fails, automatically tries the next
- 🖱️ **Direct JavaScript Clicks** - Reliable clicking without mouse automation complications
- 📊 **Detailed Logging** - See exactly which detection method succeeded

## Quick Start

### 1. Setup Credentials

Create or edit `credentials.json` in the project root:

```json
{
    "email": "your-email@example.com",
    "password": "your-password"
}
```

### 2. Run the Application

```bash
run.bat
```

That's it! The automation will:
1. Open DeepSeek Chat in a browser window
2. Detect and click the cookie banner (if present)
3. Fill in your email and password
4. Detect and click the login button
5. Submit the form

## Detection Methods

### Cookie Banner (5 Methods)
1. **XPath** - Direct path: `/html/body/div[1]/div/div[2]/div[3]`
2. **CSS Selector** - Class: `div.ds-button`
3. **CSS Class** - Specific: `.cookie_banner-accept-essential-button`
4. **Button Text** - Searches for buttons containing "necessary" or "only"
5. **DIV Text** - Searches all DIVs for "necessary" text

### Login Button (5 Methods)
1. **XPath** - Direct path: `/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[5]`
2. **CSS Selector** - Class: `div.ds-button`
3. **CSS Class** - Specific: `.ds-sign-up-form__register-button`
4. **Exact Text** - Searches for exact "log in" text
5. **Keywords** - Searches for "log", "sign", or "login" in text

## Project Structure

```
py-deepseek/
├── main.py                 # Application entry point
├── run.bat                 # Quick start script
├── credentials.json        # Your login credentials (create this)
├── requirements.txt        # Python dependencies
│
├── src/                    # Source code
│   ├── browser_manager.py      # Browser window management
│   ├── page_handler.py          # Cookie detection & page events
│   ├── login_button_detector.py # Login button detection
│   ├── keyboard_automation.py   # Credential entry
│   └── credentials_manager.py   # Credentials handling
│
├── config/                 # Configuration
│   └── settings.py             # All configurable settings
│
└── docs/                   # Documentation
    └── ...
```

## Requirements

- Python 3.9+
- Windows OS
- Internet connection

### Python Dependencies

```
pywebview==4.2.2
keyboard==0.13.5
```

Install with:
```bash
pip install -r requirements.txt
```

Or use the virtual environment:
```bash
env\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Edit `config/settings.py` to customize:

- `DEEPSEEK_URL` - Target website URL
- `WINDOW_WIDTH`, `WINDOW_HEIGHT` - Browser window size
- `COOKIE_PROCESSING_DELAY` - Wait time after cookie click
- `LOGIN_BUTTON_SEARCH_TIMEOUT` - Timeout for button detection

## How It Works

The automation uses a **multi-method fallback cascade**:

1. **Try Method 1** (XPath - fastest)
   - ✅ Found? → Click → Done!
   - ❌ Not found? → Try Method 2

2. **Try Method 2** (CSS Selector)
   - ✅ Found? → Click → Done!
   - ❌ Not found? → Try Method 3

3. **Try Method 3** (CSS Class)
   - ✅ Found? → Click → Done!
   - ❌ Not found? → Try Method 4

4. **Try Method 4** (Text Search)
   - ✅ Found? → Click → Done!
   - ❌ Not found? → Try Method 5

5. **Try Method 5** (Keyword Search)
   - ✅ Found? → Click → Done!
   - ❌ Not found? → Log failure and continue

All clicks happen **directly in JavaScript** for maximum reliability.

## Console Output

When running, you'll see output like:

```
============================================================
DeepSeek Chat Automation
============================================================

🍪 Detecting cookie banner (trying all methods)...
✅ Cookie banner clicked!
   Method: xpath

⌨️  Entering email...
✅ Email entered

⌨️  Entering password...
✅ Password entered

✅ Login button found and clicked!
   Method: css_selector
```

## Troubleshooting

### Button Not Found
- Check the console output to see which methods were tried
- The page structure may have changed - update XPaths in the code
- Ensure the page has fully loaded before detection runs

### Credentials Not Working
- Verify `credentials.json` exists in the project root
- Check JSON syntax is correct
- Ensure email and password are correct

### Browser Won't Open
- Check `DEEPSEEK_URL` in `config/settings.py`
- Ensure internet connection is active
- Verify pywebview is installed: `pip install pywebview`

## Development

### Run from Source
```bash
python main.py
```

### Build Executable
```bash
onefile.bat
```

This creates a standalone `.exe` in the `dist/` folder.

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is for educational purposes. Make sure you comply with DeepSeek's Terms of Service when using automation tools.

---

**Made with ❤️ for easier DeepSeek access**
