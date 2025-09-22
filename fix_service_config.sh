#!/bin/bash

echo "🔧 Исправляем конфигурацию systemd сервиса..."

# Останавливаем сервис
systemctl stop daryrei-bot

# Создаем правильную конфигурацию сервиса
cat > /etc/systemd/system/daryrei-bot.service << 'EOF'
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
EOF

# Исправляем права доступа
chown -R www-data:www-data /var/www/daryrei-bot
chmod +x /var/www/daryrei-bot/bot.py

# Перезагружаем systemd
systemctl daemon-reload

# Запускаем сервис
systemctl start daryrei-bot

# Проверяем статус
echo "📊 Статус сервиса:"
systemctl status daryrei-bot --no-pager

echo "✅ Исправление завершено"
