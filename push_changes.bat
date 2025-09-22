@echo off
set GIT_PAGER=
git add .
git commit -m "Добавлена система управления каталогом: исправлены цены, создана админ-панель, обновлен каталог товаров"
git push
pause
