#!/bin/bash

echo "🔧 Исправляем права доступа на сервере..."

# Переходим в директорию бота
cd /var/www/daryrei-bot

# Устанавливаем правильного владельца
sudo chown -R www-data:www-data /var/www/daryrei-bot

# Устанавливаем права на запись
sudo chmod -R 755 /var/www/daryrei-bot
sudo chmod 664 catalog.json
sudo chmod 755 images/

# Перезапускаем бота
sudo systemctl restart daryrei-bot

echo "✅ Права доступа исправлены"
echo "✅ Бот перезапущен"

# Проверяем статус
sudo systemctl status daryrei-bot --no-pager
