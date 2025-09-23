#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Определяем окружение
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Конфигурация для разных окружений
if ENVIRONMENT == 'production':
    # Продакшен настройки
    API_BASE_URL = "https://daryreibot.duckdns.org"
    IMAGES_BASE_URL = "https://daryreibot.duckdns.org"
    WEBAPP_URL = "https://soda2l.github.io/daryrei-mini-app/"
else:
    # Локальная разработка
    API_BASE_URL = "http://localhost:8000"
    IMAGES_BASE_URL = "http://localhost:8000"
    WEBAPP_URL = "http://localhost:8000"

# Экспортируем константы
API_CATALOG_URL = f"{API_BASE_URL}/api/catalog"
API_ORDER_URL = f"{API_BASE_URL}/api/order"
API_HEALTH_URL = f"{API_BASE_URL}/api/health"
IMAGES_URL = f"{IMAGES_BASE_URL}/images"
