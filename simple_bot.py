#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import os
from telegram import Bot
from telegram.error import TelegramError
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import threading
import time

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8121877943:AAEPprLrwI627XQd9Al7CQGTLvQtyopRKcE")

# ID группы для получения заказов
ORDER_GROUP_ID = "-1003025937033"

# Создаем Flask приложение
app = Flask(__name__)

# Создаем бота
bot = Bot(token=BOT_TOKEN)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка здоровья API"""
    return {"status": "ok", "message": "DaryRei Bot API is running"}

@app.route('/api/order', methods=['POST'])
def handle_order():
    """Обработка заказа от WebApp"""
    try:
        data = request.get_json()
        logger.info(f"=== ПОЛУЧЕН HTTP ЗАПРОС ЗАКАЗА ===")
        logger.info(f"Order data: {data}")
        
        if not data or not data.get('message'):
            return jsonify({"error": "Message is required"}), 400
        
        message = data.get('message', '')
        group_id = data.get('groupId', ORDER_GROUP_ID)
        
        logger.info(f"=== ОТПРАВКА ЗАКАЗА В ГРУППУ ===")
        logger.info(f"Message length: {len(message)}")
        logger.info(f"Group ID: {group_id}")
        
        # Отправляем сообщение в группу
        try:
            import asyncio
            
            async def send_message_async():
                return await bot.send_message(
                    chat_id=group_id,
                    text=message,
                    parse_mode='HTML'
                )
            
            # Запускаем асинхронную функцию
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            sent_message = loop.run_until_complete(send_message_async())
            
            logger.info(f"✅ Заказ успешно отправлен в группу {group_id}")
            logger.info(f"Sent message ID: {sent_message.message_id}")
            
            return jsonify({"status": "success", "message": "Order sent successfully"})
            
        except TelegramError as e:
            logger.error(f"❌ Ошибка при отправке в группу: {e}")
            return jsonify({"error": f"Failed to send to group: {str(e)}"}), 500
            
    except Exception as e:
        logger.error(f"Ошибка при обработке заказа: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info("Запуск простого бота DaryRei...")
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
