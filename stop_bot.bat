@echo off
echo Останавливаем все процессы Python...

echo Ищем процессы Python...
tasklist | findstr python
if %errorlevel% neq 0 (
    echo Процессы Python не найдены
) else (
    echo Останавливаем процессы Python...
    taskkill /f /im python.exe
    taskkill /f /im pythonw.exe
)

echo Готово! Теперь можно запустить бота заново.
pause
