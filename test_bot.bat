@echo off
echo Тестируем бота...

echo Проверяем синтаксис...
python -m py_compile bot.py
if %errorlevel% neq 0 (
    echo Ошибка синтаксиса в bot.py
    pause
    exit /b 1
)

echo Синтаксис OK

echo Запускаем тест каталога...
python test_bot.py

echo Тест завершен!
pause
