@echo off
echo Проверяем ошибку Python скрипта...
echo.
echo 1. Запускаем bot.py напрямую для диагностики:
ssh root@147.45.164.202 "cd /var/www/daryrei-bot && python3 bot.py"
echo.
echo 2. Проверяем логи Python:
ssh root@147.45.164.202 "journalctl -xeu daryrei-bot.service --no-pager -n 20"
echo.
echo 3. Проверяем синтаксис Python:
ssh root@147.45.164.202 "cd /var/www/daryrei-bot && python3 -m py_compile bot.py"
echo.
echo 4. Проверяем зависимости:
ssh root@147.45.164.202 "cd /var/www/daryrei-bot && python3 -c 'import telegram, flask, requests'"
echo.
echo Готово!
pause
