import os

import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from transitions import Machine

from keyboard import default_keyboard
from statemanagers.cdrestatemanager import CdreStateManager
from statemanagers.hnecstatemanager import HnecStateManager
from statemanagers.lpcpstatemanager import LpcpStateManager
from statemanagers.pecstatemanager import PecStateManager
from statemanagers.rtahstatemanager import RtahStateManager


class TelegramBotRunner:
    def __init__(self):
        load_dotenv()
        self.bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])

        transitions = [
            {'trigger': 'start-to-pec', 'source': 'start', 'dest': 'pec'},
            {'trigger': 'start-to-lpcp', 'source': 'start', 'dest': 'lpcp'},
            {'trigger': 'start-to-cdre', 'source': 'start', 'dest': 'cdre'},
            {'trigger': 'start-to-hnec', 'source': 'start', 'dest': 'hnec'},
            {'trigger': 'start-to-rtah', 'source': 'start', 'dest': 'rtah'},
            {'trigger': 'back-to-start',
             'source': ['start', 'pec', 'lpcp', 'cdre', 'hnec', 'rtah'],
             'dest': 'start'},
        ]

        # Расшифровка состояний:
        # pec - Предложение о расширении сотрудничества
        # lpcp - Письмо потенциальному клиенту по проекту
        # cdre - Формирование напоминания о дедлайне для сотрудника
        # hnec - Наем нового сотрудника в компанию
        # rtah - Запрос подсказок и дополнительной помощи
        self.machine = Machine(model=self,
                               states=['start', 'pec', 'lpcp', 'cdre', 'hnec', 'rtah'],
                               transitions=transitions,
                               initial='start')

        self.trigger = getattr(self, 'trigger')

        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(content_types=['text'])(self.router)

    def start(self, message: Message):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton(text="Предложение о расширении сотрудничества"))
        keyboard.add(KeyboardButton(text="Письмо потенциальному клиенту по проекту"))
        keyboard.add(KeyboardButton(text="Формирование напоминания о дедлайне для сотрудника"))
        keyboard.add(KeyboardButton(text="Наем нового сотрудника в компанию"))
        keyboard.add(KeyboardButton(text="Запрос подсказок и дополнительной помощи"))

        self.bot.reply_to(message,
                          "Добро пожаловать в чат-бота для деловой переписке",
                          reply_markup=keyboard)

    def router(self, message: Message):
        if self.machine.get_model_state(self).name == "pec":
            PecStateManager.process(self.bot, message)
        elif self.machine.get_model_state(self).name == "lpcp":
            LpcpStateManager.process(self.bot, message)
        elif self.machine.get_model_state(self).name == "cdre":
            CdreStateManager.process(self.bot, message)
        elif self.machine.get_model_state(self).name == "hnec":
            HnecStateManager.process(self.bot, message)
        elif self.machine.get_model_state(self).name == "rtah":
            RtahStateManager.process(self.bot, message)

        if message.text == "Предложение о расширении сотрудничества":
            self.trigger('start-to-pec')
            self.bot.reply_to(message, "Выбрано 'Предложение о расширении сотрудничества'",
                              reply_markup=default_keyboard)
        elif message.text == "Письмо потенциальному клиенту по проекту":
            self.trigger('start-to-lpcp')
            self.bot.reply_to(message, "Выбрано 'Письмо потенциальному клиенту по проекту'",
                              reply_markup=default_keyboard)
        elif message.text == "Формирование напоминания о дедлайне для сотрудника":
            self.trigger('start-to-cdre')
            self.bot.reply_to(message, "Выбрано 'Формирование напоминания о дедлайне для сотрудника'",
                              reply_markup=default_keyboard)
        elif message.text == "Наем нового сотрудника в компанию":
            self.trigger('start-to-hnec')
            self.bot.reply_to(message, "Выбрано 'Наем нового сотрудника в компанию'",
                              reply_markup=default_keyboard)
        elif message.text == "Запрос подсказок и дополнительной помощи":
            self.trigger('start-to-rtah')
            self.bot.reply_to(message, "Выбрано 'Запрос подсказок и дополнительной помощи'",
                              reply_markup=default_keyboard)
        elif message.text == "Назад в меню":
            self.trigger('back-to-start')
            self.start(message)

    def run(self):
        self.bot.polling()


if __name__ == "__main__":
    bot = TelegramBotRunner()
    bot.run()
