@echo off
echo Тестируем обработку фото...

echo Проверяем синтаксис bot.py...
python -m py_compile bot.py
if %errorlevel% neq 0 (
    echo Ошибка синтаксиса в bot.py
    pause
    exit /b 1
)

echo Синтаксис OK

echo Тестируем обработку фото...
python test_photo.py

echo Тест завершен!
pause
