#!/bin/bash

# Скрипт для исправления прав доступа на сервере

echo "🔧 Исправление прав доступа на сервере..."
echo "================================================"

# Переходим в папку бота
cd /var/www/daryrei-bot

echo "📁 Текущая папка: $(pwd)"
echo "👤 Текущий пользователь: $(whoami)"

# Проверяем права доступа
echo ""
echo "🔍 Проверяем текущие права доступа:"
ls -la

echo ""
echo "🔧 Исправляем права доступа..."

# Делаем владельцем папки пользователя www-data
echo "1. Устанавливаем владельца папки..."
sudo chown -R www-data:www-data /var/www/daryrei-bot/

# Даем права на чтение и запись
echo "2. Устанавливаем права на папку..."
sudo chmod -R 755 /var/www/daryrei-bot/

# Особые права для файла каталога
echo "3. Устанавливаем права на файл каталога..."
sudo chmod 666 /var/www/daryrei-bot/catalog.json

# Создаем папку для изображений если её нет
echo "4. Создаем папку для изображений..."
sudo mkdir -p /var/www/daryrei-bot/images
sudo chmod 755 /var/www/daryrei-bot/images
sudo chown www-data:www-data /var/www/daryrei-bot/images

echo ""
echo "✅ Права доступа исправлены!"

# Проверяем результат
echo ""
echo "🔍 Проверяем результат:"
echo "Файл каталога:"
ls -la /var/www/daryrei-bot/catalog.json

echo ""
echo "Папка изображений:"
ls -la /var/www/daryrei-bot/images/

echo ""
echo "🔄 Перезапускаем бота..."
sudo systemctl restart daryrei-bot

echo ""
echo "📊 Статус бота:"
sudo systemctl status daryrei-bot --no-pager

echo ""
echo "✅ Готово! Проверьте логи бота:"
echo "sudo journalctl -u daryrei-bot -f"
