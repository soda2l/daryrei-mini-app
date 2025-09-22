#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диагностика проблем на сервере
"""

import json
import os
import requests
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
SERVER_API_URL = "https://daryreibot.duckdns.org/api/catalog"
LOCAL_CATALOG_FILE = "catalog.json"

def check_server_connectivity():
    """Проверить доступность сервера"""
    print("🔍 Проверка доступности сервера...")
    
    try:
        response = requests.get(SERVER_API_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Сервер доступен")
            return True
        else:
            print(f"❌ Сервер недоступен: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения к серверу: {e}")
        return False

def check_server_catalog():
    """Проверить каталог на сервере"""
    print("\n📦 Проверка каталога на сервере...")
    
    try:
        response = requests.get(SERVER_API_URL, timeout=10)
        if response.status_code == 200:
            catalog = response.json()
            products_count = len(catalog.get('products', []))
            categories_count = len(catalog.get('categories', []))
            
            print(f"✅ Каталог загружен с сервера:")
            print(f"   📦 Товаров: {products_count}")
            print(f"   📁 Категорий: {categories_count}")
            
            # Показываем первые несколько товаров
            if products_count > 0:
                print("\n📋 Первые товары:")
                for i, product in enumerate(catalog.get('products', [])[:3]):
                    print(f"   {i+1}. {product.get('name', 'Без названия')} - {product.get('price', 'Без цены')} ₽")
            
            return catalog
        else:
            print(f"❌ Ошибка загрузки каталога: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Ошибка при загрузке каталога: {e}")
        return None

def check_local_catalog():
    """Проверить локальный каталог"""
    print("\n💾 Проверка локального каталога...")
    
    try:
        if os.path.exists(LOCAL_CATALOG_FILE):
            with open(LOCAL_CATALOG_FILE, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
            
            products_count = len(catalog.get('products', []))
            categories_count = len(catalog.get('categories', []))
            
            print(f"✅ Локальный каталог найден:")
            print(f"   📦 Товаров: {products_count}")
            print(f"   📁 Категорий: {categories_count}")
            
            return catalog
        else:
            print("❌ Локальный каталог не найден")
            return None
    except Exception as e:
        print(f"❌ Ошибка при загрузке локального каталога: {e}")
        return None

def check_image_files():
    """Проверить файлы изображений"""
    print("\n🖼️ Проверка файлов изображений...")
    
    images_dir = "images"
    if os.path.exists(images_dir):
        image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        print(f"✅ Папка images найдена: {len(image_files)} файлов")
        
        if image_files:
            print("📋 Первые файлы:")
            for i, file in enumerate(image_files[:5]):
                print(f"   {i+1}. {file}")
        else:
            print("⚠️ В папке images нет изображений")
    else:
        print("❌ Папка images не найдена")

def check_catalog_consistency(local_catalog, server_catalog):
    """Проверить согласованность каталогов"""
    print("\n🔄 Проверка согласованности каталогов...")
    
    if not local_catalog or not server_catalog:
        print("⚠️ Не удалось сравнить каталоги")
        return
    
    local_products = {p['id']: p for p in local_catalog.get('products', [])}
    server_products = {p['id']: p for p in server_catalog.get('products', [])}
    
    local_only = set(local_products.keys()) - set(server_products.keys())
    server_only = set(server_products.keys()) - set(local_products.keys())
    
    if not local_only and not server_only:
        print("✅ Каталоги синхронизированы")
    else:
        print(f"⚠️ Найдены различия:")
        if local_only:
            print(f"   📱 Только в локальном: {len(local_only)} товаров")
        if server_only:
            print(f"   🌐 Только на сервере: {len(server_only)} товаров")

def main():
    """Главная функция"""
    print("🔍 Диагностика проблем на сервере")
    print("=" * 50)
    
    # Проверяем доступность сервера
    server_available = check_server_connectivity()
    
    # Проверяем каталог на сервере
    server_catalog = None
    if server_available:
        server_catalog = check_server_catalog()
    
    # Проверяем локальный каталог
    local_catalog = check_local_catalog()
    
    # Проверяем файлы изображений
    check_image_files()
    
    # Проверяем согласованность каталогов
    if local_catalog and server_catalog:
        check_catalog_consistency(local_catalog, server_catalog)
    
    print("\n📋 Рекомендации:")
    
    if not server_available:
        print("1. ❌ Сервер недоступен - проверьте интернет-соединение")
        print("2. 🔧 Проверьте, что бот запущен на сервере")
        print("3. 🌐 Проверьте URL сервера")
    
    if not local_catalog:
        print("1. 💾 Создайте локальный каталог")
        print("2. 🔄 Синхронизируйте с сервером")
    
    if local_catalog and server_catalog:
        local_only = set(p['id'] for p in local_catalog.get('products', [])) - set(p['id'] for p in server_catalog.get('products', []))
        if local_only:
            print("1. 🔄 Синхронизируйте локальные изменения с сервером")
            print("2. 📤 Скопируйте catalog.json на сервер")
    
    print("\n🚀 Следующие шаги:")
    print("1. Запустите sync_catalog.bat для синхронизации")
    print("2. Проверьте логи бота на сервере")
    print("3. Убедитесь, что права доступа настроены правильно")

if __name__ == "__main__":
    main()
