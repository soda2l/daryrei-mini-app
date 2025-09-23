#!/bin/bash

# Быстрое исправление проблемы с зависимостями на сервере
# Запускать от имени root

echo "🚀 Быстрое исправление DaryRei Bot..."

# Останавливаем сервис
echo "⏹️ Остановка сервиса..."
systemctl stop daryrei-bot

# Переходим в директорию бота
cd /var/www/daryrei-bot

# Создаем виртуальное окружение если не существует
if [ ! -d "venv" ]; then
    echo "🌐 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
echo "⚡ Активация виртуального окружения..."
source venv/bin/activate

# Устанавливаем зависимости
echo "📚 Установка зависимостей..."
pip install python-telegram-bot==20.7
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install requests==2.31.0
pip install python-dotenv==1.0.0

# Проверяем установку
echo "✅ Проверка установки..."
python3 -c "import telegram, flask, requests, dotenv; print('Все модули установлены успешно!')"

if [ $? -eq 0 ]; then
    echo "✅ Зависимости установлены успешно!"
    
    # Устанавливаем права
    chown -R www-data:www-data /var/www/daryrei-bot
    chmod -R 755 /var/www/daryrei-bot
    
    # Перезапускаем сервис
    echo "🔄 Перезапуск сервиса..."
    systemctl daemon-reload
    systemctl start daryrei-bot
    
    # Проверяем статус
    echo "📊 Статус сервиса:"
    systemctl status daryrei-bot --no-pager
    
    echo "🎉 Исправление завершено!"
    echo "Проверьте логи: journalctl -u daryrei-bot -f"
else
    echo "❌ Ошибка при установке зависимостей!"
    exit 1
fi
