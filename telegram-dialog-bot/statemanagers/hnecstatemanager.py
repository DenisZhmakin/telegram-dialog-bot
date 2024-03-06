from telebot import TeleBot
from telebot.types import Message


class HnecStateManager:
    @staticmethod
    def process(bot: TeleBot, message: Message):
        if message.text.startswith("Далее"):
            bot.reply_to(message, "Далее hnec")
        elif message.text.startswith("Обновить"):
            bot.reply_to(message, "Обновить hnec")
        elif message.text.startswith("Назад"):
            bot.reply_to(message, "Назад hnec")
