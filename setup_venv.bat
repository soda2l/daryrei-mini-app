@echo off
echo Настраиваем виртуальное окружение на сервере...
echo.
echo 1. Создаем виртуальное окружение:
ssh root@147.45.164.202 "cd /var/www/daryrei-bot && python3 -m venv venv"
echo.
echo 2. Активируем виртуальное окружение и устанавливаем зависимости:
ssh root@147.45.164.202 "cd /var/www/daryrei-bot && source venv/bin/activate && pip install python-telegram-bot flask requests"
echo.
echo 3. Проверяем установку:
ssh root@147.45.164.202 "cd /var/www/daryrei-bot && source venv/bin/activate && python -c 'import telegram, flask, requests; print(\"Все модули установлены успешно!\")'"
echo.
echo 4. Обновляем конфигурацию сервиса для использования venv:
ssh root@147.45.164.202 "cat > /etc/systemd/system/daryrei-bot.service << 'EOF'
[Unit]
Description=DaryRei Bot
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/daryrei-bot
ExecStart=/var/www/daryrei-bot/venv/bin/python /var/www/daryrei-bot/bot.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/var/www/daryrei-bot

[Install]
WantedBy=multi-user.target
EOF"
echo.
echo 5. Перезагружаем systemd:
ssh root@147.45.164.202 "systemctl daemon-reload"
echo.
echo 6. Перезапускаем сервис:
ssh root@147.45.164.202 "systemctl restart daryrei-bot"
echo.
echo 7. Проверяем статус:
ssh root@147.45.164.202 "systemctl status daryrei-bot --no-pager"
echo.
echo Готово!
pause
