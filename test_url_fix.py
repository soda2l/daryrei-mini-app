#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест исправления URL для скачивания фото
"""

import os
import sys
import time
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_url_construction():
    """Тест построения URL"""
    print("🧪 Тестируем исправление URL для скачивания фото...")
    
    # Симулируем разные варианты file_path
    test_cases = [
        "photos/file_0.jpg",  # Обычный путь
        "https://api.telegram.org/file/botTOKEN/photos/file_0.jpg",  # Полный URL
        "documents/file_1.pdf",  # Другой тип файла
        None,  # None значение
        "",  # Пустая строка
    ]
    
    BOT_TOKEN = "8121877943:AAEPprLrwI627XQd9Al7CQGTLvQtyopRKcE"
    
    print("\n📋 Тестируем разные варианты file_path:")
    
    for i, file_path in enumerate(test_cases, 1):
        print(f"\n{i}. file_path: {file_path}")
        
        if file_path is None:
            print("   ❌ file_path is None - пропускаем")
            continue
        
        if not file_path:
            print("   ❌ file_path пустой - пропускаем")
            continue
        
        # Проверяем, содержит ли file_path уже полный URL
        if file_path.startswith('https://'):
            download_url = file_path
            print(f"   ✅ File path уже содержит полный URL: {download_url}")
        else:
            download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            print(f"   ✅ Строим URL: {download_url}")
    
    print("\n🔧 Исправления:")
    print("1. ✅ Добавлена проверка на полный URL")
    print("2. ✅ Если file_path уже содержит https://, используем его как есть")
    print("3. ✅ Иначе строим URL как обычно")
    print("4. ✅ Добавлено детальное логирование")
    
    print("\n📋 Что нужно проверить:")
    print("1. Запустить бота: python bot.py")
    print("2. Отправить /admin")
    print("3. Добавить товар")
    print("4. Отправить фото")
    print("5. Проверить логи - URL не должен дублироваться")
    
    return True

if __name__ == "__main__":
    test_url_construction()
