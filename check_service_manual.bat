@echo off
echo Проверяем конфигурацию сервиса на сервере...
echo.
echo 1. Конфигурация сервиса:
ssh root@147.45.164.202 "cat /etc/systemd/system/daryrei-bot.service"
echo.
echo 2. Права доступа к bot.py:
ssh root@147.45.164.202 "ls -la /var/www/daryrei-bot/bot.py"
echo.
echo 3. Статус сервиса:
ssh root@147.45.164.202 "systemctl status daryrei-bot --no-pager"
echo.
echo 4. Последние логи:
ssh root@147.45.164.202 "journalctl -xeu daryrei-bot.service --no-pager -n 10"
echo.
echo Готово!
pause
