import os
from typing import Optional

import telebot
from dotenv import load_dotenv
from telebot.types import Message
from transitions import Machine

from keyboard import main_keyboard
from machines.abstractfinalstatemachine import AbstractFinalStateMachine
from machines.cooperationofferfinalstatemachine import CooperationOfferFinalStateMachine
from machines.guaranteeletterfinalstatemachine import GuaranteeLetterFinalStateMachine


class TelegramBotMainFSM:
    def __init__(self):
        load_dotenv()
        self.bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])

        @self.bot.message_handler(func=lambda msg: msg.text == "Формирование предложения о сотрудничестве")
        def cooperation_offer_wrapper(message: Message): self.cooperation_offer_handler(message)
        @self.bot.message_handler(func=lambda msg: msg.text == "Формирование гарантийного письма от организации")
        def guarantee_letter_wrapper(message: Message): self.guarantee_letter_handler(message)
        @self.bot.message_handler(func=lambda msg: msg.text == "Назад в меню")
        def back_to_menu_wrapper(message: Message): self.back_to_menu_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Начать")
        def begin_button_wrapper(message: Message):
            current_fsm = self.get_current_fsm()

            if current_fsm is None:
                self.bot.reply_to(message, "Произошла внутренняя ошибка")
            else:
                current_fsm.begin_button_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Далее")
        def next_button_wrapper(message: Message):
            current_fsm = self.get_current_fsm()

            if current_fsm is None:
                self.bot.reply_to(message, "Произошла внутренняя ошибка")
            else:
                current_fsm.next_button_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Назад")
        def previous_button_wrapper(message: Message):
            current_fsm = self.get_current_fsm()

            if current_fsm is None:
                self.bot.reply_to(message, "Произошла внутренняя ошибка")
            else:
                current_fsm.previous_button_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Обновить")
        def update_button_wrapper(message: Message):
            current_fsm = self.get_current_fsm()

            if current_fsm is None:
                self.bot.reply_to(message, "Произошла внутренняя ошибка")
            else:
                current_fsm.update_button_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Печать")
        def print_document_wrapper(message: Message):
            current_fsm = self.get_current_fsm()

            if current_fsm is None:
                self.bot.reply_to(message, "Произошла внутренняя ошибка")
            else:
                current_fsm.print_document(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Назад в меню")
        def back_to_menu_button_wrapper(message: Message):
            current_fsm = self.get_current_fsm()

            if current_fsm is not None:
                current_fsm.back_to_menu_handler(message)
            else:
                self.back_to_menu_handler(message)

        @self.bot.message_handler(content_types=['text'])
        def text_wrapper(message: Message):
            current_fsm = self.get_current_fsm()

            if current_fsm is None:
                self.bot.reply_to(message, "Произошла внутренняя ошибка")
            else:
                current_fsm.text_handler(message)

        self.bot.message_handler(commands=['start'])(self.start_command_handler)

        transitions = [
            {'trigger': 'start-to-cooperation-offer', 'source': 'start', 'dest': 'cooperation-offer'},
            {'trigger': 'start-to-guarantee-letter', 'source': 'start', 'dest': 'guarantee-letter'},
            {'trigger': 'back-to-start',
             'source': ['start', 'cooperation-offer', 'guarantee-letter'],
             'dest': 'start'},
        ]

        self.machine = Machine(model=self,
                               states=['start', 'cooperation-offer', 'guarantee-letter'],
                               transitions=transitions,
                               initial='start')

        self.cooperation_offer_fsm = CooperationOfferFinalStateMachine(self.bot, getattr(self, 'trigger'))
        self.guarantee_letter_fsm = GuaranteeLetterFinalStateMachine(self.bot, getattr(self, 'trigger'))
        self.trigger = getattr(self, 'trigger')

    def get_current_fsm(self) -> Optional[AbstractFinalStateMachine]:
        if self.machine.get_model_state(self).name == 'cooperation-offer':
            return self.cooperation_offer_fsm
        elif self.machine.get_model_state(self).name == 'guarantee-letter':
            return self.guarantee_letter_fsm
        else:
            return None

    def start_command_handler(self, message: Message):
        self.bot.reply_to(message,
                          "Добро пожаловать в главное меню чат-бота для деловой переписке",
                          reply_markup=main_keyboard)

    def cooperation_offer_handler(self, message: Message):
        self.cooperation_offer_fsm.initialize(message)
        self.trigger('start-to-cooperation-offer')

    def guarantee_letter_handler(self, message: Message):
        self.guarantee_letter_fsm.initialize(message)
        self.trigger('start-to-guarantee-letter')

    def back_to_menu_handler(self, message: Message):
        self.start_command_handler(message)
        self.trigger('back-to-start')

    def run(self):
        self.bot.polling()


if __name__ == "__main__":
    bot = TelegramBotMainFSM()
    bot.run()
