@echo off
echo Activating virtual environment...
call tele\Scripts\activate.bat

echo Starting Daphne server...
start cmd /k "daphne -b 0.0.0.0 -p 8000 telescope_log.asgi:application"

timeout /t 5 /nobreak > NUL
echo Opening project in browser...
start http://127.0.0.1:8000