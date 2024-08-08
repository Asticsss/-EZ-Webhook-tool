@echo off
echo Installing dependecies...
pip install -r requirements.txt
cls
echo Running EZWebhookTool...
py EZWebhookTool.py
timeout /t 2

