# Исправление проблемы с зависимостями на сервере

## Проблема
```
ModuleNotFoundError: No module named 'telegram'
```

## Быстрое решение

### 1. Подключитесь к серверу
```bash
ssh root@ваш-ip-адрес
```

### 2. Запустите скрипт исправления
```bash
# Скачайте и запустите скрипт
wget https://raw.githubusercontent.com/ваш-репозиторий/daryrei_bot/main/fix_server_dependencies.sh
chmod +x fix_server_dependencies.sh
./fix_server_dependencies.sh
```

### 3. Или выполните команды вручную
```bash
# Остановите сервис
systemctl stop daryrei-bot

# Перейдите в директорию бота
cd /var/www/daryrei-bot

# Создайте виртуальное окружение
python3 -m venv venv

# Активируйте виртуальное окружение
source venv/bin/activate

# Установите зависимости
pip install python-telegram-bot==20.7
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install requests==2.31.0
pip install python-dotenv==1.0.0

# Проверьте установку
python3 -c "import telegram, flask, requests, dotenv; print('Все модули установлены успешно!')"

# Установите права
chown -R www-data:www-data /var/www/daryrei-bot
chmod -R 755 /var/www/daryrei-bot

# Перезапустите сервис
systemctl daemon-reload
systemctl start daryrei-bot

# Проверьте статус
systemctl status daryrei-bot
```

## Проверка работы

### 1. Проверьте статус сервиса
```bash
systemctl status daryrei-bot
```

### 2. Проверьте логи
```bash
journalctl -u daryrei-bot -f
```

### 3. Проверьте API
```bash
curl http://localhost:8000/api/health
```

## Если проблема не решена

### 1. Проверьте Python версию
```bash
python3 --version
# Должна быть 3.8 или выше
```

### 2. Проверьте pip
```bash
pip --version
```

### 3. Переустановите зависимости
```bash
cd /var/www/daryrei-bot
source venv/bin/activate
pip uninstall -y python-telegram-bot flask flask-cors requests python-dotenv
pip install -r requirements.txt
```

### 4. Проверьте права доступа
```bash
ls -la /var/www/daryrei-bot/
ls -la /var/www/daryrei-bot/venv/bin/
```

## Обновление systemd сервиса

Если нужно обновить конфигурацию сервиса:

```bash
# Остановите сервис
systemctl stop daryrei-bot

# Обновите файл сервиса
cp daryrei-bot.service /etc/systemd/system/

# Перезагрузите systemd
systemctl daemon-reload

# Запустите сервис
systemctl start daryrei-bot
systemctl enable daryrei-bot
```

## Мониторинг

### Просмотр логов в реальном времени
```bash
journalctl -u daryrei-bot -f
```

### Проверка портов
```bash
netstat -tlnp | grep :8000
```

### Проверка процессов
```bash
ps aux | grep bot.py
```
