from telebot.types import ReplyKeyboardMarkup, KeyboardButton

default_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard.add(KeyboardButton(text="Далее ➡️"))
default_keyboard.add(KeyboardButton(text="Обновить 🔄"))
default_keyboard.add(KeyboardButton(text="Назад ⬅️"))
default_keyboard.add(KeyboardButton(text="Назад в меню"))
