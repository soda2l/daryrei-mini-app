@echo off
echo Решаем проблему с git...

echo Добавляем все файлы...
git add .

echo Создаем коммит...
git commit -m "Добавлены инструкции и скрипты для переключения веток"

echo Переключаемся на ветку main...
git checkout main

echo Готово! Теперь ты на ветке main.
pause
