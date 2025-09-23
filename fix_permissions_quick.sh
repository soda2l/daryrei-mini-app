#!/bin/bash

# Быстрое исправление прав доступа
echo "🔧 Быстрое исправление прав доступа..."

# Переходим в директорию бота
cd /var/www/daryrei_bot || cd /var/www/daryrei-bot

# Основные права
chmod 755 .
chmod 644 *.py
chmod 644 *.json
chmod 644 *.html
chmod 644 *.md

# Права на каталог изображений
chmod 755 images/
chmod 644 images/*

# Критически важные права
chmod 666 catalog.json
chmod +x bot.py

echo "✅ Права исправлены!"
echo "📋 Проверка:"
ls -la catalog.json
ls -la images/
