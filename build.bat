@echo off

REM =====================================================
REM Instalacja wymaganych bibliotek
REM =====================================================

py -3.13 -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo BLAD PODCZAS INSTALACJI BIBLIOTEK
    pause
    exit /b 1
)


REM =====================================================
REM Instalacja PyInstaller
REM =====================================================

py -3.13 -m pip install pyinstaller

if errorlevel 1 (
    echo.
    echo BLAD PODCZAS INSTALACJI PYINSTALLER
    pause
    exit /b 1
)


REM =====================================================
REM Budowanie pliku EXE
REM =====================================================

py -3.13 -m PyInstaller ^
--clean ^
--noconfirm ^
--onefile ^
--windowed ^
--name GeneratorRaportu ^
main.py


REM =====================================================
REM Sprawdzenie wyniku
REM =====================================================

if errorlevel 1 (
    echo.
    echo BLAD PODCZAS BUDOWANIA EXE
    pause
    exit /b 1
)

echo.
echo ================================================
echo GOTOWE
echo ================================================
echo.
echo Plik znajduje sie w folderze:
echo dist\GeneratorRaportu.exe
echo.

pause