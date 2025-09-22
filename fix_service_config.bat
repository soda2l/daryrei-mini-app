@echo off
echo Копируем скрипт исправления на сервер...
scp fix_service_config.sh root@147.45.164.202:/tmp/
echo Выполняем исправление на сервере...
ssh root@147.45.164.202 "chmod +x /tmp/fix_service_config.sh && /tmp/fix_service_config.sh"
echo Готово!
pause
