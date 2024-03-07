import os

import telebot
from dotenv import load_dotenv
from telebot.types import Message
from transitions import Machine

from keyboard import main_keyboard
from statemanagers.pecfinalstatemachine import PecFinalStateMachine


class TelegramBotMainFSM:
    def __init__(self):
        load_dotenv()
        self.bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])

        self.bot.message_handler(
            func=lambda message: message.text == "Предложение о расширении сотрудничества",
        )(self.proposal_expand_cooperation_handler)
        self.bot.message_handler(
            func=lambda message: message.text == "Письмо потенциальному клиенту по проекту",
        )(self.potential_client_on_project_letter_handler)
        self.bot.message_handler(
            func=lambda msg: msg.text == "Назад в меню"
        )(self.back_to_menu_handler)

        self.bot.message_handler(commands=['start'])(self.start_command_handler)

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

        self.machine = Machine(model=self,
                               states=['start', 'pec', 'lpcp', 'cdre', 'hnec', 'rtah'],
                               transitions=transitions,
                               initial='start')

        self.pecFinalStateMachine = PecFinalStateMachine(self.bot, getattr(self, 'trigger'))
        self.trigger = getattr(self, 'trigger')

    def start_command_handler(self, message: Message):
        self.bot.reply_to(message,
                          "Добро пожаловать в главное меню чат-бота для деловой переписке",
                          reply_markup=main_keyboard)

    def proposal_expand_cooperation_handler(self, message: Message):
        self.pecFinalStateMachine.initialize(message)

        self.bot.message_handler(
            func=lambda msg: msg.text == "Начать"
        )(self.pecFinalStateMachine.begin_button_handler)
        self.bot.message_handler(
            func=lambda msg: msg.text == "Далее"
        )(self.pecFinalStateMachine.next_button_handler)
        self.bot.message_handler(
            func=lambda msg: msg.text == "Назад"
        )(self.pecFinalStateMachine.previous_button_handler)
        self.bot.message_handler(
            func=lambda msg: msg.text == "Обновить"
        )(self.pecFinalStateMachine.update_button_handler)
        self.bot.message_handler(
            func=lambda msg: msg.text == "Назад в меню"
        )(self.pecFinalStateMachine.back_to_menu_handler)
        self.bot.message_handler(
            func=lambda msg: msg.text == "Назад в меню"
        )(self.pecFinalStateMachine.back_to_menu_handler)

        self.bot.message_handler(content_types=['text'])(self.pecFinalStateMachine.text_handler)

        self.trigger('start-to-pec')

    def potential_client_on_project_letter_handler(self, message: Message):
        pass

    def back_to_menu_handler(self, message: Message):
        self.start_command_handler(message)
        self.trigger('back-to-start')

    # elif message.text == "Формирование напоминания о дедлайне для сотрудника":
    #     self.trigger('start-to-cdre')
    #     self.bot.reply_to(message, "Выбрано 'Формирование напоминания о дедлайне для сотрудника'",
    #                       reply_markup=default_keyboard)
    # elif message.text == "Наем нового сотрудника в компанию":
    #     self.trigger('start-to-hnec')
    #     self.bot.reply_to(message, "Выбрано 'Наем нового сотрудника в компанию'",
    #                       reply_markup=default_keyboard)
    # elif message.text == "Запрос подсказок и дополнительной помощи":
    #     self.trigger('start-to-rtah')
    #     self.bot.reply_to(message, "Выбрано 'Запрос подсказок и дополнительной помощи'",
    #                       reply_markup=default_keyboard)

    def run(self):
        self.bot.polling()


if __name__ == "__main__":
    bot = TelegramBotMainFSM()
    bot.run()
