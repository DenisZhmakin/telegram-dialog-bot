from telebot import TeleBot
from telebot.types import Message


class LpcpStateManager:
    @staticmethod
    def process(bot: TeleBot, message: Message):
        if message.text.startswith("Далее"):
            bot.reply_to(message, "Далее lpcp")
        elif message.text.startswith("Обновить"):
            bot.reply_to(message, "Обновить lpcp")
        elif message.text.startswith("Назад"):
            bot.reply_to(message, "Назад lpcp")
