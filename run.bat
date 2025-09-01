@echo off
echo Activating Python environment...
call env\Scripts\activate

echo Running Python form.py...
py form.py

echo.
call env\Scripts\deactivate
pause