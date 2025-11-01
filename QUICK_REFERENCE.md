# Quick Reference: Testing Button Detection

## One-Liner: Run Everything

```bash
run.bat
```

This will:
1. ✅ Detect and click cookie banner (4 methods)
2. ✅ Detect and click login button (4 methods)
3. ✅ Enter email/password
4. ✅ Complete the form

---

## What to Look For

### ✅ Success Signs
- See: `🍪 Detecting cookie banner...`
- See: `✅ Cookie found at (x, y)`
- See: `✅ Cookie banner clicked!`
- See: `🔍 Detecting login button...`
- See: `✅ Login button found!`
- See: `✅ Login button clicked!`

### ❌ Problem Signs
- See: `⚠️ Cookie banner not found`
- See: `❌ Login button not found`
- See any Python error with traceback

---

## If Something Fails

### Option 1: More Debugging
```bash
python test_debug.py
```
Shows what's on the page and if XPaths work.

### Option 2: Check Browser Manually
1. Open DevTools (F12)
2. Console tab
3. Run:
```javascript
// Test if XPath finds cookie element
const x1 = "/html/body/div[1]/div/div[2]/div[3]";
const r1 = document.evaluate(x1, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
console.log(r1.singleNodeValue);  // null = not found

// Test if XPath finds login element
const x2 = "/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[5]";
const r2 = document.evaluate(x2, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
console.log(r2.singleNodeValue);  // null = not found
```

---

## What Changed

| Component | Change |
|-----------|--------|
| Cookie Detection | Now tries 4 methods instead of 1 |
| Login Detection | Now tries 4 methods instead of 1 |
| Logging | Shows which method succeeded |
| Mouse Module | Confirmed correct syntax |

---

## Detection Methods (in order)

### Cookie Banner
1. XPath: `/html/body/div[1]/div/div[2]/div[3]`
2. Button with "necessary" text
3. Any element with "necessary" text
4. Styled clickable element

### Login Button
1. XPath: `/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[5]`
2. Element with exact text "Log in"
3. Button/link with "log", "sign", "login"
4. Styled clickable element

---

## Status Check

✅ **Complete & Ready:**
- Folder structure (src/, config/, docs/)
- Configuration system
- Credentials loading
- Keyboard automation
- Browser management
- Cookie detection (4 methods)
- Login detection (4 methods)
- Mouse module integration
- Comprehensive logging
- Debug script

⏳ **Pending:**
- Test with actual website
- Verify buttons actually click
- Confirm credentials are entered

---

## Files to Know

- `run.bat` - Main entry point
- `main.py` - Application start
- `src/page_handler.py` - Cookie detection
- `src/login_button_detector.py` - Login detection
- `src/browser_manager.py` - Window management
- `config/settings.py` - All settings
- `test_debug.py` - Debug script
- `ENHANCED_DEBUGGING.md` - Full debugging guide

---

## Common Questions

**Q: Why isn't the cookie banner detected?**
A: The 4-method system should find it. Run `test_debug.py` to see page structure.

**Q: Will it work if XPath is wrong?**
A: Yes! Methods 2-4 are fallbacks. It will search by button text, generic text, or styled elements.

**Q: What if nothing works?**
A: Run `test_debug.py`, open browser DevTools, manually test the XPaths to see if elements exist.

**Q: How do I know if it's working?**
A: Check console output from `run.bat`. It will show exactly what happened at each step.

**Q: Can I see all buttons on the page?**
A: Run `test_debug.py` - it shows all buttons and cookie-related elements.

---

## Next Action

```bash
run.bat
```

Check the console output. If it works, great! If not, run `test_debug.py` to diagnose.
