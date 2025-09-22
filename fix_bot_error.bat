@echo off
echo Исправляем ошибку в боте...

echo Добавляем исправленный bot.py...
git add bot.py

echo Создаем коммит...
git commit -m "Исправлена ошибка: удалена ссылка на несуществующий метод test_webapp_data_command"

echo Пушим изменения...
git push

echo Готово! Ошибка исправлена.
pause
