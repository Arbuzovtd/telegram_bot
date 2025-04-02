from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    """Создает основную клавиатуру для главного меню."""
    keyboard = [
        [KeyboardButton("Прикрепить фото")],
        [KeyboardButton("Отправить заказ без фото")],
        [KeyboardButton("Инструкция по оформлению")],
        [KeyboardButton("Мегабук")],
        [KeyboardButton("Нужна другая информация?")],
        [KeyboardButton("Заказ фото/видео")],
        [KeyboardButton("Фотосет")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_back_keyboard():
    """Создает клавиатуру с кнопками 'Назад' и 'Главное меню'."""
    keyboard = [
        [KeyboardButton("Назад")],
        [KeyboardButton("Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_yes_no_keyboard():
    """Создает клавиатуру с кнопками 'Да' и 'Нет'."""
    keyboard = [
        [KeyboardButton("Да"), KeyboardButton("Нет")],
        [KeyboardButton("Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_inline_url_keyboard(text, url):
    """Создает инлайн-клавиатуру с одной кнопкой-ссылкой."""
    keyboard = [[InlineKeyboardButton(text, url=url)]]
    return InlineKeyboardMarkup(keyboard)

def get_instructions_keyboard():
    """Создает клавиатуру для раздела инструкций."""
    keyboard = [
        [KeyboardButton("Скачать инструкцию")],
        [KeyboardButton("Назад")],
        [KeyboardButton("Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_megabook_keyboard():
    """Создает клавиатуру для раздела мегабука."""
    keyboard = [
        [KeyboardButton("Открыть мегабук")],
        [KeyboardButton("Назад")],
        [KeyboardButton("Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_photoset_keyboard():
    """Создает клавиатуру для раздела фотосета."""
    keyboard = [
        [KeyboardButton("Перейти к фотосету")],
        [KeyboardButton("Назад")],
        [KeyboardButton("Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
