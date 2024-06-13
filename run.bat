@echo off
cd %~dp0
python main2.py
timeout 60
python dell.py
exit
