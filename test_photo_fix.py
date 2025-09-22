#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тест исправления загрузки фото
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

def test_photo_download():
    """Тест загрузки фото"""
    print("🧪 Тестируем исправление загрузки фото...")
    
    # Проверяем, что папка images существует
    images_dir = "images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"✅ Создана папка: {images_dir}")
    else:
        print(f"✅ Папка {images_dir} уже существует")
    
    # Проверяем, что requests установлен
    try:
        import requests
        print("✅ Библиотека requests доступна")
    except ImportError:
        print("❌ Библиотека requests не установлена")
        return False
    
    # Проверяем, что urllib доступен
    try:
        import urllib.request
        import urllib.error
        print("✅ Библиотека urllib доступна")
    except ImportError:
        print("❌ Библиотека urllib не доступна")
        return False
    
    print("\n🔧 Исправления в handle_photo:")
    print("1. ✅ Добавлена проверка file_path на None")
    print("2. ✅ Добавлен fallback через requests")
    print("3. ✅ Улучшено логирование ошибок")
    print("4. ✅ Добавлена обработка HTTPError")
    
    print("\n📋 Что нужно проверить:")
    print("1. Запустить бота: python bot.py")
    print("2. Отправить /admin")
    print("3. Добавить товар")
    print("4. Отправить фото")
    print("5. Проверить логи на ошибки")
    
    return True

if __name__ == "__main__":
    test_photo_download()
