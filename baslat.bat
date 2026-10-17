@echo off
title Ege CBS Sunucusu
color 0b

echo ==================================================
echo         Ege CBS Projesi - Baslatma Komutu
echo ==================================================
echo.

set "PY_CMD=python"
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        color 0c
        echo UYARI: Bilgisayarinizda Python yuklu degil veya PATH sistem degiskenine eklenmemis!
        echo Gerekli surum olan Python 3.11.0 indirme sayfasina yonlendiriliyorsunuz...
        echo Kurulum sirasinda "Add Python to PATH" secenegini isaretlemeyi unutmayin!
        echo.
        start https://www.python.org/downloads/release/python-3110/
        pause
        exit /b 1
    ) else (
        set "PY_CMD=py"
    )
)

if exist requirements.txt (
    echo Kutuphaneler kontrol ediliyor ve yukleniyor...
    REM Pip encoding guvenligi icin UTF-8 ayarlaniyor
    set PYTHONUTF8=1
    %PY_CMD% -m pip install -r requirements.txt
    echo Kutuphaneler hazir!
) else (
    echo Bilgi: requirements.txt bulunamadi, dahili kutuphanelerle devam ediliyor...
)

echo.
echo Sunucu baslatiliyor, tarayici aciliyor...
echo Harita Sayfasi : http://localhost:3000/
echo Admin Paneli   : http://localhost:3000/admin/
echo.

start http://localhost:3000/
%PY_CMD% server.py

pause
