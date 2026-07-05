# 🍪 Cookie Click Implementation - How It Works

## Location: `src/page_handler.py`

### 1. **Method: `handle_cookie_banner()`** (Lines 31-79)

This method handles clicking the "Necessary cookies only" button:

```python
def handle_cookie_banner(self):
    """Handle cookie banner acceptance using XPath"""
    js_code = """
    function handleCookieBanner() {
        try {
            // Use XPath to find "Necessary cookies only" div
            const xpath = "/html/body/div[1]/div/div[2]/div[3]";
            const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
            const cookieButton = result.singleNodeValue;
            
            if (cookieButton && cookieButton.offsetParent !== null) {
                console.log('Found cookie button via XPath:', cookieButton.textContent);
                const rect = cookieButton.getBoundingClientRect();
                return {
                    x: Math.round(rect.left + rect.width / 2),
                    y: Math.round(rect.top + rect.height / 2),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height),
                    text: cookieButton.textContent.trim()
                };
            }
            return null;
        } catch (e) {
            console.error('Cookie error:', e);
            return null;
        }
    }
    return handleCookieBanner();
    """
    
    try:
        print("🍪 Handling cookie banner (XPath: /html/body/div[1]/div/div[2]/div[3])...")
        result = self.window.evaluate_js(js_code)
        if result:
            print(f"✅ Cookie button found: {result['text']}")
            print(f"   Position: ({result['x']}, {result['y']})")
            # 👈 THIS IS WHERE THE CLICK HAPPENS:
            self._simulate_mouse_click(result['x'], result['y'])
            # 👆 Simulates mouse click at button coordinates
            
            print("✅ Cookie banner accepted")
            time.sleep(COOKIE_PROCESSING_DELAY)
            # Give extra time for cookie banner to fully disappear
            time.sleep(1.0)
        else:
            print("⚠️  No cookie banner found, continuing...")
        return True
    except Exception as e:
        print(f"⚠️  Error handling cookie banner: {e}")
        return False
```

### 2. **Method: `_simulate_mouse_click(x, y)`** (Lines 81-88)

This is the method that actually clicks the mouse:

```python
def _simulate_mouse_click(self, x, y):
    """Simulate mouse click at given coordinates"""
    try:
        print(f"🖱️  Simulating mouse click at ({x}, {y})")
        pyautogui.click(x, y)  # 👈 THIS CLICKS THE MOUSE
        time.sleep(0.3)
    except Exception as e:
        print(f"⚠️  Error simulating mouse click: {e}")
```

---

## 🔍 **Flow Step by Step:**

1. **Page loads** → `on_page_loaded()` is called
2. **Wait 0.5 seconds** for cookie banner to appear
3. **Find XPath:** `/html/body/div[1]/div/div[2]/div[3]`
4. **Get coordinates** of the button
5. **Print:** `🖱️  Simulating mouse click at (x, y)`
6. **pyautogui.click(x, y)** ← **ACTUAL MOUSE CLICK**
7. **Wait 2 seconds** for cookie banner to disappear
8. **Continue** with credentials entry

---

## 📍 **XPath for Cookie Button:**

```
/html/body/div[1]/div/div[2]/div[3]
```

This div contains: `"Necessary cookies only"`

---

## ✅ **Output You'll See:**

```
🍪 Handling cookie banner (XPath: /html/body/div[1]/div/div[2]/div[3])...
✅ Cookie button found: Necessary cookies only
   Position: (728, 745)
🖱️  Simulating mouse click at (728, 745)
✅ Cookie banner accepted
```

---

## 📚 **Files Involved:**

| File | Method | Purpose |
|------|--------|---------|
| `src/page_handler.py` | `handle_cookie_banner()` | Finds & clicks cookie button |
| `src/page_handler.py` | `_simulate_mouse_click()` | Simulates mouse click using pyautogui |
| `src/page_handler.py` | `on_page_loaded()` | Calls handle_cookie_banner() |

---

## 🖱️ **Mouse Click Technology:**

- **Library:** `pyautogui` (version 0.9.53)
- **Function:** `pyautogui.click(x, y)`
- **What it does:** Moves mouse to coordinates and clicks left button

---

## ✨ **Summary**

When the page loads, the automation:
1. ✅ Uses XPath to find the "Necessary cookies only" div
2. ✅ Gets its screen coordinates
3. ✅ **Clicks the mouse at those coordinates** using `pyautogui.click()`
4. ✅ Waits for banner to disappear
5. ✅ Continues with email/password entry
