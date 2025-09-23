#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Простой тест для проверки синтаксиса

try:
    import bot
    print("✅ Модуль bot импортирован успешно")
    
    # Проверяем класс
    if hasattr(bot, 'DaryReiBot'):
        print("✅ Класс DaryReiBot найден")
        
        # Проверяем методы класса
        methods = [method for method in dir(bot.DaryReiBot) if not method.startswith('_')]
        print(f"Методы класса: {methods}")
        
        if 'start_command' in methods:
            print("✅ Метод start_command найден в классе")
        else:
            print("❌ Метод start_command НЕ найден в классе")
    else:
        print("❌ Класс DaryReiBot НЕ найден")
        
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
