from telegram import Update
from telegram.ext import ContextTypes
from ..keyboards.keyboards import get_main_keyboard, get_back_keyboard, get_inline_url_keyboard
from ..utils.helpers import setup_logger

# Настройка логгера
logger = setup_logger()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик команды /start."""
    from main import START, AWAITING_CODE
    
    user = update.effective_user
    logger.info(f"User {user.id} started the bot")
    
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я бот для заказа материалов.\n\n"
        "Пожалуйста, введите код товара/номер заказа:"
    )
    return AWAITING_CODE

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help."""
    await update.message.reply_text(
        "Этот бот предназначен для заказа материалов.\n\n"
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/menu - Показать главное меню\n\n"
        "Для начала работы введите /start и следуйте инструкциям."
    )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик команды /menu."""
    from main import MAIN_MENU
    
    await update.message.reply_text(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    )
    return MAIN_MENU

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возвращает пользователя в главное меню."""
    from main import MAIN_MENU
    
    await update.message.reply_text(
        "Главное меню:",
        reply_markup=get_main_keyboard()
    )
    return MAIN_MENU

async def handle_instructions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик для раздела инструкций."""
    from main import MAIN_MENU
    
    await update.message.reply_text(
        "Файл на данный момент формируется пользователем. Группа сайтов файлов может скачиваться. "
        "Файлы можно скачивать, редактировать и добавляться заново в течение администратора.",
        reply_markup=get_back_keyboard()
    )
    return MAIN_MENU

async def handle_megabook(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик для раздела мегабука."""
    from main import MAIN_MENU
    
    megabook_url = "https://megabook.example.com"
    
    await update.message.reply_text(
        "Пользователь переходит по ссылке:",
        reply_markup=get_inline_url_keyboard("Открыть мегабук", megabook_url)
    )
    
    # Также отправляем клавиатуру для возврата
    await update.message.reply_text(
        "Используйте кнопки ниже для навигации:",
        reply_markup=get_back_keyboard()
    )
    
    return MAIN_MENU

async def handle_photoset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик для раздела фотосета."""
    from main import MAIN_MENU
    
    photoset_bot = "@photoset_bot"
    
    await update.message.reply_text(
        f"Переход в чат с другим ботом: {photoset_bot}",
        reply_markup=get_back_keyboard()
    )
    return MAIN_MENU

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик неизвестных команд."""
    await update.message.reply_text(
        "Извините, я не понимаю эту команду. Пожалуйста, используйте /help для получения списка доступных команд."
    )

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик неизвестных сообщений."""
    await update.message.reply_text(
        "Извините, я не понимаю это сообщение. Пожалуйста, используйте /help для получения списка доступных команд."
    )
