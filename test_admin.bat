@echo off
echo Тестируем админские функции...

echo Проверяем синтаксис bot.py...
python -m py_compile bot.py
if %errorlevel% neq 0 (
    echo Ошибка синтаксиса в bot.py
    pause
    exit /b 1
)

echo Синтаксис OK

echo Тестируем каталог...
python test_admin.py

echo Тест завершен!
pause
