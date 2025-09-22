@echo off
echo Быстрое исправление systemd сервиса...
echo.
echo 1. Останавливаем сервис:
ssh root@147.45.164.202 "systemctl stop daryrei-bot"
echo.
echo 2. Создаем правильную конфигурацию сервиса:
ssh root@147.45.164.202 "cat > /etc/systemd/system/daryrei-bot.service << 'EOF'
[Unit]
Description=DaryRei Bot
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/daryrei-bot
ExecStart=/usr/bin/python3 /var/www/daryrei-bot/bot.py
Restart=always
RestartSec=10
Environment=PYTHONPATH=/var/www/daryrei-bot

[Install]
WantedBy=multi-user.target
EOF"
echo.
echo 3. Исправляем права доступа:
ssh root@147.45.164.202 "chown -R www-data:www-data /var/www/daryrei-bot"
ssh root@147.45.164.202 "chmod +x /var/www/daryrei-bot/bot.py"
echo.
echo 4. Перезагружаем systemd:
ssh root@147.45.164.202 "systemctl daemon-reload"
echo.
echo 5. Запускаем сервис:
ssh root@147.45.164.202 "systemctl start daryrei-bot"
echo.
echo 6. Проверяем статус:
ssh root@147.45.164.202 "systemctl status daryrei-bot --no-pager"
echo.
echo Готово!
pause
