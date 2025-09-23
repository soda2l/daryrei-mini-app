#!/bin/bash

# Скрипт для установки зависимостей на сервере Timeweb
# Запускать от имени root или с sudo

echo "🔧 Установка зависимостей для DaryRei Bot..."

# Обновляем систему
echo "📦 Обновление системы..."
apt update && apt upgrade -y

# Устанавливаем Python и pip если не установлены
echo "🐍 Установка Python и pip..."
apt install -y python3 python3-pip python3-venv

# Создаем виртуальное окружение
echo "🌐 Создание виртуального окружения..."
cd /var/www/daryrei-bot
python3 -m venv venv

# Активируем виртуальное окружение
echo "⚡ Активация виртуального окружения..."
source venv/bin/activate

# Обновляем pip
echo "📈 Обновление pip..."
pip install --upgrade pip

# Устанавливаем зависимости из requirements.txt
echo "📚 Установка зависимостей..."
pip install -r requirements.txt

# Проверяем установку
echo "✅ Проверка установки..."
python3 -c "import telegram, flask, requests, dotenv; print('Все модули установлены успешно!')"

# Устанавливаем права на файлы
echo "🔐 Установка прав доступа..."
chown -R www-data:www-data /var/www/daryrei-bot
chmod -R 755 /var/www/daryrei-bot

echo "🎉 Установка завершена!"
echo "Теперь перезапустите сервис: systemctl restart daryrei-bot"
