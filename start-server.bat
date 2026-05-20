@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo  Khoa hoc Automation Testing - Server
echo ========================================
echo.
echo Dang giai phong cong 5500 / 5501 (neu bi chiem)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5500 " ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5501 " ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
timeout /t 1 /nobreak >nul
echo.
echo Khoi dong python server.py ...
echo Mo trinh duyet: http://localhost:5500/index.html
echo.
python server.py
pause
