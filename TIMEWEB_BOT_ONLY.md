# Деплой бота на Timeweb (только ветка master)

## Текущая ситуация
- ✅ **Мини-приложение** - работает на GitHub Pages: `https://soda2l.github.io/daryrei-mini-app/`
- 🔄 **Бот** - нужно развернуть на Timeweb

## 1. Создание VPS на Timeweb

1. Войдите в панель управления Timeweb
2. Создайте новый VPS:
   - **ОС:** Ubuntu 20.04 или 22.04
   - **Тариф:** VPS Start (от 199₽/мес) или VPS Pro (от 399₽/мес)
   - **Регион:** Москва (для лучшей скорости)

## 2. Подключение к серверу

```bash
ssh root@ваш-ip-адрес
```

## 3. Обновление системы

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git python3.11 python3.11-pip python3.11-venv nginx -y
```

## 4. Клонирование репозитория

```bash
# Создайте папку для проекта
mkdir -p /var/www/daryrei-bot
cd /var/www/daryrei-bot

# Клонируйте только ветку master
git clone -b master https://github.com/soda2l/daryrei-mini-app.git .

# Проверьте, что файлы на месте
ls -la
```

## 5. Настройка Python окружения

```bash
# Создайте виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

## 6. Настройка переменных окружения

```bash
# Создайте файл .env
cat > .env << EOF
BOT_TOKEN=ваш_токен_бота_здесь
ORDER_GROUP_ID=-1003025937033
PORT=8000
EOF

# Установите права доступа
chmod 600 .env
```

## 7. Настройка автозапуска (systemd)

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
WorkingDirectory=/var/www/daryrei-bot
ExecStart=/var/www/daryrei-bot/venv/bin/python bot.py
Restart=always
RestartSec=10
Environment=PATH=/var/www/daryrei-bot/venv/bin

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

## 8. Настройка Nginx

```bash
# Создайте конфигурацию
sudo nano /etc/nginx/sites-available/daryrei-bot
```

Содержимое файла:
```nginx
server {
    listen 80;
    server_name ваш-домен.ru api.ваш-домен.ru;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Активация конфигурации:
```bash
sudo ln -s /etc/nginx/sites-available/daryrei-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 9. Настройка SSL (HTTPS)

```bash
# Установите Certbot
sudo apt install certbot python3-certbot-nginx -y

# Получите SSL сертификат
sudo certbot --nginx -d ваш-домен.ru -d api.ваш-домен.ru
```

## 10. Проверка работы

```bash
# Проверьте статус бота
sudo systemctl status daryrei-bot

# Проверьте логи
sudo journalctl -u daryrei-bot -f

# Проверьте API
curl http://localhost:8000/api/health
```

## 11. Обновление URL в мини-приложении (если нужно)

Если вы хотите использовать свой домен вместо Render:

1. Перейдите в ветку main
2. Обновите URL в `index.html`:
   ```javascript
   // Замените
   const response = await fetch('https://daryrei-bot.onrender.com/api/order', {
   
   // На
   const response = await fetch('https://api.ваш-домен.ru/api/order', {
   ```
3. Зафиксируйте изменения и отправьте в GitHub

## 12. Мониторинг и обслуживание

```bash
# Просмотр логов
sudo journalctl -u daryrei-bot -f

# Перезапуск бота
sudo systemctl restart daryrei-bot

# Обновление кода
cd /var/www/daryrei-bot
git pull origin master
sudo systemctl restart daryrei-bot
```

## Готово! 🎉

Теперь у вас есть:
- **Мини-приложение:** `https://soda2l.github.io/daryrei-mini-app/`
- **Бот API:** `https://api.ваш-домен.ru/api/health`

Бот будет автоматически запускаться при перезагрузке сервера и перезапускаться при сбоях.
