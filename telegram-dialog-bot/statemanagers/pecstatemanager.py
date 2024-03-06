from telebot import TeleBot
from telebot.types import Message


class PecStateManager:
    @staticmethod
    def process(bot: TeleBot, message: Message):
        if message.text.startswith("Далее"):
            bot.reply_to(message, "Далее pec")
        elif message.text.startswith("Обновить"):
            bot.reply_to(message, "Обновить pec")
        elif message.text.startswith("Назад"):
            bot.reply_to(message, "Назад pec")
