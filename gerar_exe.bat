@echo off
chcp 65001 >nul
title Gerando PC Ronyx Download Audio
cd /d "%~dp0"

echo [1/3] Instalando dependencias...
python -m pip install --upgrade pyinstaller yt-dlp
if errorlevel 1 goto erro

echo.
echo [2/3] Gerando o .exe (pode levar 1 a 3 minutos)...
python -m PyInstaller --noconfirm --onefile --windowed ^
  --name "PC Ronyx Download Audio" ^
  --icon logo.ico ^
  --collect-all yt_dlp ^
  baixar_audio.py
if errorlevel 1 goto erro

echo.
echo [3/3] Pronto!
echo O arquivo esta em: %~dp0dist\PC Ronyx Download Audio.exe
explorer "%~dp0dist"
pause
exit /b 0

:erro
echo.
echo Ocorreu um erro. Copie a mensagem acima e mande para o Claude.
pause
exit /b 1
