#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Проверяем конфигурацию systemd сервиса
"""

import paramiko

def check_service_config():
    """Проверяем конфигурацию сервиса"""
    
    print("🔍 Проверяем конфигурацию systemd сервиса...")
    
    try:
        # Подключаемся к серверу
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("147.45.164.202", username="root")
        
        print("✅ Подключение установлено")
        
        # Проверяем конфигурацию сервиса
        print("\n📋 Конфигурация сервиса:")
        stdin, stdout, stderr = ssh.exec_command("cat /etc/systemd/system/daryrei-bot.service")
        service_config = stdout.read().decode('utf-8')
        print(service_config)
        
        # Проверяем права доступа к файлу
        print("\n🔐 Права доступа к bot.py:")
        stdin, stdout, stderr = ssh.exec_command("ls -la /var/www/daryrei-bot/bot.py")
        permissions = stdout.read().decode('utf-8')
        print(permissions)
        
        # Проверяем, существует ли Python
        print("\n🐍 Проверка Python:")
        stdin, stdout, stderr = ssh.exec_command("which python3")
        python_path = stdout.read().decode('utf-8').strip()
        print(f"Python3 path: {python_path}")
        
        # Проверяем, может ли systemd запустить Python
        print("\n🧪 Тест запуска Python:")
        stdin, stdout, stderr = ssh.exec_command("cd /var/www/daryrei-bot && python3 --version")
        python_version = stdout.read().decode('utf-8')
        python_error = stderr.read().decode('utf-8')
        print(f"Version: {python_version}")
        if python_error:
            print(f"Error: {python_error}")
        
        # Проверяем, может ли Python импортировать модули
        print("\n📦 Тест импорта модулей:")
        stdin, stdout, stderr = ssh.exec_command("cd /var/www/daryrei-bot && python3 -c 'import sys; print(sys.path)'")
        sys_path = stdout.read().decode('utf-8')
        print(f"Python path: {sys_path}")
        
        ssh.close()
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    check_service_config()
