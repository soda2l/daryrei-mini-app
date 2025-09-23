#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Простой тест для проверки методов в классе DaryReiBot

import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from bot import DaryReiBot
    
    # Создаем экземпляр бота
    print("Создаем экземпляр DaryReiBot...")
    bot = DaryReiBot()
    
    # Проверяем наличие метода start_command
    if hasattr(bot, 'start_command'):
        print("✅ Метод start_command найден!")
        print(f"Тип метода: {type(bot.start_command)}")
    else:
        print("❌ Метод start_command НЕ найден!")
        
    # Выводим все методы класса
    print("\nВсе методы класса DaryReiBot:")
    methods = [method for method in dir(bot) if not method.startswith('_')]
    for method in sorted(methods):
        print(f"  - {method}")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
