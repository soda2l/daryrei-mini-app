#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для синхронизации каталога между локальной и серверной версиями
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
LOCAL_CATALOG_FILE = "catalog.json"
SERVER_API_URL = "https://daryreibot.duckdns.org/api/catalog"

def load_local_catalog():
    """Загрузить локальный каталог"""
    try:
        if os.path.exists(LOCAL_CATALOG_FILE):
            with open(LOCAL_CATALOG_FILE, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
            logger.info(f"Локальный каталог загружен: {len(catalog.get('products', []))} товаров")
            return catalog
        else:
            logger.warning("Локальный каталог не найден")
            return None
    except Exception as e:
        logger.error(f"Ошибка при загрузке локального каталога: {e}")
        return None

def load_server_catalog():
    """Загрузить каталог с сервера"""
    try:
        response = requests.get(SERVER_API_URL, timeout=10)
        if response.status_code == 200:
            catalog = response.json()
            logger.info(f"Серверный каталог загружен: {len(catalog.get('products', []))} товаров")
            return catalog
        else:
            logger.error(f"Ошибка при загрузке серверного каталога: HTTP {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Ошибка при загрузке серверного каталога: {e}")
        return None

def compare_catalogs(local_catalog, server_catalog):
    """Сравнить каталоги"""
    if not local_catalog or not server_catalog:
        return None, None
    
    local_products = {p['id']: p for p in local_catalog.get('products', [])}
    server_products = {p['id']: p for p in server_catalog.get('products', [])}
    
    local_only = {k: v for k, v in local_products.items() if k not in server_products}
    server_only = {k: v for k, v in server_products.items() if k not in local_products}
    
    logger.info(f"Товары только в локальном каталоге: {len(local_only)}")
    logger.info(f"Товары только в серверном каталоге: {len(server_only)}")
    
    return local_only, server_only

def save_catalog(catalog, filename):
    """Сохранить каталог в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        logger.info(f"Каталог сохранен в {filename}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при сохранении каталога: {e}")
        return False

def sync_catalogs():
    """Синхронизировать каталоги"""
    print("🔄 Синхронизация каталогов...")
    
    # Загружаем каталоги
    local_catalog = load_local_catalog()
    server_catalog = load_server_catalog()
    
    if not local_catalog and not server_catalog:
        print("❌ Не удалось загрузить ни один каталог")
        return False
    
    if not local_catalog:
        print("⚠️ Локальный каталог не найден, используем серверный")
        return save_catalog(server_catalog, LOCAL_CATALOG_FILE)
    
    if not server_catalog:
        print("⚠️ Серверный каталог недоступен, используем локальный")
        return True
    
    # Сравниваем каталоги
    local_only, server_only = compare_catalogs(local_catalog, server_catalog)
    
    if not local_only and not server_only:
        print("✅ Каталоги синхронизированы")
        return True
    
    # Объединяем каталоги
    merged_catalog = local_catalog.copy()
    merged_products = {p['id']: p for p in merged_catalog.get('products', [])}
    
    # Добавляем товары с сервера, которых нет локально
    for product_id, product in server_only.items():
        merged_products[product_id] = product
        print(f"➕ Добавлен товар с сервера: {product.get('name', 'Без названия')}")
    
    merged_catalog['products'] = list(merged_products.values())
    
    # Сохраняем объединенный каталог
    if save_catalog(merged_catalog, LOCAL_CATALOG_FILE):
        print(f"✅ Каталоги синхронизированы: {len(merged_catalog.get('products', []))} товаров")
        return True
    else:
        print("❌ Ошибка при сохранении объединенного каталога")
        return False

def main():
    """Главная функция"""
    print("🚀 Скрипт синхронизации каталогов")
    print("=" * 50)
    
    success = sync_catalogs()
    
    if success:
        print("\n✅ Синхронизация завершена успешно!")
        print("\n📋 Что делать дальше:")
        print("1. Запустить бота локально: python bot.py")
        print("2. Проверить, что товары отображаются в мини-приложении")
        print("3. Если нужно, скопировать catalog.json на сервер")
    else:
        print("\n❌ Ошибка при синхронизации")
        print("\n🔧 Возможные решения:")
        print("1. Проверить интернет-соединение")
        print("2. Проверить доступность сервера")
        print("3. Проверить права доступа к файлам")

if __name__ == "__main__":
    main()
