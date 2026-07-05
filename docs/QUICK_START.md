# 🚀 QUICK START GUIDE

## What Changed?

Your project has been reorganized from a cluttered root folder into a **clean, professional folder structure**.

---

## 📁 New Structure

```
py-deepseek/
├── main.py                    ← Run this (or use run.bat)
├── credentials.json           ← Your login info
├── run.bat                    ← Easy start button
├── src/                       ← Source code
│   ├── browser_manager.py
│   ├── credentials_manager.py
│   ├── keyboard_automation.py
│   ├── login_button_detector.py ⭐ NEW
│   └── page_handler.py
├── config/                    ← Settings
│   └── settings.py
├── docs/                      ← Guides
│   ├── QUICKSTART.md
│   ├── README_NEW.md
│   └── ... (10 more)
└── env/                       ← Python environment
```

---

## ⚡ Quick Start (3 Steps)

### Step 1: Add Your Credentials
Edit `credentials.json` in the root folder:
```json
{
    "username": "your_email@example.com",
    "password": "your_password"
}
```

### Step 2: Run the Application
**Option A (Easiest):** Double-click `run.bat`

**Option B (Command line):**
```
run.bat
```

**Option C (Manual):**
```
env\Scripts\activate
py main.py
env\Scripts\deactivate
```

### Step 3: Done! ✅
- Browser opens
- Credentials auto-filled
- Login button detected & clicked
- You're logged in!

---

## 📂 File Organization

| Folder | Purpose | Files |
|--------|---------|-------|
| `src/` | Your code | 5 Python modules |
| `config/` | Settings | 1 config file |
| `docs/` | Guides | 12 markdown files |
| `env/` | Python | Virtual environment |
| Root | Entry point | `main.py`, `run.bat` |

---

## 🎯 What Each Module Does

| Module | Purpose |
|--------|---------|
| `browser_manager.py` | Opens & manages browser window |
| `page_handler.py` | Handles page events |
| `credentials_manager.py` | Loads your login info |
| `keyboard_automation.py` | Types your credentials |
| `login_button_detector.py` | Finds & clicks login button ⭐ |

---

## ⚙️ Customize Settings

Edit `config/settings.py`:
```python
# Window size
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Typing speed (seconds per character)
TYPING_DELAY = 0.05

# Button detection timeout (seconds)
LOGIN_BUTTON_SEARCH_TIMEOUT = 10

# ... 15+ more options
```

---

## ✅ Verify Everything Works

1. **Edit credentials:** `credentials.json`
2. **Run:** `run.bat`
3. **Check:**
   - ✅ Browser opens
   - ✅ Email/password filled in
   - ✅ Login button clicked
   - ✅ Logged in successfully

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| `run.bat` doesn't work | Try manual: `env\Scripts\activate && py main.py` |
| ModuleNotFoundError | Run from project root folder |
| credentials.json not found | Make sure it's in root folder with correct name |
| Button not detected | Check `docs/LOGIN_BUTTON_DETECTION.md` |

---

## 📖 Need Help?

- Quick start: `docs/QUICKSTART.md`
- Full guide: `docs/README_NEW.md`
- Technical details: `docs/ARCHITECTURE.md`
- Button detection: `docs/LOGIN_BUTTON_DETECTION.md`

---

## 🎉 That's It!

Your project is now:
- ✅ **Organized** - Clean folders
- ✅ **Ready** - Just run `run.bat`
- ✅ **Documented** - 12 guides available
- ✅ **Working** - All features functional

**To start:** `run.bat`

---

## Key Reminders

✅ Always use `run.bat` to activate environment
✅ Keep `credentials.json` in root folder
✅ Edit `config/settings.py` for custom options
✅ View `docs/` for detailed guides
✅ Source code is in `src/` folder

---

**Happy automating!** 🚀
