"""
Central logging utility for DeepSeek Automation.

Logs every action both to the console and to deepseek_error.log so the full
run can be reviewed later. The log file is git-ignored.
"""
import os
import sys
from datetime import datetime

# Resolve project root the same way config/settings.py does, so the log lands
# next to the executable/script regardless of how the app is launched.
if getattr(sys, 'frozen', False):
    _ROOT = os.path.dirname(sys.executable)
else:
    _ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_FILE = os.path.join(_ROOT, 'deepseek_error.log')


def log(message, to_console=True):
    """
    Write a timestamped message to the log file (and optionally the console).

    Args:
        message: Text to log.
        to_console: Also print to stdout (default True).
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {message}"
    if to_console:
        try:
            print(message)
        except Exception:
            pass
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + "\n")
    except Exception:
        pass  # Never let logging crash the app
