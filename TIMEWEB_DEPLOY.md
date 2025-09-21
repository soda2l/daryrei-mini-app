# Деплой на Timeweb

## Структура проекта

- **main** - мини-приложение (index.html + images)
- **master** - бот (bot.py + API)

## 1. Деплой мини-приложения

### Вариант 1: Статический хостинг
1. Войдите в панель управления Timeweb
2. Создайте новый сайт → "Статический сайт"
3. Загрузите файлы из ветки `main`:
   - `index.html`
   - папка `images/`
4. Привяжите домен
5. URL: `https://ваш-домен.ru/`

### Вариант 2: VPS + Nginx
1. Создайте VPS на Timeweb
2. Установите Nginx:
   ```bash
   sudo apt update
   sudo apt install nginx
   ```
3. Настройте Nginx для статических файлов:
   ```nginx
   server {
       listen 80;
       server_name ваш-домен.ru;
       root /var/www/daryrei;
       index index.html;
       
       location / {
           try_files $uri $uri/ =404;
       }
   }
   ```
4. Загрузите файлы в `/var/www/daryrei/`
5. Перезапустите Nginx: `sudo systemctl restart nginx`

## 2. Деплой бота

### Настройка VPS
1. Создайте VPS на Timeweb (рекомендуется Ubuntu 20.04+)
2. Подключитесь по SSH
3. Обновите систему:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

### Установка Python и зависимостей
```bash
# Установите Python 3.11
sudo apt install python3.11 python3.11-pip python3.11-venv

# Создайте виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### Настройка переменных окружения
```bash
# Создайте файл .env
cat > .env << EOF
BOT_TOKEN=ваш_токен_бота
ORDER_GROUP_ID=-1003025937033
PORT=8000
EOF
```

### Настройка автозапуска (systemd)
```bash
# Создайте сервис
sudo nano /etc/systemd/system/daryrei-bot.service
```

Содержимое файла:
```ini
[Unit]
Description=DaryRei Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/username/daryrei-bot
ExecStart=/home/username/daryrei-bot/venv/bin/python bot.py
Restart=always
Environment=PATH=/home/username/daryrei-bot/venv/bin

[Install]
WantedBy=multi-user.target
```

Активация сервиса:
```bash
sudo systemctl daemon-reload
sudo systemctl enable daryrei-bot
sudo systemctl start daryrei-bot
sudo systemctl status daryrei-bot
```

### Настройка Nginx для API
```nginx
server {
    listen 80;
    server_name api.ваш-домен.ru;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 3. Обновление URL в мини-приложении

Если бот развернут на Timeweb, обновите URL в `index.html`:

```javascript
// Замените
const response = await fetch('https://daryrei-bot.onrender.com/api/order', {

// На
const response = await fetch('https://api.ваш-домен.ru/api/order', {
```

## 4. Настройка SSL (HTTPS)

### Для статического сайта:
- Включите SSL в панели Timeweb
- Или используйте Let's Encrypt

### Для VPS:
```bash
# Установите Certbot
sudo apt install certbot python3-certbot-nginx

# Получите сертификат
sudo certbot --nginx -d ваш-домен.ru -d api.ваш-домен.ru
```

## 5. Проверка работы

1. **Мини-приложение:** `https://ваш-домен.ru/`
2. **API бота:** `https://api.ваш-домен.ru/api/health`
3. **Тест заказа:** Через бота в Telegram

## 6. Мониторинг

```bash
# Проверка статуса бота
sudo systemctl status daryrei-bot

# Просмотр логов
sudo journalctl -u daryrei-bot -f

# Проверка портов
sudo netstat -tlnp | grep :8000
```

## 7. Обновление

```bash
# Остановите бота
sudo systemctl stop daryrei-bot

# Обновите код
git pull origin master

# Перезапустите бота
sudo systemctl start daryrei-bot
```

## Рекомендуемые тарифы Timeweb

- **Мини-приложение:** Статический хостинг (от 99₽/мес)
- **Бот:** VPS Start (от 199₽/мес) или VPS Pro (от 399₽/мес)
