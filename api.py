from flask import Flask, request, jsonify
from telegram import Bot
import asyncio
import logging

app = Flask(__name__)
bot = Bot(token="8121877943:AAEPprLrwI627XQd9Al7CQGTLvQtyopRKcE")
ORDER_GROUP_ID = "-1003025937033"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/order', methods=['POST'])
def handle_order():
    try:
        data = request.get_json()
        message = data.get('message', '')
        group_id = data.get('groupId', ORDER_GROUP_ID)
        
        logger.info(f"Получен заказ: {message[:50]}...")
        
        # Отправляем в группу
        async def send_message():
            return await bot.send_message(
                chat_id=group_id,
                text=message,
                parse_mode='HTML'
            )
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        sent_message = loop.run_until_complete(send_message())
        loop.close()
        
        logger.info(f"✅ Заказ отправлен! ID: {sent_message.message_id}")
        return jsonify({"status": "success", "message": "Order sent successfully"})
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
