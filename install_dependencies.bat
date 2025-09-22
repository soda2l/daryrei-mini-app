@echo off
echo Устанавливаем зависимости Python на сервере...
echo.
echo 1. Устанавливаем python-telegram-bot:
ssh root@147.45.164.202 "pip3 install python-telegram-bot"
echo.
echo 2. Устанавливаем flask:
ssh root@147.45.164.202 "pip3 install flask"
echo.
echo 3. Устанавливаем requests:
ssh root@147.45.164.202 "pip3 install requests"
echo.
echo 4. Проверяем установку:
ssh root@147.45.164.202 "python3 -c 'import telegram, flask, requests; print(\"Все модули установлены успешно!\")'"
echo.
echo 5. Перезапускаем сервис:
ssh root@147.45.164.202 "systemctl restart daryrei-bot"
echo.
echo 6. Проверяем статус:
ssh root@147.45.164.202 "systemctl status daryrei-bot --no-pager"
echo.
echo Готово!
pause
