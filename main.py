#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes

# Импорт модулей проекта
from handlers.command_handlers import start_command, help_command, menu_command, handle_instructions, handle_megabook, handle_photoset, unknown_command, unknown_message
from handlers.order_handlers import register_user, save_order, save_photo_video_order
from keyboards.keyboards import get_main_keyboard, get_back_keyboard
from utils.helpers import validate_product_code, setup_logger
from database.db import Database

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logger = setup_logger()

# Состояния диалога
START, AWAITING_CODE, MAIN_MENU, ORDER_WITH_PHOTO, ORDER_WITHOUT_PHOTO, INSTRUCTIONS, MEGABOOK, ADDITIONAL_INFO, PHOTO_VIDEO_ORDER, PHOTOSET = range(10)

# Токен бота из переменных окружения
TOKEN = os.getenv("TOKEN", "")

# Инициализация базы данных
db = Database()

# Функция для проверки кода товара
async def check_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Проверяет введенный код товара и переходит к соответствующему разделу."""
    code = update.message.text
    
    # Регистрируем пользователя при первом взаимодействии
    await register_user(update, context)
    
    # Проверяем корректность кода
    if validate_product_code(code):
        context.user_data['product_code'] = code
        await update.message.reply_text(
            "Код принят! Вы можете посмотреть инструкции по оформлению заказа, "
            "заказать материалы или воспользоваться другими функциями."
        )
        return await show_main_menu(update, context)
    else:
        await update.message.reply_text(
            "Неверный формат кода. Пожалуйста, проверьте корректность ввода и попробуйте снова."
        )
        return AWAITING_CODE

# Функция для отображения главного меню
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отображает главное меню с основными функциями."""
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=get_main_keyboard()
    )
    return MAIN_MENU

# Обработчик выбора в главном меню
async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает выбор пользователя в главном меню."""
    choice = update.message.text
    
    if choice == "Прикрепить фото":
        await update.message.reply_text(
            "Пожалуйста, прикрепите фото и добавьте описание к заказу.",
            reply_markup=get_back_keyboard()
        )
        return ORDER_WITH_PHOTO
    
    elif choice == "Отправить заказ без фото":
        await update.message.reply_text(
            "Пожалуйста, введите описание вашего заказа.",
            reply_markup=get_back_keyboard()
        )
        return ORDER_WITHOUT_PHOTO
    
    elif choice == "Инструкция по оформлению":
        return await handle_instructions(update, context)
    
    elif choice == "Мегабук":
        return await handle_megabook(update, context)
    
    elif choice == "Нужна другая информация?":
        await update.message.reply_text(
            "Какая дополнительная информация вам требуется? Пожалуйста, опишите ваш вопрос.",
            reply_markup=get_back_keyboard()
        )
        return ADDITIONAL_INFO
    
    elif choice == "Заказ фото/видео":
        await update.message.reply_text(
            "Пожалуйста, опишите, какие фото или видео вам необходимы.",
            reply_markup=get_back_keyboard()
        )
        return PHOTO_VIDEO_ORDER
    
    elif choice == "Фотосет":
        return await handle_photoset(update, context)
    
    elif choice == "Назад" or choice == "Главное меню":
        return await show_main_menu(update, context)
    
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите один из пунктов меню."
        )
        return MAIN_MENU

# Обработчик заказа с фото
async def handle_order_with_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает заказ с фотографией."""
    # Проверяем, есть ли фото в сообщении
    if update.message.photo:
        # Сохраняем ID фото в данных пользователя
        photo_id = update.message.photo[-1].file_id
        context.user_data['photo_id'] = photo_id
        
        # Если есть текст, сохраняем его как описание
        if update.message.caption:
            context.user_data['order_description'] = update.message.caption
            
            # Сохраняем заказ в базу данных
            await save_order(update, context, has_photo=True)
            
            await update.message.reply_text(
                "Заказ принят! Если через 10 рабочих дней материал не доставят, "
                "обратитесь к своему руководителю. Также с вами может связаться "
                "сотрудник для уточнения деталей заказа."
            )
            return await show_main_menu(update, context)
        else:
            await update.message.reply_text(
                "Пожалуйста, добавьте описание к фотографии."
            )
            return ORDER_WITH_PHOTO
    elif update.message.text == "Назад" or update.message.text == "Главное меню":
        return await show_main_menu(update, context)
    elif update.message.text:
        # Если пользователь отправил только текст без фото
        await update.message.reply_text(
            "Пожалуйста, прикрепите фотографию к вашему заказу."
        )
        return ORDER_WITH_PHOTO
    else:
        await update.message.reply_text(
            "Пожалуйста, отправьте фотографию с описанием."
        )
        return ORDER_WITH_PHOTO

