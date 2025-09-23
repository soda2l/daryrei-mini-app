#!/bin/bash

# Скрипт для настройки прав доступа на сервере
# Запускать от имени root или с sudo

echo "🔧 Настройка прав доступа для бота DaryRei..."

# Переходим в директорию бота
cd /var/www/daryrei_bot || cd /var/www/daryrei-bot

# Устанавливаем владельца (замените username на ваше имя пользователя)
# chown -R www-data:www-data /var/www/daryrei_bot
# Или если используете другого пользователя:
# chown -R $USER:$USER /var/www/daryrei_bot

# Устанавливаем права на директории
echo "📁 Настройка прав на директории..."
find /var/www/daryrei_bot -type d -exec chmod 755 {} \;

# Устанавливаем права на файлы
echo "📄 Настройка прав на файлы..."
find /var/www/daryrei_bot -type f -exec chmod 644 {} \;

# Особые права для исполняемых файлов
echo "⚙️ Настройка прав на исполняемые файлы..."
chmod +x /var/www/daryrei_bot/bot.py
chmod +x /var/www/daryrei_bot/setup_permissions.sh

# Права на каталог изображений
echo "🖼️ Настройка прав на каталог изображений..."
chmod 755 /var/www/daryrei_bot/images
find /var/www/daryrei_bot/images -type f -exec chmod 644 {} \;

# Права на файл каталога (должен быть доступен для записи)
echo "📋 Настройка прав на файл каталога..."
chmod 666 /var/www/daryrei_bot/catalog.json

# Права на логи (если есть)
echo "📝 Настройка прав на логи..."
touch /var/www/daryrei_bot/bot.log 2>/dev/null || true
chmod 666 /var/www/daryrei_bot/bot.log 2>/dev/null || true

# Проверяем права
echo "✅ Проверка прав доступа..."
ls -la /var/www/daryrei_bot/

echo ""
echo "🎉 Настройка прав завершена!"
echo ""
echo "📋 Проверьте следующее:"
echo "1. Файл catalog.json должен иметь права 666"
echo "2. Директория images должна иметь права 755"
echo "3. Все Python файлы должны иметь права 644"
echo "4. bot.py должен быть исполняемым (755)"
echo ""
echo "🚀 Теперь можно запускать бота!"
