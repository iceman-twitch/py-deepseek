@echo off
REM Zip icon.ico (root) and dist\deepseek.exe into deepseek.zip
REM Only runs if BOTH files exist. No folders inside the zip - just the 2 files.

setlocal
cd /d "%~dp0"

if not exist "icon.ico" (
    echo [ERROR] icon.ico not found in root folder.
    goto :abort
)

if not exist "dist\deepseek.exe" (
    echo [ERROR] dist\deepseek.exe not found.
    goto :abort
)

echo [INFO] Both files found. Creating deepseek.zip...

if exist "deepseek.zip" del /f /q "deepseek.zip"

powershell -NoProfile -Command "Compress-Archive -Path 'icon.ico','dist\deepseek.exe' -DestinationPath 'deepseek.zip' -Force"

if exist "deepseek.zip" (
    echo [SUCCESS] deepseek.zip created with icon.ico and deepseek.exe.
) else (
    echo [ERROR] Failed to create deepseek.zip.
)
goto :end

:abort
echo [ABORTED] Zip not created - both files must exist.

:end
endlocal
