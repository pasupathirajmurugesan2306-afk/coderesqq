@echo off
title CoderesQ Debugging Platform
cd /d "%~dp0"
set SECRET_KEY="coderesq-secret"
set ADMIN_PASSWORD="password"
echo Starting CoderesQ...
python run.py
pause
