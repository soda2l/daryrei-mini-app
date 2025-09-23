#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
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
ORDER_GROUP_ID = os.getenv("ORDER_GROUP_ID", "-1003025937033")

# ID админов (доступ к админ-панели)
ADMIN_IDS = [1852800505, 5308921954]

# Путь к файлу каталога
CATALOG_FILE = "catalog.json"

# Создаем Flask приложение для API
flask_app = Flask(__name__)
CORS(flask_app)

class DaryReiBot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
        self.setup_error_handlers()
        self.setup_flask_api()
        
        # Запускаем Flask API в отдельном потоке
        self.flask_thread = threading.Thread(target=self.run_flask, daemon=True)
        self.flask_thread.start()
        
        # Инициализируем каталог
        self.init_catalog()
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("catalog", self.catalog_command))
        self.application.add_handler(CommandHandler("test", self.test_command))
        self.application.add_handler(CommandHandler("debug", self.debug_command))
        self.application.add_handler(CommandHandler("webapp", self.webapp_test_command))
        # self.application.add_handler(CommandHandler("testwebapp", self.test_webapp_data_command))
        
        # Админские команды
        self.application.add_handler(CommandHandler("admin", self.admin_command))
        self.application.add_handler(CommandHandler("add_product", self.add_product_command))
        self.application.add_handler(CommandHandler("delete_product", self.delete_product_command))
        self.application.add_handler(CommandHandler("add_category", self.add_category_command))
        self.application.add_handler(CommandHandler("delete_category", self.delete_category_command))
        self.application.add_handler(CommandHandler("list_products", self.list_products_command))
        self.application.add_handler(CommandHandler("list_categories", self.list_categories_command))
        self.application.add_handler(CommandHandler("reset", self.reset_command))
        self.application.add_handler(CommandHandler("update_catalog", self.update_catalog_command))
        self.application.add_handler(CommandHandler("delete_product_by_category", self.delete_product_by_category_command))
        
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Обработчик для данных от WebApp (приоритетный)
        self.application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, self.handle_web_app_data))
        
        # Обработчик для фото
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        
        # Обработчик для всех текстовых сообщений (на случай если WebApp не работает)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
        
        # Универсальный обработчик для всех сообщений (для отладки) - последний
        # self.application.add_handler(MessageHandler(filters.ALL, self.handle_all_messages))
    
    def setup_error_handlers(self):
        """Настройка обработчиков ошибок"""
        self.application.add_error_handler(self.error_handler)
    
    def setup_flask_api(self):
        """Настройка Flask API для заказов"""
        
        @flask_app.route('/api/order', methods=['POST', 'OPTIONS'])
        def handle_order():
            # Обработка CORS preflight запросов
            if request.method == 'OPTIONS':
                response = jsonify({"status": "ok"})
                response.headers.add('Access-Control-Allow-Origin', '*')
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
                return response
            
            try:
                data = request.get_json()
                logger.info(f"Получен заказ через API: {json.dumps(data, ensure_ascii=False)}")
                
                message = data.get('message', '')
                group_id = data.get('groupId', ORDER_GROUP_ID)
                
                if not message:
                    logger.error("Пустое сообщение в заказе")
                    return jsonify({"error": "Message is required"}), 400
                
                logger.info(f"Отправляем заказ в группу {group_id}...")
                logger.info(f"Длина сообщения: {len(message)}")
                
                # Отправляем через HTTP API Telegram (простой способ)
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                payload = {
                    'chat_id': group_id,
                    'text': message,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✅ Заказ отправлен! Message ID: {result.get('result', {}).get('message_id')}")
                    
                    response = jsonify({"status": "success", "message": "Order sent successfully"})
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
                else:
                    logger.error(f"❌ Ошибка отправки: {response.status_code} - {response.text}")
                    response = jsonify({"error": f"Failed to send: {response.text}"})
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response, 500
                
            except Exception as e:
                logger.error(f"❌ Ошибка при обработке заказа: {e}")
                logger.error(f"Тип ошибки: {type(e)}")
                response = jsonify({"error": str(e)})
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response, 500
        
        @flask_app.route('/api/health', methods=['GET'])
        def health():
            response = jsonify({
                "status": "ok", 
                "message": "DaryRei Bot API is running",
                "bot_token": BOT_TOKEN[:10] + "..." if BOT_TOKEN else "not_set",
                "group_id": ORDER_GROUP_ID
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        @flask_app.route('/api/catalog', methods=['GET'])
        def get_catalog():
            """API для получения каталога товаров"""
            try:
                # Используем каталог из памяти бота (актуальная версия)
                catalog = self.get_catalog()
                
                response = jsonify(catalog)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            except Exception as e:
                logger.error(f"Ошибка при получении каталога: {e}")
                response = jsonify({"error": str(e)})
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response, 500
        
        @flask_app.route('/images/<path:filename>')
        def serve_image(filename):
            """Сервер для статических изображений"""
            try:
                return send_from_directory('images', filename)
            except FileNotFoundError:
                return "Image not found", 404
    
    def run_flask(self):
        """Запуск Flask API в отдельном потоке"""
        logger.info("Запускаем Flask API на порту 8000...")
        flask_app.run(host="0.0.0.0", port=8000, debug=False)
    
    def init_catalog(self):
        """Инициализация каталога"""
        try:
            if os.path.exists(CATALOG_FILE):
                with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
                    self.catalog = json.load(f)
                logger.info("Каталог загружен из файла")
            else:
                # Создаем базовый каталог
                self.catalog = {
                    "categories": [],
                    "products": []
                }
                self.save_catalog()
                logger.info("Создан новый каталог")
        except Exception as e:
            logger.error(f"Ошибка при инициализации каталога: {e}")
            self.catalog = {"categories": [], "products": []}
    
    def save_catalog(self):
        """Сохранение каталога в файл"""
        try:
            with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.catalog, f, ensure_ascii=False, indent=2)
            logger.info("Каталог сохранен")
        except Exception as e:
            logger.error(f"Ошибка при сохранении каталога: {e}")
    
    def is_admin(self, user_id):
        """Проверка, является ли пользователь админом"""
        return user_id in ADMIN_IDS
    
    def get_catalog(self):
        """Получить каталог"""
        return self.catalog
    
    def add_category(self, category_id, name, description=""):
        """Добавить категорию"""
        category = {
            "id": category_id,
            "name": name,
            "description": description
        }
        self.catalog["categories"].append(category)
        self.save_catalog()
        return True
    
    def delete_category(self, category_id):
        """Удалить категорию"""
        self.catalog["categories"] = [cat for cat in self.catalog["categories"] if cat["id"] != category_id]
        # Также удаляем все товары из этой категории
        self.catalog["products"] = [prod for prod in self.catalog["products"] if prod["category"] != category_id]
        self.save_catalog()
        return True
    
    def add_product(self, product_id, name, description, price, category_id, images, available=True):
        """Добавить товар"""
        product = {
            "id": product_id,
            "name": name,
            "description": description,
            "price": price,
            "category": category_id,
            "images": images,
            "available": available
        }
        self.catalog["products"].append(product)
        self.save_catalog()
        return True
    
    def delete_product(self, product_id):
        """Удалить товар"""
        self.catalog["products"] = [prod for prod in self.catalog["products"] if prod["id"] != product_id]
        self.save_catalog()
        return True
    
    def update_product(self, product_id, **kwargs):
        """Обновить товар"""
        for product in self.catalog["products"]:
            if product["id"] == product_id:
                product.update(kwargs)
                self.save_catalog()
                return True
        return False
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_text = """🕯 Магазин авторских свечей DaryRei

✨ Уют, аромат и тепло в каждой свече.

Нажмите Старт, чтобы начать работу 🔥"""
        
        keyboard = [
            [InlineKeyboardButton("🚀 Начать покупки", callback_data="start_shopping")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        user_id = update.effective_user.id
        
        help_text = """Доступные команды:
/start - Начать работу с ботом
/help - Показать эту справку
/catalog - Открыть каталог товаров
/test - Тест отправки в группу
/webapp - Тест WebApp
/testwebapp - Тест обработки WebApp данных
/debug - Отправить тестовый заказ"""
        
        # Добавляем админские команды если пользователь админ
        if self.is_admin(user_id):
            help_text += """

🛠️ Админские команды:
/admin - Админ-панель
/add_product - Добавить товар
/delete_product - Удалить товар
/delete_product_by_category - Удалить товары по категории
/add_category - Добавить категорию
/delete_category - Удалить категорию
/list_products - Показать все товары
/list_categories - Показать все категории
/update_catalog - Обновить каталог"""
        
        await update.message.reply_text(help_text)
    
    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Тестовая команда для проверки отправки в группу"""
        try:
            test_message = "🧪 ТЕСТ: Проверка отправки сообщений в группу"
            await context.bot.send_message(
                chat_id=ORDER_GROUP_ID,
                text=test_message
            )
            await update.message.reply_text(f"✅ Тестовое сообщение отправлено в группу {ORDER_GROUP_ID}")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при отправке тестового сообщения: {str(e)}")
            logger.error(f"Ошибка тестовой отправки: {e}")
    
    async def debug_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда для отладки - отправляет тестовый заказ"""
        try:
            test_order = """🛒 НОВЫЙ ЗАКАЗ

👤 Покупатель: @test_user

📦 Товары:
• Тестовая свеча - 1 шт. × 1000 ₽ = 1000 ₽

💰 Итого: 1000 ₽

📅 Дата: Тестовый заказ"""
            
            await context.bot.send_message(
                chat_id=ORDER_GROUP_ID,
                text=test_order,
                parse_mode='HTML'
            )
            await update.message.reply_text("✅ Тестовый заказ отправлен в группу")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {str(e)}")
            logger.error(f"Ошибка debug команды: {e}")
    
    async def webapp_test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Тестовая команда для проверки WebApp"""
        keyboard = [
            [InlineKeyboardButton("🧪 Тест WebApp", web_app=WebAppInfo(url="https://soda2l.github.io/daryrei-mini-app/"))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Нажмите кнопку для тестирования WebApp. Если WebApp работает, вы увидите мини-приложение.",
            reply_markup=reply_markup
        )
    
    async def catalog_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /catalog"""
        await self.show_main_menu(update, context)
    
    # ========== АДМИНСКИЕ КОМАНДЫ ==========
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Главная админ-панель"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав доступа к админ-панели")
            return
        
        text = """🛠️ <b>АДМИН-ПАНЕЛЬ</b>
━━━━━━━━━━━━━━━━━━━━━━━━

📦 <b>Управление товарами:</b>
• /add_product - Добавить товар
• /delete_product - Удалить товар
• /list_products - Показать все товары

📁 <b>Управление категориями:</b>
• /add_category - Добавить категорию
• /delete_category - Удалить категорию
• /list_categories - Показать все категории

🔧 <b>Утилиты:</b>
• /reset - Сбросить состояния

📊 <b>Статистика:</b>
• Всего товаров: {products_count}
• Всего категорий: {categories_count}"""
        
        products_count = len(self.catalog.get("products", []))
        categories_count = len(self.catalog.get("categories", []))
        
        text = text.format(products_count=products_count, categories_count=categories_count)
        
        # Добавляем кнопки для быстрого доступа
        keyboard = [
            [InlineKeyboardButton("🔄 Сбросить состояния", callback_data="admin_reset")],
            [InlineKeyboardButton("📦 Добавить товар", callback_data="admin_add_product")],
            [InlineKeyboardButton("📁 Добавить категорию", callback_data="admin_add_category")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')
    
    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Сброс состояний админа"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав доступа")
            return
        
        # Очищаем все состояния ожидания
        context.user_data.clear()
        
        await update.message.reply_text(
            "✅ <b>Состояния сброшены</b>\n\n"
            "Все активные процессы добавления товаров/категорий отменены.\n"
            "Используйте /admin для управления каталогом.",
            parse_mode='HTML'
        )
    
    async def add_product_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Добавить товар"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав доступа")
            return
        
        # Показываем доступные категории
        categories = self.catalog.get("categories", [])
        if not categories:
            await update.message.reply_text("❌ Сначала добавьте категории командой /add_category")
            return
        
        text = "📦 <b>Добавление товара</b>\n\nВыберите категорию:"
        keyboard = []
        
        for category in categories:
            keyboard.append([InlineKeyboardButton(
                f"📁 {category['name']}", 
                callback_data=f"add_product_category_{category['id']}"
            )])
        
        keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="admin_cancel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')
    
    async def delete_product_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Удалить товар"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав доступа")
            return
        
        products = self.catalog.get("products", [])
        if not products:
            await update.message.reply_text("❌ В каталоге нет товаров")
            return
        
        text = "🗑️ <b>Удаление товара</b>\n\nВыберите товар для удаления:"
        keyboard = []
        
        for product in products[:10]:  # Показываем первые 10 товаров
            keyboard.append([InlineKeyboardButton(
                f"❌ {product['name']} ({product['price']} ₽)", 
                callback_data=f"delete_product_{product['id']}"
            )])
        
        keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="admin_cancel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')
    
    async def add_category_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Добавить категорию"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав доступа")
            return
        
        await update.message.reply_text(
            "📁 <b>Добавление категории</b>\n\n"
            "Отправьте сообщение в формате:\n"
            "<code>название_категории|описание</code>\n\n"
            "Пример: <code>свечи|Ароматические свечи ручной работы</code>",
            parse_mode='HTML'
        )
        
        # Устанавливаем состояние ожидания ввода категории
        context.user_data['waiting_for_category'] = True
    
    async def delete_category_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Удалить категорию"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав доступа")
            return
        
        categories = self.catalog.get("categories", [])
        if not categories:
            await update.message.reply_text("❌ В каталоге нет категорий")
            return
        
        text = "🗑️ <b>Удаление категории</b>\n\nВыберите категорию для удаления:"
        keyboard = []
        
        for category in categories:
            keyboard.append([InlineKeyboardButton(
                f"❌ {category['name']}", 
                callback_data=f"delete_category_{category['id']}"
            )])
        
        keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="admin_cancel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')
    
    async def list_products_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать все товары"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав доступа")
            return
        
        products = self.catalog.get("products", [])
        if not products:
            await update.message.reply_text("❌ В каталоге нет товаров")
            return
        
        text = "📦 <b>Список товаров</b>\n\n"
        
        for i, product in enumerate(products, 1):
            status = "✅" if product.get("available", True) else "❌"
            text += f"{i}. {status} <b>{product['name']}</b>\n"
            text += f"   💰 {product['price']} ₽\n"
            text += f"   📁 {product['category']}\n\n"
        
        if len(text) > 4000:  # Ограничение Telegram
            text = text[:4000] + "\n... (список обрезан)"
        
        await update.message.reply_text(text, parse_mode='HTML')
    
    async def list_categories_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать все категории"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав доступа")
            return
        
        categories = self.catalog.get("categories", [])
        if not categories:
            await update.message.reply_text("❌ В каталоге нет категорий")
            return
        
        text = "📁 <b>Список категорий</b>\n\n"
        
        for i, category in enumerate(categories, 1):
            text += f"{i}. <b>{category['name']}</b>\n"
            if category.get('description'):
                text += f"   📝 {category['description']}\n"
            text += f"   🆔 {category['id']}\n\n"
        
        await update.message.reply_text(text, parse_mode='HTML')
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать главное меню"""
        text = "Выберите действие:"
        keyboard = [
            [InlineKeyboardButton("ℹ️ О нас", callback_data="about_us")],
            [InlineKeyboardButton("📢 Перейти на основной канал", callback_data="main_channel")],
            [InlineKeyboardButton("🛒 Открыть магазин", callback_data="open_mini_app")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
        else:
            await update.message.reply_text(text, reply_markup=reply_markup)
    
    async def show_about_us(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать раздел 'О нас'"""
        about_text = """Иногда все, что нужно - это отключить мысли и просто улыбаться. 😊 Здесь ты не найдешь место для философских размышлений. Мои свечи идеально подойдут для душевного отдыха в одиночестве или в компании. 🤗 А выбранные запахи, помогут расслабиться, отвлечься от забот и провести вечер с удовольствием. 🕯️

Бывают дни, когда хочется спрятаться от забот, забраться под плед с чашкой чая ☕, и зажечь свечу, которое не требует усилий, но при этом гарантированно поднимает настроение. 😌 Именно для таких случаев и создана эта подборка.

Тебя ждут легкие, теплые, местами романтичные нотки аромата свечей - идеальные спутники для уютного вечера. 🌙✨"""
        
        keyboard = [
            [InlineKeyboardButton("❓ Часто задаваемые вопросы", callback_data="faq")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(about_text, reply_markup=reply_markup)
    
    async def show_main_channel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать ссылку на основной канал"""
        text = "Переходите на наш основной канал для новостей и обновлений:"
        keyboard = [
            [InlineKeyboardButton("📢 @daryreflexive1999", url="https://t.me/daryreflexive1999")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_faq(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать FAQ"""
        text = "Часто задаваемые вопросы:"
        keyboard = [
            [InlineKeyboardButton("🚚 Сколько времени занимает доставка?", callback_data="faq_delivery")],
            [InlineKeyboardButton("🕯️ Памятка по уходу за свечами", callback_data="faq_care")],
            [InlineKeyboardButton("🪔 Можно ли выбрать воск?", callback_data="faq_wax")],
            [InlineKeyboardButton("🎨 Можно ли выбрать цвет свечи?", callback_data="faq_color")],
            [InlineKeyboardButton("✨ Как сделать свечу уникальной?", callback_data="faq_unique")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_faq_delivery(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать ответ о доставке"""
        text = "Обычно от 2-х дней (зависит от расстояния). 📦"
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="faq")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_faq_care(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать памятку по уходу за свечами"""
        text = """⚠️ Памятка по уходу за свечами:

• Перед тем как зажечь свечу, обрежьте фитиль (0,5–0,6 см). ✂️
• Зажигайте свечу минимум на час, чтобы воск растаял правильно. ⏰
• Повторное зажигание — не ранее, чем через 2 часа. ⏳
• Не держите свечу дольше 4 часов. 🕐
• Гасите крышкой. 🛡️
• Не оставляйте без присмотра. 👀
• Хранить в прохладном, сухом месте, вдали от солнца. 🌡️"""
        
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="faq")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_faq_wax(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать ответ о воске"""
        text = "Да, использую соевый и кокосовый воск. 🌱🥥"
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="faq")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_faq_color(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать ответ о цвете свечи"""
        text = "Да, до двух оттенков или градиент. 🌈"
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="faq")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_faq_unique(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать ответ об уникальности свечи"""
        text = "Можно добавить сухоцветы, фрукты, сладости, шиммер или минералы. 🌸🍓✨"
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="faq")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def open_mini_app(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Открыть мини-приложение"""
        text = "Открываем магазин..."
        keyboard = [
            [InlineKeyboardButton("🛒 Открыть магазин", web_app=WebAppInfo(url="https://soda2l.github.io/daryrei-mini-app/"))],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        # Основные кнопки
        if data == "start_shopping":
            await self.show_main_menu(update, context)
        elif data == "about_us":
            await self.show_about_us(update, context)
        elif data == "main_channel":
            await self.show_main_channel(update, context)
        elif data == "faq":
            await self.show_faq(update, context)
        elif data == "back_to_main":
            await self.show_main_menu(update, context)
        elif data == "back_to_about":
            await self.show_about_us(update, context)
        elif data == "faq_delivery":
            await self.show_faq_delivery(update, context)
        elif data == "faq_care":
            await self.show_faq_care(update, context)
        elif data == "faq_wax":
            await self.show_faq_wax(update, context)
        elif data == "faq_color":
            await self.show_faq_color(update, context)
        elif data == "faq_unique":
            await self.show_faq_unique(update, context)
        elif data == "open_mini_app":
            await self.open_mini_app(update, context)
        
        # Админские кнопки
        elif data == "admin_cancel":
            await query.edit_message_text("❌ Операция отменена")
        elif data == "cancel":
            await query.edit_message_text("❌ Операция отменена")
        elif data == "admin_reset":
            await self.handle_admin_reset(update, context)
        elif data == "admin_add_product":
            await self.add_product_command(update, context)
        elif data == "admin_add_category":
            await self.add_category_command(update, context)
        elif data.startswith("add_product_category_"):
            category_id = data.replace("add_product_category_", "")
            await self.handle_add_product_category(update, context, category_id)
        elif data.startswith("delete_product_"):
            product_id = data.replace("delete_product_", "")
            await self.handle_delete_product(update, context, product_id)
        elif data.startswith("delete_category_"):
            category_id = data.replace("delete_category_", "")
            await self.handle_delete_category(update, context, category_id)
        elif data.startswith("delete_category_products_"):
            category_id = data.replace("delete_category_products_", "")
            await self.handle_delete_category_products(update, context, category_id)
    
    # ========== ОБРАБОТЧИКИ АДМИНСКИХ ДЕЙСТВИЙ ==========
    
    async def handle_admin_reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка сброса состояний через кнопку"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.callback_query.edit_message_text("❌ У вас нет прав доступа")
            return
        
        # Очищаем все состояния ожидания
        context.user_data.clear()
        
        await update.callback_query.edit_message_text(
            "✅ <b>Состояния сброшены</b>\n\n"
            "Все активные процессы добавления товаров/категорий отменены.\n"
            "Используйте /admin для управления каталогом.",
            parse_mode='HTML'
        )
    
    async def handle_add_product_category(self, update: Update, context: ContextTypes.DEFAULT_TYPE, category_id):
        """Обработка выбора категории для добавления товара"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.callback_query.edit_message_text("❌ У вас нет прав доступа")
            return
        
        # Сохраняем выбранную категорию
        context.user_data['selected_category'] = category_id
        context.user_data['waiting_for_product_name'] = True
        
        await update.callback_query.edit_message_text(
            "📦 <b>Добавление товара</b>\n\n"
            "Отправьте название товара:",
            parse_mode='HTML'
        )
    
    async def handle_delete_product(self, update: Update, context: ContextTypes.DEFAULT_TYPE, product_id):
        """Обработка удаления товара"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.callback_query.edit_message_text("❌ У вас нет прав доступа")
            return
        
        # Находим товар
        product = None
        for p in self.catalog.get("products", []):
            if p["id"] == product_id:
                product = p
                break
        
        if not product:
            await update.callback_query.edit_message_text("❌ Товар не найден")
            return
        
        # Удаляем товар
        if self.delete_product(product_id):
            await update.callback_query.edit_message_text(
                f"✅ Товар <b>{product['name']}</b> успешно удален",
                parse_mode='HTML'
            )
        else:
            await update.callback_query.edit_message_text("❌ Ошибка при удалении товара")
    
    async def handle_delete_category(self, update: Update, context: ContextTypes.DEFAULT_TYPE, category_id):
        """Обработка удаления категории"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.callback_query.edit_message_text("❌ У вас нет прав доступа")
            return
        
        # Находим категорию
        category = None
        for c in self.catalog.get("categories", []):
            if c["id"] == category_id:
                category = c
                break
        
        if not category:
            await update.callback_query.edit_message_text("❌ Категория не найдена")
            return
        
        # Удаляем категорию
        if self.delete_category(category_id):
            await update.callback_query.edit_message_text(
                f"✅ Категория <b>{category['name']}</b> и все товары в ней успешно удалены",
                parse_mode='HTML'
            )
        else:
            await update.callback_query.edit_message_text("❌ Ошибка при удалении категории")
    
    async def handle_delete_category_products(self, update: Update, context: ContextTypes.DEFAULT_TYPE, category_id):
        """Обработка удаления товаров по категории"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.callback_query.edit_message_text("❌ У вас нет прав доступа")
            return
        
        try:
            # Находим категорию
            category = None
            for c in self.catalog.get("categories", []):
                if c["id"] == category_id:
                    category = c
                    break
            
            if not category:
                await update.callback_query.edit_message_text("❌ Категория не найдена")
                return
            
            # Получаем товары этой категории
            products_in_category = [
                p for p in self.catalog.get("products", []) 
                if p.get("category") == category_id
            ]
            
            if not products_in_category:
                await update.callback_query.edit_message_text(
                    f"ℹ️ В категории <b>{category['name']}</b> нет товаров",
                    parse_mode='HTML'
                )
                return
            
            # Создаем кнопки для выбора товаров
            keyboard = []
            for product in products_in_category:
                keyboard.append([InlineKeyboardButton(
                    f"🗑️ {product['name']} - {product['price']}₽", 
                    callback_data=f"delete_product_{product['id']}"
                )])
            
            keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="cancel")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.callback_query.edit_message_text(
                f"🗂️ <b>Товары в категории '{category['name']}':</b>\n\n"
                f"Выберите товар для удаления:",
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Ошибка при получении товаров категории: {e}")
            await update.callback_query.edit_message_text(f"❌ Ошибка: {e}")
    
    async def handle_web_app_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик данных от WebApp"""
        try:
            logger.info("=== ПОЛУЧЕНЫ ДАННЫЕ ОТ WEBAPP ===")
            logger.info(f"Update ID: {update.update_id}")
            logger.info(f"Message ID: {update.message.message_id if update.message else 'None'}")
            logger.info(f"User ID: {update.effective_user.id if update.effective_user else 'None'}")
            
            if not update.message or not update.message.web_app_data:
                logger.error("Нет данных от WebApp в сообщении")
                await update.message.reply_text("❌ Не получены данные от приложения")
                return
            
            # Получаем данные от WebApp
            web_app_data = update.message.web_app_data.data
            logger.info(f"Raw web_app_data: {web_app_data}")
            
            # Пытаемся распарсить JSON
            try:
                data = json.loads(web_app_data)
                logger.info(f"Parsed data: {data}")
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка парсинга JSON: {e}")
                await update.message.reply_text("❌ Ошибка формата данных от приложения")
                return
            
            # Проверяем тип данных
            if data.get('type') == 'order':
                logger.info("Обрабатываем заказ...")
                # Отправляем заказ в группу
                await self.send_order_to_group(update, context, data)
                
                # Отправляем подтверждение пользователю
                await update.message.reply_text(
                    "✅ Заказ успешно отправлен! Мы свяжемся с вами в ближайшее время для обсуждения деталей оплаты и доставки.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🛒 Продолжить покупки", web_app=WebAppInfo(url="https://soda2l.github.io/daryrei-mini-app/"))
                    ]])
                )
            else:
                logger.warning(f"Неизвестный тип данных от WebApp: {data.get('type')}")
                await update.message.reply_text(f"❌ Неизвестный тип данных: {data.get('type')}")
                
        except Exception as e:
            logger.error(f"Критическая ошибка при обработке данных от WebApp: {e}")
            await update.message.reply_text(f"❌ Произошла критическая ошибка при обработке заказа: {str(e)}")
    
    async def send_order_to_group(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: dict):
        """Отправить заказ в группу"""
        try:
            message = data.get('message', '')
            group_id = data.get('groupId', ORDER_GROUP_ID)
            
            logger.info(f"=== ОТПРАВКА ЗАКАЗА В ГРУППУ ===")
            logger.info(f"Message length: {len(message)}")
            logger.info(f"Group ID: {group_id}")
            
            # Проверяем, что сообщение не пустое
            if not message.strip():
                logger.error("Пустое сообщение для отправки в группу")
                await update.message.reply_text("❌ Ошибка: пустое сообщение заказа")
                return
            
            # Отправляем сообщение в группу
            sent_message = await context.bot.send_message(
                chat_id=group_id,
                text=message,
                parse_mode='HTML'
            )
            
            logger.info(f"✅ Заказ успешно отправлен в группу {group_id}")
            logger.info(f"Sent message ID: {sent_message.message_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке заказа в группу: {e}")
            await update.message.reply_text(f"❌ Произошла ошибка при отправке заказа: {str(e)}")
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений (резервный для заказов)"""
        try:
            message_text = update.message.text
            user_id = update.effective_user.id
            logger.info(f"Получено текстовое сообщение: {message_text}")
            
            # Игнорируем команды (они обрабатываются отдельными обработчиками)
            if message_text.startswith('/'):
                return
            
            # Проверяем админские состояния
            if self.is_admin(user_id):
                if context.user_data.get('waiting_for_category'):
                    await self.handle_category_input(update, context, message_text)
                    return
                elif context.user_data.get('waiting_for_product_name'):
                    await self.handle_product_name_input(update, context, message_text)
                    return
                elif context.user_data.get('waiting_for_product_description'):
                    await self.handle_product_description_input(update, context, message_text)
                    return
                elif context.user_data.get('waiting_for_product_price'):
                    await self.handle_product_price_input(update, context, message_text)
                    return
                elif context.user_data.get('waiting_for_product_photos'):
                    if message_text.lower().strip() in ['готово', 'готово!', 'завершить', 'закончить']:
                        # Завершаем добавление товара
                        context.user_data.pop('waiting_for_product_photos', None)
                        context.user_data.pop('current_product_id', None)
                        await update.message.reply_text(
                            "✅ <b>Товар успешно добавлен в каталог!</b>\n\n"
                            "Используйте /admin для управления каталогом",
                            parse_mode='HTML'
                        )
                        return
                    else:
                        await update.message.reply_text(
                            "📸 Отправьте фото товара или напишите 'готово' для завершения"
                        )
                        return
                else:
                    # Админ без активных состояний - показываем меню
                    await self.show_main_menu(update, context)
                    return
            
            # Проверяем, не является ли это заказом (начинается с "🛒 НОВЫЙ ЗАКАЗ")
            if message_text.startswith("🛒 НОВЫЙ ЗАКАЗ"):
                logger.info("Обнаружен заказ в текстовом сообщении")
                
                # Отправляем заказ в группу
                await context.bot.send_message(
                    chat_id=ORDER_GROUP_ID,
                    text=message_text,
                    parse_mode='HTML'
                )
                
                await update.message.reply_text(
                    "✅ Заказ получен и отправлен в группу! Мы свяжемся с вами в ближайшее время.",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🛒 Продолжить покупки", web_app=WebAppInfo(url="https://soda2l.github.io/daryrei-mini-app/"))
                    ]])
                )
            else:
                # Обычное сообщение - показываем меню
                await self.show_main_menu(update, context)
                
        except Exception as e:
            logger.error(f"Ошибка при обработке текстового сообщения: {e}")
            await update.message.reply_text("❌ Произошла ошибка при обработке сообщения.")
    
    # ========== ОБРАБОТЧИКИ ВВОДА АДМИНА ==========
    
    async def handle_category_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str):
        """Обработка ввода категории"""
        try:
            # Парсим ввод: название|описание
            if '|' in message_text:
                name, description = message_text.split('|', 1)
                name = name.strip()
                description = description.strip()
            else:
                name = message_text.strip()
                description = ""
            
            if not name:
                await update.message.reply_text("❌ Название категории не может быть пустым")
                return
            
            # Создаем ID категории (транслитерация)
            category_id = name.lower().replace(' ', '_').replace('ё', 'e').replace('й', 'y')
            category_id = ''.join(c for c in category_id if c.isalnum() or c == '_')
            
            # Проверяем, не существует ли уже такая категория
            for cat in self.catalog.get("categories", []):
                if cat["id"] == category_id:
                    await update.message.reply_text("❌ Категория с таким названием уже существует")
                    return
            
            # Добавляем категорию
            if self.add_category(category_id, name, description):
                await update.message.reply_text(
                    f"✅ Категория <b>{name}</b> успешно добавлена!\n"
                    f"🆔 ID: <code>{category_id}</code>",
                    parse_mode='HTML'
                )
            else:
                await update.message.reply_text("❌ Ошибка при добавлении категории")
            
            # Сбрасываем состояние
            context.user_data.pop('waiting_for_category', None)
            
        except Exception as e:
            logger.error(f"Ошибка при обработке ввода категории: {e}")
            await update.message.reply_text("❌ Ошибка при обработке ввода категории")
    
    async def handle_product_name_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str):
        """Обработка ввода названия товара"""
        if not message_text.strip():
            await update.message.reply_text("❌ Название товара не может быть пустым")
            return
        
        context.user_data['product_name'] = message_text.strip()
        context.user_data.pop('waiting_for_product_name', None)
        context.user_data['waiting_for_product_description'] = True
        
        await update.message.reply_text(
            "📝 <b>Добавление товара</b>\n\n"
            "Отправьте описание товара:",
            parse_mode='HTML'
        )
    
    async def handle_product_description_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str):
        """Обработка ввода описания товара"""
        context.user_data['product_description'] = message_text.strip()
        context.user_data.pop('waiting_for_product_description', None)
        context.user_data['waiting_for_product_price'] = True
        
        await update.message.reply_text(
            "💰 <b>Добавление товара</b>\n\n"
            "Отправьте цену товара (только число):",
            parse_mode='HTML'
        )
    
    async def handle_product_price_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str):
        """Обработка ввода цены товара"""
        try:
            price = int(message_text.strip())
            if price <= 0:
                await update.message.reply_text("❌ Цена должна быть больше 0")
                return
            
            # Создаем ID товара
            product_name = context.user_data.get('product_name', '')
            product_id = product_name.lower().replace(' ', '_').replace('ё', 'e').replace('й', 'y')
            product_id = ''.join(c for c in product_id if c.isalnum() or c == '_')
            product_id = f"{product_id}_{int(time.time())}"  # Добавляем timestamp для уникальности
            
            # Получаем данные
            category_id = context.user_data.get('selected_category')
            name = context.user_data.get('product_name')
            description = context.user_data.get('product_description', '')
            
            # Добавляем товар (пока без фото)
            if self.add_product(product_id, name, description, price, category_id, []):
                await update.message.reply_text(
                    f"✅ Товар <b>{name}</b> успешно добавлен!\n"
                    f"💰 Цена: {price} ₽\n"
                    f"📁 Категория: {category_id}\n"
                    f"🆔 ID: <code>{product_id}</code>\n\n"
                    f"📸 Для добавления фото отправьте изображения следующим сообщением",
                    parse_mode='HTML'
                )
                
                # Устанавливаем состояние ожидания фото
                context.user_data['waiting_for_product_photos'] = True
                context.user_data['current_product_id'] = product_id
            else:
                await update.message.reply_text("❌ Ошибка при добавлении товара")
            
            # Сбрасываем состояния
            context.user_data.pop('waiting_for_product_price', None)
            context.user_data.pop('selected_category', None)
            context.user_data.pop('product_name', None)
            context.user_data.pop('product_description', None)
            
        except ValueError:
            await update.message.reply_text("❌ Цена должна быть числом")
        except Exception as e:
            logger.error(f"Ошибка при обработке ввода цены: {e}")
            await update.message.reply_text("❌ Ошибка при обработке ввода цены")
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка фото для товаров"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            return
        
        if not context.user_data.get('waiting_for_product_photos'):
            return
        
        try:
            # Получаем фото с наилучшим качеством
            photo = update.message.photo[-1]
            file_id = photo.file_id
            
            # Получаем информацию о файле
            file_info = await context.bot.get_file(file_id)
            file_path = file_info.file_path
            
            # Создаем имя файла
            product_id = context.user_data.get('current_product_id')
            if not product_id:
                await update.message.reply_text("❌ Ошибка: не найден ID товара")
                return
            
            # Создаем папку для изображений если её нет
            images_dir = "images"
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            
            # Скачиваем файл
            filename = f"{product_id}_{int(time.time())}.jpg"
            filepath = os.path.join(images_dir, filename)
            
            # Скачиваем изображение
            logger.info(f"Product ID: {product_id}")
            logger.info(f"Сохраняем в: {filepath}")
            
            # Проверяем, содержит ли file_path уже полный URL
            if file_path.startswith('https://'):
                download_url = file_path
                logger.info(f"Скачиваем фото: {download_url}")
            else:
                download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
                logger.info(f"Скачиваем фото: {download_url}")
            
            try:
                import urllib.request
                urllib.request.urlretrieve(download_url, filepath)
                logger.info(f"Фото успешно скачано: {filepath}")
            except Exception as urllib_error:
                logger.error(f"HTTP Error при скачивании: {urllib_error}")
                # Fallback на requests
                try:
                    import requests
                    response = requests.get(download_url)
                    if response.status_code == 200:
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        logger.info(f"Фото скачано через requests: {filepath}")
                    else:
                        logger.error(f"Ошибка при скачивании через requests: HTTP {response.status_code}")
                        raise Exception(f"HTTP {response.status_code}")
                except Exception as requests_error:
                    logger.error(f"Ошибка при скачивании через requests: {requests_error}")
                    raise urllib_error
            
            # Добавляем фото к товару
            product = None
            for p in self.catalog.get("products", []):
                if p["id"] == product_id:
                    product = p
                    break
            
            if product:
                if "images" not in product:
                    product["images"] = []
                product["images"].append(filename)
                self.save_catalog()
                
                await update.message.reply_text(
                    f"✅ Фото добавлено к товару <b>{product['name']}</b>!\n"
                    f"📸 Всего фото: {len(product['images'])}\n\n"
                    f"Отправьте еще фото или напишите 'готово' для завершения",
                    parse_mode='HTML'
                )
            else:
                await update.message.reply_text("❌ Ошибка: товар не найден")
                
        except Exception as e:
            logger.error(f"Ошибка при обработке фото: {e}")
            await update.message.reply_text("❌ Ошибка при обработке фото")
    
    async def handle_all_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Универсальный обработчик для всех сообщений"""
        try:
            logger.info(f"=== УНИВЕРСАЛЬНЫЙ ОБРАБОТЧИК ===")
            logger.info(f"Update ID: {update.update_id}")
            
            # Проверяем, есть ли WebApp данные
            if hasattr(update.message, 'web_app_data') and update.message.web_app_data:
                logger.info("Обнаружены WebApp данные в универсальном обработчике!")
                await self.handle_web_app_data(update, context)
                return
            
            # Проверяем, есть ли текст сообщения
            if update.message and update.message.text:
                logger.info(f"Текстовое сообщение: {update.message.text}")
                # Проверяем, не является ли это заказом
                if update.message.text.startswith("🛒 НОВЫЙ ЗАКАЗ"):
                    logger.info("Обнаружен заказ в универсальном обработчике!")
                    await self.handle_text_message(update, context)
                    return
            
        except Exception as e:
            logger.error(f"Ошибка в универсальном обработчике: {e}")
        
        # Если это не заказ, не обрабатываем
        return False
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок"""
        logger.error(f"Ошибка в боте: {context.error}")
        
        # Если есть update и message, отправляем уведомление пользователю
        if update and update.effective_message:
            try:
                await update.effective_message.reply_text(
                    "❌ Произошла ошибка при обработке запроса. Попробуйте еще раз."
                )
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение об ошибке: {e}")
    
    async def update_catalog_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда для обновления каталога"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав доступа к этой команде")
            return
        
        try:
            # Перезагружаем каталог из файла
            self.load_catalog()
            await update.message.reply_text("✅ Каталог успешно обновлен!")
        except Exception as e:
            logger.error(f"Ошибка при обновлении каталога: {e}")
            await update.message.reply_text(f"❌ Ошибка при обновлении каталога: {e}")
    
    async def delete_product_by_category_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда для удаления товаров по категории"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ У вас нет прав доступа к этой команде")
            return
        
        try:
            catalog = self.get_catalog()
            categories = catalog.get('categories', [])
            
            if not categories:
                await update.message.reply_text("❌ В каталоге нет категорий")
                return
            
            # Создаем кнопки для выбора категории
            keyboard = []
            for category in categories:
                keyboard.append([InlineKeyboardButton(
                    f"🗂️ {category['name']}", 
                    callback_data=f"delete_category_products_{category['id']}"
                )])
            
            keyboard.append([InlineKeyboardButton("❌ Отмена", callback_data="cancel")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "🗂️ <b>Выберите категорию для удаления товаров:</b>",
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Ошибка при получении категорий: {e}")
            await update.message.reply_text(f"❌ Ошибка: {e}")
    
    def run(self):
        """Запуск бота"""
        logger.info("Запуск бота DaryRei...")
        logger.info("Flask API запущен на порту 8000")
        self.application.run_polling()

# Создаем экземпляр бота
bot = DaryReiBot()

# Запускаем бота
if __name__ == "__main__":
    bot.run()