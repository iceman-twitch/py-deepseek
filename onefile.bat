@echo off
echo Activating Python environment...
call env\Scripts\activate

echo Cleaning up old build and dist folders...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
echo [OK] Cleanup complete!

echo.
echo Running PyInstaller using deepseek.spec...
pyinstaller deepseek.spec

echo.
echo Build complete! Check the 'dist' folder for your executable.
call env\Scripts\deactivate
pause