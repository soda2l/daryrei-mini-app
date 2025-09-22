@echo off
echo Копируем скрипт исправления прав на сервер...
scp fix_permissions_again.sh root@daryreibot.duckdns.org:/tmp/
echo Выполняем исправление прав на сервере...
ssh root@daryreibot.duckdns.org "chmod +x /tmp/fix_permissions_again.sh && /tmp/fix_permissions_again.sh"
echo Готово!
pause
