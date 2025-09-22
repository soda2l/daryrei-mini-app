#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Обновляем bot.py на сервере - исправляем API endpoint для каталога
"""

import paramiko
import os

# Конфигурация сервера
SERVER_HOST = "daryreibot.duckdns.org"
SERVER_USER = "root"
SERVER_PATH = "/var/www/daryrei-bot/bot.py"

def update_server_bot():
    """Обновляем bot.py на сервере"""
    
    print("🔧 Подключаемся к серверу...")
    
    try:
        # Подключаемся к серверу
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SERVER_HOST, username=SERVER_USER)
        
        print("✅ Подключение установлено")
        
        # Читаем локальный bot.py
        with open('bot.py', 'r', encoding='utf-8') as f:
            local_content = f.read()
        
        print("📖 Локальный bot.py прочитан")
        
        # Создаем временный файл на сервере
        sftp = ssh.open_sftp()
        
        # Создаем резервную копию
        print("💾 Создаем резервную копию...")
        ssh.exec_command(f"cp {SERVER_PATH} {SERVER_PATH}.backup")
        
        # Записываем новый файл
        print("📝 Обновляем bot.py на сервере...")
        with sftp.open(SERVER_PATH, 'w') as remote_file:
            remote_file.write(local_content)
        
        print("✅ bot.py обновлен на сервере")
        
        # Перезапускаем бота
        print("🔄 Перезапускаем бота...")
        stdin, stdout, stderr = ssh.exec_command("systemctl restart daryrei-bot")
        
        # Ждем завершения
        stdout.channel.recv_exit_status()
        
        print("✅ Бот перезапущен")
        
        # Проверяем статус
        print("📊 Проверяем статус бота...")
        stdin, stdout, stderr = ssh.exec_command("systemctl status daryrei-bot --no-pager")
        status = stdout.read().decode('utf-8')
        print(status)
        
        sftp.close()
        ssh.close()
        
        print("🎉 Обновление завершено!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    update_server_bot()
