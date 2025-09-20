#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import time
import os

def check_python_processes():
    """Проверяем, есть ли запущенные процессы Python"""
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                              capture_output=True, text=True, shell=True)
        lines = result.stdout.strip().split('\n')
        # Считаем строки с python.exe (исключая заголовок)
        python_processes = [line for line in lines if 'python.exe' in line]
        return len(python_processes)
    except Exception as e:
        print(f"Ошибка при проверке процессов: {e}")
        return 0

def kill_python_processes():
    """Останавливаем все процессы Python"""
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                      capture_output=True, shell=True)
        print("✅ Все процессы Python остановлены")
        return True
    except Exception as e:
        print(f"Ошибка при остановке процессов: {e}")
        return False

def start_bot():
    """Запускаем бота"""
    try:
        print("🚀 Запуск бота DaryRei...")
        subprocess.run([sys.executable, 'bot.py'])
    except KeyboardInterrupt:
        print("\n⏹️ Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")

def main():
    """Основная функция"""
    print("=== БЕЗОПАСНЫЙ ЗАПУСК БОТА DARYREI ===")
    
    # Проверяем текущие процессы
    process_count = check_python_processes()
    print(f"📊 Найдено процессов Python: {process_count}")
    
    if process_count > 0:
        print("⚠️ Обнаружены запущенные процессы Python")
        print("🔄 Останавливаем все процессы...")
        
        if kill_python_processes():
            print("⏳ Ждем 3 секунды...")
            time.sleep(3)
        else:
            print("❌ Не удалось остановить процессы")
            return
    
    # Запускаем бота
    start_bot()

if __name__ == "__main__":
    main()