# Обработчик заказа без фото
async def handle_order_without_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает заказ без фотографии."""
    if update.message.text == "Назад" or update.message.text == "Главное меню":
        return await show_main_menu(update, context)
    elif update.message.text:
        context.user_data['order_description'] = update.message.text
        
        # Сохраняем заказ в базу данных
        await save_order(update, context, has_photo=False)
        
        await update.message.reply_text(
            "Заказ принят! Если через 10 рабочих дней материал не доставят, "
            "обратитесь к своему руководителю. Также с вами может связаться "
            "сотрудник для уточнения деталей заказа."
        )
        return await show_main_menu(update, context)
    else:
        await update.message.reply_text(
            "Пожалуйста, введите описание вашего заказа."
        )
        return ORDER_WITHOUT_PHOTO

# Обработчик дополнительной информации
async def handle_additional_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает запрос дополнительной информации."""
    if update.message.text == "Назад" or update.message.text == "Главное меню":
        return await show_main_menu(update, context)
    
    query = update.message.text
    
    # Здесь должна быть логика обработки запроса дополнительной информации
    
    await update.message.reply_text(
        f"Спасибо за ваш запрос: '{query}'. Мы обработаем его и свяжемся с вами."
    )
    return await show_main_menu(update, context)

# Обработчик заказа фото/видео
async def handle_photo_video_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает заказ фото/видео."""
    if update.message.text == "Назад" or update.message.text == "Главное меню":
        return await show_main_menu(update, context)
    
    if update.message.text:
        context.user_data['photo_video_order'] = update.message.text
        
        # Сохраняем заказ фото/видео в базу данных
        await save_photo_video_order(update, context)
        
        await update.message.reply_text(
            "Заказ на фото/видео принят! Мы свяжемся с вами для уточнения деталей."
        )
        return await show_main_menu(update, context)
    else:
        await update.message.reply_text(
            "Пожалуйста, опишите, какие фото или видео вам необходимы."
        )
        return PHOTO_VIDEO_ORDER

def main() -> None:
    """Запускает бота."""
    # Проверяем наличие токена
    if not TOKEN:
        logger.error("Токен бота не найден. Пожалуйста, установите переменную окружения TOKEN.")
        return
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Создаем обработчик диалога
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            AWAITING_CODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, check_code)
            ],
            MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_main_menu)
            ],
            ORDER_WITH_PHOTO: [
                MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, handle_order_with_photo)
            ],
            ORDER_WITHOUT_PHOTO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_order_without_photo)
            ],
            ADDITIONAL_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_additional_info)
            ],
            PHOTO_VIDEO_ORDER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_photo_video_order)
            ],
        },
        fallbacks=[
            CommandHandler("start", start_command),
            CommandHandler("menu", menu_command),
        ],
    )

    # Добавляем обработчики
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    
    # Обработчики неизвестных команд и сообщений
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    application.add_handler(MessageHandler(filters.ALL, unknown_message))

    # Запускаем бота
    logger.info("Бот запущен")
    application.run_polling()

if __name__ == '__main__':
    main()
