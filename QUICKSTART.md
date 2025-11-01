# Quick Start Guide

## 5-Minute Setup

### Step 1: Verify Python Installation
```powershell
python --version
# Should show Python 3.9 or higher
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run the Application
```powershell
python main.py
```

On first run, it will create `credentials.json` template.

### Step 4: Add Your Credentials
Edit `credentials.json`:
```json
{
    "username": "your_email@example.com",
    "password": "your_password"
}
```

### Step 5: Run Again
```powershell
python main.py
```

The app will:
1. ✅ Open DeepSeek Chat in a browser window
2. ✅ Handle cookie banners
3. ✅ Fill in email automatically
4. ✅ Fill in password automatically
5. ✅ Detect login button location on screen
6. ✅ Click login button automatically

---

## What's New in This Version?

### 🎯 Login Button Auto-Detection
The application now **automatically detects where the login button is on the screen** and calculates the exact coordinates from the window position, then **clicks it automatically** after credentials are entered.

### 📦 Better Project Structure
Instead of one big `form.py`, the code is now organized into:

| File | Purpose |
|------|---------|
| `main.py` | Entry point ⭐ |
| `config.py` | All settings in one place |
| `credentials_manager.py` | Handles credentials safely |
| `keyboard_automation.py` | Types credentials |
| `login_button_detector.py` | **NEW** - Finds and clicks login button |
| `browser_manager.py` | Manages browser window |
| `page_handler.py` | Orchestrates automation |

### ✅ Smart Validation
Before clicking login, the app validates:
- ✓ Email field is filled
- ✓ Password field is filled
- ✓ Login button is visible and accessible

---

## Features Overview

### 🤖 Full Automation
1. **Cookie Banner** - Automatically accepts
2. **Email Entry** - Types your email
3. **Password Entry** - Types your password
4. **Login Detection** - Finds login button
5. **Auto-Click** - Clicks login button
6. **Smart Validation** - Only clicks after validation

### 🔍 Button Detection Details
The app searches for login button using:
- Button text containing "Login" or "Sign in"
- Standard button element types
- Custom button classes
- ARIA labels
- Multiple backup methods

### ⚙️ Highly Configurable
All settings in `config.py`:
- Timing delays
- UI selectors
- Timeouts
- Window size

### 🧵 Non-Blocking
- UI remains responsive
- Automation runs in background thread
- Can cancel anytime

---

## Troubleshooting

### Q: Credentials not entered?
**A:** Check `credentials.json` exists and is valid JSON

### Q: Login button not found?
**A:** 
1. Check browser console for errors
2. Increase `LOGIN_BUTTON_SEARCH_TIMEOUT` in `config.py`
3. Add custom selector for your target site

### Q: Application won't start?
**A:** Run: `pip install -r requirements.txt`

### Q: Old code not working?
**A:** Old `form.py` still works but uses new modular structure internally

---

## File Structure After Setup
```
py-deepseek/
├── main.py                      ⭐ Run this
├── form.py                      (Legacy, uses main structure)
├── config.py                    Configuration
├── credentials.json             Your credentials (create yourself)
├── credentials_manager.py       
├── keyboard_automation.py       
├── login_button_detector.py     NEW - Button detection
├── browser_manager.py           
├── page_handler.py              
├── requirements.txt             
├── README_NEW.md                Full documentation
├── ARCHITECTURE.md              Technical details
└── QUICKSTART.md               This file
```

---

## Advanced Usage

### Custom Button Selector
Edit `config.py`:
```python
LOGIN_BUTTON_SELECTORS = [
    'button:contains("Login")',      # These are tried first
    'button.my-custom-class',         # Add your custom selector here
    'button[id="submit-btn"]',        # More custom options
]
```

### Adjust Timings
If page is slow, increase delays in `config.py`:
```python
FIELD_FOCUS_DELAY = 1.0        # Increase to 1 second
TYPING_DELAY = 1.0              # Give more time for typing
LOGIN_BUTTON_SEARCH_TIMEOUT = 20  # Wait up to 20 seconds
```

### Debug Mode
Add prints in `page_handler.py`:
```python
print(f"Button location: {self.login_detector.get_button_coordinates()}")
```

---

## Run Commands

### Standard Start
```powershell
python main.py
```

### Legacy Start (still works)
```powershell
python form.py
```

### Build Standalone Executable
```powershell
pyinstaller -F --add-data "credentials.json:." main.py
```

---

## File Locations
After first run, look for:
- **Browser Window**: Opens automatically
- **Console Output**: Shows automation progress
- **credentials.json**: Created in project root
- **Error Logs**: Printed to console

---

## Next Steps

1. **Read** `README_NEW.md` for full documentation
2. **Read** `ARCHITECTURE.md` for technical details
3. **Customize** `config.py` for your needs
4. **Test** with your DeepSeek account

---

## Support

For issues:
1. Check credentials.json is valid
2. Check browser console (F12) for errors
3. Increase timeouts if page is slow
4. Add custom selectors for your website

---

**Version**: 2.0 with Auto-Click Login Button  
**Updated**: November 1, 2025
