#!/bin/bash

# Скрипт для исправления прав доступа к файлам бота

echo "🔧 Исправляем права доступа к файлам бота..."

# Переходим в папку бота
cd /var/www/daryrei_bot

# Даем права на запись к catalog.json
chmod 666 catalog.json

# Даем права на запись к папке images
chmod 755 images/
chmod 664 images/*

# Устанавливаем правильного владельца (замените на нужного пользователя)
chown www-data:www-data catalog.json
chown -R www-data:www-data images/

echo "✅ Права доступа исправлены"
echo "📁 Статус файлов:"
ls -la catalog.json
ls -la images/ | head -5
