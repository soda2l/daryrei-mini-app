import requests
import json

# Тестируем локальный API
url = "http://localhost:8000/api/order"
data = {
    "message": "🧪 ТЕСТ ЗАКАЗА\n\n👤 Покупатель: @test_user\n\n📦 Товары:\n• Тестовая свеча - 1 шт. × 1000 ₽ = 1000 ₽\n\n💰 Итого: 1000 ₽\n🚚 Доставка: 300 ₽\n\n📅 Дата: Тест",
    "groupId": "-1003025937033"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
