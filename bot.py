#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from threading import Thread

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

class DaryReiBot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
        self.setup_error_handlers()
        self.setup_http_server()
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("catalog", self.catalog_command))
        self.application.add_handler(CommandHandler("test", self.test_command))
        self.application.add_handler(CommandHandler("debug", self.debug_command))
        self.application.add_handler(CommandHandler("webapp", self.webapp_test_command))
        self.application.add_handler(CommandHandler("testwebapp", self.test_webapp_data_command))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Обработчик для данных от WebApp (приоритетный)
        self.application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, self.handle_web_app_data))
        
        # Обработчик для всех текстовых сообщений (на случай если WebApp не работает)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
        
        # Универсальный обработчик для всех сообщений (для отладки) - последний
        self.application.add_handler(MessageHandler(filters.ALL, self.handle_all_messages))
    
    def setup_error_handlers(self):
        """Настройка обработчиков ошибок"""
        self.application.add_error_handler(self.error_handler)
    
    def setup_http_server(self):
        """Настройка HTTP сервера"""
        self.http_app = FastAPI(title="DaryRei Bot API", version="1.0.0")
        
        # Настройка CORS для WebApp
        self.http_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # В продакшене лучше указать конкретные домены
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Добавляем маршруты
        self.http_app.post("/api/order")(self.handle_order_request)
        self.http_app.get("/api/health")(self.health_check)
        
        # Запускаем HTTP сервер в отдельном потоке
        self.http_thread = Thread(target=self.run_http_server, daemon=True)
        self.http_thread.start()
    
    def run_http_server(self):
        """Запуск HTTP сервера"""
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(self.http_app, host="0.0.0.0", port=port, log_level="info", access_log=False)
    
    async def health_check(self):
        """Проверка здоровья API"""
        return {"status": "ok", "message": "DaryRei Bot API is running"}
    
    async def handle_order_request(self, order_data: dict):
        """Обработка заказа от WebApp"""
        try:
            logger.info(f"=== ПОЛУЧЕН HTTP ЗАПРОС ЗАКАЗА ===")
            logger.info(f"Order data: {order_data}")
            
            # Проверяем наличие обязательных полей
            if not order_data.get('message'):
                raise HTTPException(status_code=400, detail="Message is required")
            
            # Отправляем заказ в группу
            await self.send_order_to_group_http(order_data)
            
            return {"status": "success", "message": "Order sent successfully"}
            
        except Exception as e:
            logger.error(f"Ошибка при обработке HTTP заказа: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def send_order_to_group_http(self, order_data: dict):
        """Отправить заказ в группу через HTTP API"""
        try:
            message = order_data.get('message', '')
            group_id = order_data.get('groupId', ORDER_GROUP_ID)
            
            logger.info(f"=== ОТПРАВКА ЗАКАЗА В ГРУППУ ЧЕРЕЗ HTTP ===")
            logger.info(f"Message length: {len(message)}")
            logger.info(f"Group ID: {group_id}")
            
            # Получаем бота из приложения
            bot = self.application.bot
            
            # Отправляем сообщение в группу
            sent_message = await bot.send_message(
                chat_id=group_id,
                text=message,
                parse_mode='HTML'
            )
            
            logger.info(f"✅ Заказ успешно отправлен в группу {group_id}")
            logger.info(f"Sent message ID: {sent_message.message_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке заказа в группу через HTTP: {e}")
            raise
    
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
        help_text = """Доступные команды:
/start - Начать работу с ботом
/help - Показать эту справку
/catalog - Открыть каталог товаров
/test - Тест отправки в группу
/webapp - Тест WebApp
/testwebapp - Тест обработки WebApp данных
/debug - Отправить тестовый заказ"""
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
🚚 Доставка: 300 ₽

📅 Дата: 16.09.2025, 20:53:57"""
            
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
    
    async def test_webapp_data_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Тестовая команда для проверки обработки WebApp данных"""
        try:
            # Создаем тестовые данные заказа
            test_data = {
                "type": "order",
                "message": "🛒 ТЕСТОВЫЙ ЗАКАЗ\n\n👤 Покупатель: @test_user\n\n📦 Товары:\n• Тестовая свеча - 1 шт. × 1000 ₽ = 1000 ₽\n\n💰 Итого: 1000 ₽\n🚚 Доставка: 300 ₽\n\n📅 Дата: " + str(context.bot_data.get('current_time', 'тест')),
                "groupId": ORDER_GROUP_ID
            }
            
            # Имитируем получение данных от WebApp
            logger.info("=== ТЕСТИРОВАНИЕ ОБРАБОТКИ WEBAPP ДАННЫХ ===")
            logger.info(f"Test data: {test_data}")
            
            # Отправляем тестовый заказ в группу
            await self.send_order_to_group(update, context, test_data)
            
            await update.message.reply_text("✅ Тестовые данные WebApp обработаны и отправлены в группу")
            
        except Exception as e:
            logger.error(f"Ошибка в тестовой команде WebApp: {e}")
            await update.message.reply_text(f"❌ Ошибка при тестировании: {str(e)}")
    
    async def catalog_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /catalog"""
        await self.show_main_menu(update, context)
    
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
    
    async def handle_web_app_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик данных от WebApp"""
        try:
            logger.info("=== ПОЛУЧЕНЫ ДАННЫЕ ОТ WEBAPP ===")
            logger.info(f"Update ID: {update.update_id}")
            logger.info(f"Message ID: {update.message.message_id if update.message else 'None'}")
            logger.info(f"User ID: {update.effective_user.id if update.effective_user else 'None'}")
            logger.info(f"WebApp data exists: {hasattr(update.message, 'web_app_data') and update.message.web_app_data is not None}")
            
            if not update.message or not update.message.web_app_data:
                logger.error("Нет данных от WebApp в сообщении")
                await update.message.reply_text("❌ Не получены данные от приложения")
                return
            
            # Получаем данные от WebApp
            web_app_data = update.message.web_app_data.data
            logger.info(f"Raw web_app_data: {web_app_data}")
            logger.info(f"WebApp data type: {type(web_app_data)}")
            
            # Пытаемся распарсить JSON
            try:
                data = json.loads(web_app_data)
                logger.info(f"Parsed data: {data}")
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка парсинга JSON: {e}")
                logger.error(f"Проблемные данные: {repr(web_app_data)}")
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
            logger.error(f"Тип ошибки: {type(e)}")
            logger.error(f"Traceback: {e.__traceback__}")
            await update.message.reply_text(f"❌ Произошла критическая ошибка при обработке заказа: {str(e)}")
    
    async def handle_all_updates(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик всех обновлений для отладки"""
        logger.info(f"=== ПОЛУЧЕНО ОБНОВЛЕНИЕ ===")
        logger.info(f"Update type: {update.update_id}")
        logger.info(f"Update: {update}")
        
        # Передаем обработку дальше
        return False
    
    async def handle_all_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Универсальный обработчик для всех сообщений"""
        try:
            logger.info(f"=== УНИВЕРСАЛЬНЫЙ ОБРАБОТЧИК ===")
            logger.info(f"Update ID: {update.update_id}")
            logger.info(f"Update: {update}")
            
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
    
    async def send_order_to_group(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: dict):
        """Отправить заказ в группу"""
        try:
            message = data.get('message', '')
            group_id = data.get('groupId', ORDER_GROUP_ID)
            
            logger.info(f"=== ОТПРАВКА ЗАКАЗА В ГРУППУ ===")
            logger.info(f"Message length: {len(message)}")
            logger.info(f"Message preview: {message[:200]}...")
            logger.info(f"Group ID: {group_id}")
            logger.info(f"ORDER_GROUP_ID: {ORDER_GROUP_ID}")
            
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
            logger.error(f"Тип ошибки: {type(e)}")
            logger.error(f"Детали ошибки: {str(e)}")
            
            # Пытаемся отправить простое сообщение без HTML
            try:
                logger.info("Пытаемся отправить сообщение без HTML форматирования...")
                await context.bot.send_message(
                    chat_id=group_id,
                    text=message
                )
                logger.info("✅ Сообщение отправлено без HTML форматирования")
            except Exception as e2:
                logger.error(f"❌ Ошибка при отправке без HTML: {e2}")
                await update.message.reply_text(f"❌ Произошла ошибка при отправке заказа: {str(e)}")
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений (резервный для заказов)"""
        try:
            message_text = update.message.text
            logger.info(f"Получено текстовое сообщение: {message_text}")
            
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
    
    def run(self):
        """Запуск бота"""
        logger.info("Запуск бота DaryRei...")
        self.application.run_polling()

# Создаем экземпляр бота
bot = DaryReiBot()

# Для Railway/Heroku - экспортируем app
app = bot.http_app

if __name__ == "__main__":
    bot.run()
