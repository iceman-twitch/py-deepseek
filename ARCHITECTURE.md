# Technical Architecture Guide

## System Design

### Layered Architecture

```
┌─────────────────────────────────────────────────┐
│           main.py / form.py (Entry)             │
├─────────────────────────────────────────────────┤
│          browser_manager.BrowserManager         │
│     (Window creation & lifecycle management)    │
├─────────────────────────────────────────────────┤
│           page_handler.PageHandler              │
│   (Event handling & automation orchestration)   │
├────────────────────┬────────────────────────────┤
│                    │                            │
│  credentials_      keyboard_automation  login_  │
│  manager.py        .py                 button_  │
│                                        detector │
│                                        .py      │
└────────────────────┴────────────────────────────┘
│                                                 │
│ config.py (Configuration layer)                 │
│                                                 │
├─────────────────────────────────────────────────┤
│   pywebview / keyboard / requests (Libraries)   │
└─────────────────────────────────────────────────┘
```

## Module Dependencies

```
main.py
  └─ browser_manager.py
       ├─ config.py
       ├─ credentials_manager.py
       │  └─ config.py
       └─ page_handler.py
           ├─ config.py
           ├─ credentials_manager.py
           ├─ keyboard_automation.py
           └─ login_button_detector.py
               └─ config.py
```

## Data Flow

### 1. Initialization Phase
```
main.py
  ↓
BrowserManager.run()
  ├─ check_credentials_file()
  │  └─ CredentialsManager.create_template()
  ├─ create_window()
  │  └─ PageHandler.__init__()
  │     ├─ CredentialsManager()
  │     ├─ KeyboardAutomation()
  │     └─ LoginButtonDetector()
  └─ start()
     └─ webview.start()
```

### 2. Page Load Phase
```
Page Loaded
  ↓
PageHandler.on_page_loaded()
  ├─ handle_cookie_banner()
  └─ threading.Thread(enter_credentials_and_login)
```

### 3. Automation Phase
```
enter_credentials_and_login()
  ├─ KeyboardAutomation.type_email()
  ├─ KeyboardAutomation.type_password()
  ├─ PageHandler.validate_credentials_entered()
  │  └─ JavaScript check: form fields filled?
  ├─ LoginButtonDetector.auto_click_after_credentials()
  │  ├─ LoginButtonDetector.wait_for_button()
  │  ├─ LoginButtonDetector.get_button_coordinates()
  │  └─ LoginButtonDetector.click_login_button()
  └─ Success/Failure reported
```

## Key Design Patterns

### 1. Single Responsibility Principle
Each module has one clear responsibility:
- **config.py**: Configuration management
- **credentials_manager.py**: Credential handling
- **keyboard_automation.py**: Keyboard input
- **login_button_detector.py**: Button detection
- **page_handler.py**: Event orchestration
- **browser_manager.py**: Browser lifecycle

### 2. Separation of Concerns
- **JavaScript code** for DOM interaction (JavaScript)
- **Python code** for logic and coordination
- **Configuration** separate from implementation

### 3. Dependency Injection
PageHandler receives window object instead of creating it:
```python
def __init__(self, window):
    self.window = window  # Injected dependency
```

### 4. Callback Pattern
LoginButtonDetector uses callbacks for validation:
```python
detector.auto_click_after_credentials(
    credentials_callback=validate_function
)
```

## Login Button Detection Algorithm

### Detection Strategy

```
detect_button_position()
  ├─ Build list of selectors (CSS + XPath)
  ├─ For each selector:
  │  ├─ Query DOM
  │  ├─ Check if visible (offsetParent !== null)
  │  ├─ Calculate bounding box
  │  ├─ Return center coordinates + dimensions
  │  └─ Break on first match
  └─ Return null if no button found
```

### Coordinate Calculation

```
JavaScript getBoundingClientRect()
  ├─ Returns relative to viewport
  ├─ We calculate center point:
  │  ├─ x = left + width/2
  │  ├─ y = top + height/2
  └─ Return {x, y, width, height, text}
```

### Validation Before Click

```
auto_click_after_credentials()
  ├─ wait_for_button(timeout=10s)
  │  └─ Retry every 0.5s until found or timeout
  ├─ validate_credentials_entered()
  │  ├─ Check email field has value
  │  ├─ Check password field has value
  │  └─ Return both_filled
  ├─ If validation fails → Return False
  └─ click_login_button()
     └─ Attempt JavaScript click
```

## Error Handling Strategy

### Multi-Layer Error Handling

