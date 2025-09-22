@echo off
echo Исправляем конфигурацию сервиса на сервере...
echo.
echo 1. Останавливаем сервис:
ssh root@147.45.164.202 "systemctl stop daryrei-bot"
echo.
echo 2. Исправляем права доступа:
ssh root@147.45.164.202 "chown -R www-data:www-data /var/www/daryrei-bot"
ssh root@147.45.164.202 "chmod +x /var/www/daryrei-bot/bot.py"
echo.
echo 3. Перезагружаем systemd:
ssh root@147.45.164.202 "systemctl daemon-reload"
echo.
echo 4. Запускаем сервис:
ssh root@147.45.164.202 "systemctl start daryrei-bot"
echo.
echo 5. Проверяем статус:
ssh root@147.45.164.202 "systemctl status daryrei-bot --no-pager"
echo.
echo Готово!
pause
