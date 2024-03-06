from telebot import TeleBot
from telebot.types import Message


class RtahStateManager:
    @staticmethod
    def process(bot: TeleBot, message: Message):
        if message.text.startswith("Далее"):
            bot.reply_to(message, "Далее rtah")
        elif message.text.startswith("Обновить"):
            bot.reply_to(message, "Обновить rtah")
        elif message.text.startswith("Назад"):
            bot.reply_to(message, "Назад rtah")
