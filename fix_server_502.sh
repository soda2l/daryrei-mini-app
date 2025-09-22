#!/bin/bash

# Скрипт для исправления ошибки 502 Bad Gateway

echo "🔧 Исправление ошибки 502 Bad Gateway..."
echo "================================================"

# Проверяем статус бота
echo "📊 Проверяем статус бота..."
sudo systemctl status daryrei-bot --no-pager

echo ""
echo "🔄 Перезапускаем бота..."
sudo systemctl restart daryrei-bot

echo ""
echo "⏳ Ждем 5 секунд..."
sleep 5

echo ""
echo "📊 Проверяем статус после перезапуска..."
sudo systemctl status daryrei-bot --no-pager

echo ""
echo "🔍 Проверяем логи бота..."
sudo journalctl -u daryrei-bot --since "2 minutes ago" --no-pager

echo ""
echo "🌐 Проверяем API локально..."
curl -s http://localhost:8000/api/catalog | head -c 100
echo ""

echo ""
echo "🌐 Проверяем API через nginx..."
curl -s https://daryreibot.duckdns.org/api/catalog | head -c 100
echo ""

echo ""
echo "✅ Готово! Проверьте результат выше."
echo ""
echo "📋 Если все еще есть проблемы:"
echo "1. Проверьте права доступа: sudo chown -R www-data:www-data /var/www/daryrei-bot/"
echo "2. Проверьте конфигурацию nginx: sudo nginx -t"
echo "3. Перезапустите nginx: sudo systemctl restart nginx"
