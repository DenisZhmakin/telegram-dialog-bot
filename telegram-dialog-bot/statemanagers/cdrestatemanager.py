from telebot import TeleBot
from telebot.types import Message


class CdreStateManager:
    @staticmethod
    def process(bot: TeleBot, message: Message):
        if message.text.startswith("Далее"):
            bot.reply_to(message, "Далее cdre")
        elif message.text.startswith("Обновить"):
            bot.reply_to(message, "Обновить cdre")
        elif message.text.startswith("Назад"):
            bot.reply_to(message, "Назад cdre")
