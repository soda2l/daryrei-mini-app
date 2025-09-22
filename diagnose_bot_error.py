#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диагностика ошибки запуска бота
"""

import paramiko

def diagnose_bot_error():
    """Диагностируем ошибку запуска бота"""
    
    print("🔍 Диагностируем ошибку запуска бота...")
    
    try:
        # Подключаемся к серверу
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("147.45.164.202", username="root")
        
        print("✅ Подключение установлено")
        
        # Проверяем статус сервиса
        print("\n📊 Статус сервиса:")
        stdin, stdout, stderr = ssh.exec_command("systemctl status daryrei-bot.service --no-pager")
        status = stdout.read().decode('utf-8')
        print(status)
        
        # Проверяем логи
        print("\n📋 Последние логи:")
        stdin, stdout, stderr = ssh.exec_command("journalctl -xeu daryrei-bot.service --no-pager -n 20")
        logs = stdout.read().decode('utf-8')
        print(logs)
        
        # Проверяем права доступа
        print("\n🔐 Права доступа:")
        stdin, stdout, stderr = ssh.exec_command("ls -la /var/www/daryrei-bot/")
        permissions = stdout.read().decode('utf-8')
        print(permissions)
        
        # Проверяем синтаксис Python
        print("\n🐍 Проверка синтаксиса Python:")
        stdin, stdout, stderr = ssh.exec_command("cd /var/www/daryrei-bot && python3 -m py_compile bot.py")
        compile_result = stdout.read().decode('utf-8')
        compile_error = stderr.read().decode('utf-8')
        
        if compile_error:
            print(f"❌ Ошибка синтаксиса: {compile_error}")
        else:
            print("✅ Синтаксис Python корректен")
        
        # Проверяем зависимости
        print("\n📦 Проверка зависимостей:")
        stdin, stdout, stderr = ssh.exec_command("cd /var/www/daryrei-bot && python3 -c 'import telegram, flask, requests'")
        deps_result = stdout.read().decode('utf-8')
        deps_error = stderr.read().decode('utf-8')
        
        if deps_error:
            print(f"❌ Ошибка зависимостей: {deps_error}")
        else:
            print("✅ Зависимости установлены")
        
        ssh.close()
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    diagnose_bot_error()
