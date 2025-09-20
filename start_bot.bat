@echo off
echo === ЗАПУСК БОТА DARYREI ===
echo.

REM Проверяем, есть ли запущенные процессы Python
tasklist /FI "IMAGENAME eq python.exe" | find "python.exe" >nul
if %ERRORLEVEL% == 0 (
    echo Обнаружены запущенные процессы Python
    echo Останавливаем все процессы...
    taskkill /F /IM python.exe
    echo Ждем 3 секунды...
    timeout /t 3 /nobreak >nul
)

echo Запускаем бота...
python bot.py

pause

