@echo off
echo Загрузка исправлений на сервер Timeweb...

REM Замените на ваш IP адрес сервера
set SERVER_IP=ваш-ip-адрес
set SERVER_USER=root

echo Копирование файлов на сервер...

REM Копируем requirements.txt
scp requirements.txt %SERVER_USER%@%SERVER_IP%:/var/www/daryrei-bot/

REM Копируем скрипт исправления
scp fix_server_dependencies.sh %SERVER_USER%@%SERVER_IP%:/var/www/daryrei-bot/

REM Копируем systemd сервис
scp daryrei-bot.service %SERVER_USER%@%SERVER_IP%:/var/www/daryrei-bot/

echo Подключение к серверу для выполнения исправлений...
ssh %SERVER_USER%@%SERVER_IP% "cd /var/www/daryrei-bot && chmod +x fix_server_dependencies.sh && ./fix_server_dependencies.sh"

echo Готово! Проверьте статус бота на сервере.
pause
