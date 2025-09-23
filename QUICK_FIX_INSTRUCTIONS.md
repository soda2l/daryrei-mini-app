# 🚀 Быстрое исправление бота на сервере Timeweb

## Проблема
```
ModuleNotFoundError: No module named 'telegram'
```

## Решение (выберите один из вариантов)

### Вариант 1: Автоматическое исправление (рекомендуется)

1. **Подключитесь к серверу:**
   ```bash
   ssh root@ваш-ip-адрес
   ```

2. **Выполните команды:**
   ```bash
   # Остановите бота
   systemctl stop daryrei-bot
   
   # Перейдите в директорию
   cd /var/www/daryrei-bot
   
   # Создайте виртуальное окружение
   python3 -m venv venv
   
   # Активируйте его
   source venv/bin/activate
   
   # Установите зависимости
   pip install python-telegram-bot==20.7 flask==3.0.0 flask-cors==4.0.0 requests==2.31.0 python-dotenv==1.0.0
   
   # Установите права
   chown -R www-data:www-data /var/www/daryrei-bot
   chmod -R 755 /var/www/daryrei-bot
   
   # Перезапустите бота
   systemctl start daryrei-bot
   
   # Проверьте статус
   systemctl status daryrei-bot
   ```

### Вариант 2: Использование скрипта

1. **Скачайте скрипт исправления на сервер:**
   ```bash
   wget https://raw.githubusercontent.com/ваш-репозиторий/daryrei_bot/main/fix_server_dependencies.sh
   chmod +x fix_server_dependencies.sh
   ./fix_server_dependencies.sh
   ```

### Вариант 3: Через Windows (если у вас есть доступ)

1. **Запустите скрипт `upload_fix_to_server.bat`** (предварительно отредактируйте IP адрес сервера)

## Проверка работы

### 1. Статус сервиса
```bash
systemctl status daryrei-bot
```

### 2. Логи
```bash
journalctl -u daryrei-bot -f
```

### 3. API
```bash
curl http://localhost:8000/api/health
```

## Если что-то пошло не так

### Переустановка зависимостей
```bash
cd /var/www/daryrei-bot
source venv/bin/activate
pip uninstall -y python-telegram-bot flask flask-cors requests python-dotenv
pip install python-telegram-bot==20.7 flask==3.0.0 flask-cors==4.0.0 requests==2.31.0 python-dotenv==1.0.0
```

### Проверка Python
```bash
python3 --version
which python3
```

### Проверка pip
```bash
pip --version
which pip
```

## Файлы для исправления

В репозитории созданы следующие файлы:
- `requirements.txt` - список зависимостей
- `fix_server_dependencies.sh` - скрипт автоматического исправления
- `daryrei-bot.service` - обновленная конфигурация systemd
- `upload_fix_to_server.bat` - скрипт для Windows

## После исправления

Бот должен:
1. ✅ Запускаться без ошибок
2. ✅ Отвечать на команды в Telegram
3. ✅ Обрабатывать заказы от мини-приложения
4. ✅ Работать API на порту 8000

## Мониторинг

Для постоянного мониторинга используйте:
```bash
# Просмотр логов в реальном времени
journalctl -u daryrei-bot -f

# Проверка статуса
systemctl status daryrei-bot

# Проверка портов
netstat -tlnp | grep :8000
```
