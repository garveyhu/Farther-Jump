@echo off
cd /d %~dp0
pip install -r requirements.txt
cd src
python father_jump.py