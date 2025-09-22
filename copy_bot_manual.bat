@echo off
echo Копируем bot.py на сервер...
echo.
echo 1. Копируем файл:
scp bot.py root@147.45.164.202:/var/www/daryrei-bot/
echo.
echo 2. Исправляем права:
ssh root@147.45.164.202 "chown www-data:www-data /var/www/daryrei-bot/bot.py"
ssh root@147.45.164.202 "chmod +x /var/www/daryrei-bot/bot.py"
echo.
echo 3. Перезапускаем сервис:
ssh root@147.45.164.202 "systemctl restart daryrei-bot"
echo.
echo 4. Проверяем статус:
ssh root@147.45.164.202 "systemctl status daryrei-bot --no-pager"
echo.
echo Готово!
pause
