@echo off

start "Backend - CineLog" cmd /k "cd /d "%~dp0backend" && ..\.venv\Scripts\activate && python app.py"

start "Frontend - CineLog" cmd /k "cd /d "%~dp0frontend\cinelog-react" && npm run dev"