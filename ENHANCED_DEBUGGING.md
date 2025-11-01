# Enhanced Debugging & Detection Guide

## Current State

The project now has **enhanced debugging capabilities** for both cookie banner and login button detection.

### What Changed

#### 1. **Cookie Banner Detection** (`src/page_handler.py`)

The cookie detection now tries **4 different methods** in order:

1. **XPath Direct** - `/html/body/div[1]/div/div[2]/div[3]`
   - Fastest if element exists at this path
   - Returns coordinates if found

2. **Button Search** - Looks for `<button>` elements
   - Searches for text: "necessary", "only necessary", "only"
   - Safer than generic selectors
   - Common for cookie banners

3. **Text Search** - Looks for any element with "necessary" text
   - Fallback for custom HTML structures
   - Works with divs, spans, etc.

4. **Styled Button Search** - Looks for styled clickable elements
   - Finds elements with `cursor: pointer` or `onclick` attribute
   - Filters by text content
   - Catches custom button implementations

**Output:** Logs which method worked and returns coordinates for mouse clicking

#### 2. **Login Button Detection** (`src/login_button_detector.py`)

The login detection now tries **4 different methods**:

1. **XPath Direct** - `/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[5]`
   - Most specific path

2. **Button Search** - Looks for buttons with "log", "sign", "login" text
   - Searches actual `<button>` elements
   - Safer and more reliable

3. **Element Search** - Looks for clickable elements (button, a, div with onclick)
   - Catches custom implementations

4. **Debug Info** - Returns page structure info if nothing found
   - Total buttons found
   - Total elements on page
   - Can help identify why detection failed

**Output:** Comprehensive logging with position and detection method used

#### 3. **Mouse Module Implementation**

Changed from pyautogui to `mouse` module:

```python
# Correct syntax for mouse module:
mouse.move(x, y)           # Move to coordinates
time.sleep(0.2)            # Optional delay
mouse.click()              # Click at current position
```

**Not:**
```python
mouse.move(x, y, duration=0.2)  # ❌ Wrong - mouse module doesn't support duration
mouse.click('left', 1)           # ❌ Wrong - mouse module uses no parameters
```

---

## How to Debug

### Option 1: Run Full Automation (Standard)

```bash
run.bat
```

This will:
1. Detect cookie banner with enhanced logging
2. Show which detection method succeeded
3. Detect login button with enhanced logging
4. Click buttons with mouse module
5. Fill in credentials
6. Complete the form

**Look for output like:**
```
🍪 Detecting cookie banner (trying all methods)...
   Method used: xpath
✅ Cookie found at (640, 360)
🖱️  Clicking with mouse...
✅ Cookie banner clicked!
```

### Option 2: Simple Debug Test

```bash
python test_debug.py
```

This will:
1. Start the browser
2. Let the page fully load
3. Run debug JavaScript to show page structure
4. Test if XPaths can find elements
5. Keep browser window open for manual inspection

---

## What If Elements Still Not Found?

### Diagnosis Steps

1. **Open Browser Developer Tools**
   - Right-click on page → Inspect
   - Open Developer Console (F12)

2. **Test XPaths Manually**
   - In Console, paste:
   ```javascript
   // Cookie
   const xpath1 = "/html/body/div[1]/div/div[2]/div[3]";
   const result1 = document.evaluate(xpath1, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
   console.log(result1.singleNodeValue);  // Should show element or null
   
   // Login
   const xpath2 = "/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[5]";
   const result2 = document.evaluate(xpath2, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
   console.log(result2.singleNodeValue);  // Should show element or null
   ```

3. **If XPath Returns `null`**
   - Element doesn't exist at that path
   - DOM structure is different than expected
   - May be inside an iframe

4. **Alternative: Use CSS Selectors**
   ```javascript
   // Find by class
   document.querySelector('.cookie-button')
   
   // Find by id
   document.getElementById('accept-cookies')
   
   // Find by text
   Array.from(document.querySelectorAll('*')).find(el => 
     el.textContent.toLowerCase().includes('accept')
   )
   ```

### Common Issues

| Issue | Solution |
|-------|----------|
| XPath returns `null` | Use CSS selector or text search instead |
| Element found but `offsetParent` is null | Element is hidden, try alternative detection |
| Multiple elements with same text | Use `querySelectorAll` and index the one you need |
| Element inside iframe | Can't access via JavaScript (security restriction) |
| No button visible at all | Check page fully loaded; may need longer delay |

---

## Adding New Detection Methods

To add a detection method, edit the JavaScript in:
- `src/page_handler.py` - `handle_cookie_banner()` method
- `src/login_button_detector.py` - `detect_button_position()` method

Example: Add CSS selector search
```javascript
// Method 5: CSS Selector
const elem = document.querySelector('.cookie-banner-button');
if (elem && elem.offsetParent !== null) {
    console.log('✅ Method 5 (CSS selector) found');
    elem.click();
    return { method: 'css_selector', found: true, ... };
}
```

---

## Current Testing Status

- ✅ Mouse module installed and working
- ✅ Enhanced cookie detection with 4 methods
- ✅ Enhanced login detection with 4 methods
- ✅ Detailed logging and debug output
- ⏳ **Pending:** Test with actual page to see which methods work

**Next Step:** Run `run.bat` and check console output to see:
1. Does cookie banner get detected?
2. Which detection method succeeds?
3. Does login button get detected?
4. Do mouse clicks actually work?

---

## Files Modified

1. `src/page_handler.py`
   - Enhanced `handle_cookie_banner()` with multi-method detection
   - Better logging output

2. `src/login_button_detector.py`
   - Enhanced `detect_button_position()` with multi-method detection
   - Better logging output

3. `test_debug.py` (NEW)
   - Simple test script to diagnose issues
   - Doesn't perform full automation
   - Just shows page structure and tests XPaths

---

## Questions?

If detection still fails after running `run.bat`:

1. **Check console output** - Which method did it try? What did it find?
2. **Run test_debug.py** - See page structure and XPath results
3. **Use browser DevTools** - Manually verify XPaths work
4. **Check credentials.json** - Make sure it has valid data
5. **Check page URL** - Is it loading the correct website?

The enhanced logging will help identify exactly where the process fails.
