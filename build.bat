@echo off

python -m pip install -r requirements.txt

pyinstaller ^
--onefile ^
--windowed ^
--name GeneratorRaportu ^
main.py