```
Layer 1: Try-Catch Blocks
  └─ Catch exceptions, log, continue gracefully

Layer 2: Validation Checks
  ├─ Credentials valid?
  ├─ Button found?
  ├─ Fields filled?
  └─ Return boolean result

Layer 3: Timeouts
  ├─ LOGIN_BUTTON_SEARCH_TIMEOUT: 10 seconds
  ├─ FIELD_FOCUS_DELAY: 0.5 seconds
  └─ Prevent infinite loops

Layer 4: User Feedback
  └─ Print descriptive messages
```

### Error Messages Format
```python
print("✅ Success message")     # Green check
print("❌ Error message")        # Red X
print("⚠️  Warning message")     # Warning
print("⏱️  Timeout message")     # Clock
print("🍪 Cookie message")       # Cookie
print("📝 Field message")        # Paper
print("🔐 Security message")    # Lock
```

## Threading Model

### Current Implementation
- **Main thread**: UI event loop (webview)
- **Worker thread**: Credential entry automation (daemon thread)

```python
threading.Thread(
    target=enter_credentials_and_login,
    daemon=True  # Dies when main thread exits
).start()
```

### Why Daemon Thread?
1. Non-blocking: Doesn't block UI
2. Auto-cleanup: Dies with main process
3. Responsive: UI remains interactive

## JavaScript Integration

### Execution Method
```python
result = window.evaluate_js(javascript_code)
```

### Communication Pattern
- **Python → JavaScript**: Send code string
- **JavaScript → Python**: Return serializable value
- **Data types**: strings, numbers, booleans, dicts, lists

### Key JavaScript Functions

1. **focusEmailField()** - Find and focus email input
2. **focusPasswordField()** - Find and focus password input
3. **handleCookieBanner()** - Click cookie accept button
4. **detectLoginButton()** - Find login button coordinates
5. **clickLoginButton()** - Click login button
6. **validateCredentialsEntered()** - Check form fields

## Configuration Hierarchy

```
Default Values (in module code)
  ↓
config.py settings
  ↓
Optional overrides at runtime
```

## Extensibility Points

### 1. Add New Selectors
Edit `config.py`:
```python
LOGIN_BUTTON_SELECTORS = [
    'your-custom-selector',
    ...
]
```

### 2. Add New Automation Steps
Edit `page_handler.py`:
```python
def on_page_loaded(self):
    # Add new step here
```

### 3. Custom Button Detection
Create new detector in `login_button_detector.py`:
```python
def detect_custom_button(self):
    # Custom detection logic
```

### 4. Add Pre-login Steps
Edit `PageHandler.enter_credentials_and_login()`:
```python
def enter_credentials_and_login(self):
    # Add step before keyboard entry
    self.handle_two_factor_auth()  # New step
    # Continue with existing steps
```

## Testing Strategy

### Unit Test Candidates
- `CredentialsManager.validate_credentials()`
- `KeyboardAutomation.type_text()`
- `LoginButtonDetector.detect_button_position()`
- `PageHandler.validate_credentials_entered()`

### Integration Test Candidates
- Full credential entry flow
- Cookie banner handling
- Button detection → click flow

### Manual Testing
1. Test with valid credentials
2. Test with missing credentials.json
3. Test with slow-loading page
4. Test with missing login button

## Performance Considerations

### Optimization Opportunities
1. **Caching**: Cache button coordinates if page doesn't reload
2. **Parallel**: Run button detection while typing
3. **Timeout tuning**: Adjust timeouts based on target site

### Current Bottlenecks
1. **JavaScript evaluation**: One at a time
2. **Network delay**: Waiting for page to load
3. **Cookie banner**: May take time to handle

## Security Notes

### Credentials Storage
⚠️ **Warning**: Storing passwords in JSON is NOT production-safe

**Recommendations**:
1. Use environment variables: `DEEPSEEK_PASSWORD=xxx`
2. Use secure credential vault
3. Encrypt credentials.json
4. Use token-based auth if available

### Code Execution
- Only execute trusted JavaScript
- Don't pass user input directly to evaluate_js()
- Validate all inputs

## Future Enhancements

### Planned Features
- [ ] 2FA/MFA support
- [ ] Session persistence (cookies)
- [ ] Headless browser option
- [ ] Credential encryption
- [ ] Logging framework
- [ ] Configuration file (YAML/TOML)
- [ ] Retry logic with exponential backoff
- [ ] Screenshot capability for debugging

### Scalability
- [ ] Support multiple accounts
- [ ] Parallel automation for multiple windows
- [ ] Queue-based task distribution
- [ ] Webhook notifications

---

**Architecture Version**: 2.0
**Last Updated**: November 1, 2025
