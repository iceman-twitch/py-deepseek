@echo off
echo Activating Python environment...
call env\Scripts\activate

echo Running DeepSeek Automation...
py main.py

echo.
call env\Scripts\deactivate
pause