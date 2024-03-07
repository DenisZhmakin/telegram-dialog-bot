from typing import Optional

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(KeyboardButton(text="Предложение о расширении сотрудничества"))
main_keyboard.add(KeyboardButton(text="Письмо потенциальному клиенту по проекту"))
main_keyboard.add(KeyboardButton(text="Формирование напоминания о дедлайне для сотрудника"))
main_keyboard.add(KeyboardButton(text="Наем нового сотрудника в компанию"))
main_keyboard.add(KeyboardButton(text="Запрос подсказок и дополнительной помощи"))


def create_arrows_keyboard(placeholder: Optional[str] = None):
    if placeholder is not None:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder=placeholder)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(KeyboardButton(text="Далее"))
    keyboard.add(KeyboardButton(text="Обновить"))
    keyboard.add(KeyboardButton(text="Назад"))
    keyboard.add(KeyboardButton(text="Назад в меню"))

    return keyboard


start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(KeyboardButton(text="Начать"))
start_keyboard.add(KeyboardButton(text="Назад в меню"))

print_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
print_keyboard.add(KeyboardButton(text="Печать"))
print_keyboard.add(KeyboardButton(text="Назад в меню"))
