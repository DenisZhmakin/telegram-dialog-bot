from typing import Callable

from telebot import TeleBot
from telebot.types import Message

from keyboard import main_keyboard
from machines.abstractfinalstatemachine import AbstractFinalStateMachine


class DefaultFinalStateMachine(AbstractFinalStateMachine):
    def __init__(self, bot: TeleBot, parent_trigger: Callable):
        self.parent_trigger = parent_trigger
        self.bot = bot

    def initialize(self, message: Message):
        pass

    def begin_button_handler(self, message: Message):
        self.bot.reply_to(message, "Произошла внутренняя ошибка")

    def next_button_handler(self, message: Message):
        self.bot.reply_to(message, "Произошла внутренняя ошибка")

    def previous_button_handler(self, message: Message):
        self.bot.reply_to(message, "Произошла внутренняя ошибка")

    def update_button_handler(self, message: Message):
        self.bot.reply_to(message, "Произошла внутренняя ошибка")

    def print_document(self, message: Message):
        self.bot.reply_to(message, "Произошла внутренняя ошибка")

    def show_keyboard(self, message: Message):
        self.bot.reply_to(message, "Произошла внутренняя ошибка")

    def text_handler(self, message: Message):
        self.bot.reply_to(message, "Произошла внутренняя ошибка")

    def back_to_menu_handler(self, message: Message):
        self.bot.reply_to(message,
                          "Вы вернулись в главное меню чат-бота для деловой переписке",
                          reply_markup=main_keyboard)
        self.parent_trigger('back-to-start')
