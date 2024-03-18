import os
from typing import Optional

import telebot
from dotenv import load_dotenv
from telebot.types import Message
from transitions import Machine

from keyboard import main_keyboard
from defaultfinalstatemachine import DefaultFinalStateMachine

from machines.abstractfinalstatemachine import AbstractFinalStateMachine
from machines.confirmationletterfinalstatemachine import ConfirmationLetterFinalStateMachine
from machines.cooperationofferfinalstatemachine import CooperationOfferFinalStateMachine
from machines.coverletterfinalstatemachine import CoverLetterFinalStateMachine
from machines.guaranteeletterfinalstatemachine import GuaranteeLetterFinalStateMachine
from machines.invitationletterfinalstatemachine import InvitationLetterFinalStateMachine
from machines.recommendationletterfinalstatemachine import RecommendationLetterFinalStateMachine


class TelegramBotMainFSM:
    def __init__(self):
        load_dotenv()
        self.bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])

        @self.bot.message_handler(func=lambda msg: msg.text == "Формирование предложения о сотрудничестве")
        def cooperation_offer_wrapper(message: Message):
            self.cooperation_offer_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Формирование гарантийного письма от организации")
        def guarantee_letter_wrapper(message: Message):
            self.guarantee_letter_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Формирование рекомендательного письма для сотрудника")
        def recommendation_letter_wrapper(message: Message):
            self.recommendation_letter_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Формирование письма подтверждения от компании")
        def confirmation_letter_wrapper(message: Message):
            self.confirmation_letter_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Формирование сопроводительного письма")
        def cover_letter_wrapper(message: Message):
            self.cover_letter_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Формирование письма приглашения")
        def invitation_letter_wrapper(message: Message):
            self.invitation_letter_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Начать")
        def begin_button_wrapper(message: Message):
            self.get_current_fsm().begin_button_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Далее")
        def next_button_wrapper(message: Message):
            self.get_current_fsm().next_button_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Назад")
        def previous_button_wrapper(message: Message):
            self.get_current_fsm().previous_button_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Обновить")
        def update_button_wrapper(message: Message):
            self.get_current_fsm().update_button_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Назад в меню")
        def back_to_menu_wrapper(message: Message):
            self.get_current_fsm().back_to_menu_handler(message)

        @self.bot.message_handler(func=lambda msg: msg.text == "Печать")
        def print_document_wrapper(message: Message):
            self.get_current_fsm().print_document(message)

        @self.bot.message_handler(commands=['start'])
        @self.bot.message_handler(content_types=['text'])
        def start_and_text_handler(message: Message):
            if message.text == '/start':
                self.bot.reply_to(message,
                                  "Добро пожаловать в главное меню чат-бота для деловой переписке",
                                  reply_markup=main_keyboard)
            else:
                self.get_current_fsm().text_handler(message)

        transitions = [
            {'trigger': 'start-to-cooperation-offer', 'source': 'start', 'dest': 'cooperation-offer'},
            {'trigger': 'start-to-guarantee-letter', 'source': 'start', 'dest': 'guarantee-letter'},
            {'trigger': 'start-to-recommendation-letter', 'source': 'start', 'dest': 'recommendation-letter'},
            {'trigger': 'start-to-confirmation-letter', 'source': 'start', 'dest': 'confirmation-letter'},
            {'trigger': 'start-to-invitation-letter', 'source': 'start', 'dest': 'invitation-letter'},
            {'trigger': 'start-to-cover-letter', 'source': 'start', 'dest': 'cover-letter'},
            {'trigger': 'back-to-start',
             'source': [
                 'start',
                 'cooperation-offer',
                 'guarantee-letter',
                 'recommendation-letter',
                 'confirmation-letter',
                 'invitation-letter',
                 'cover-letter'
             ],
             'dest': 'start'},
        ]

        self.machine = Machine(model=self,
                               states=[
                                   'start',
                                   'cooperation-offer',
                                   'guarantee-letter',
                                   'recommendation-letter',
                                   'confirmation-letter',
                                   'invitation-letter',
                                   'cover-letter'
                               ],
                               transitions=transitions,
                               initial='start')

        self.default_fsm = DefaultFinalStateMachine(self.bot, getattr(self, 'trigger'))

        self.cooperation_offer_fsm = CooperationOfferFinalStateMachine(self.bot, getattr(self, 'trigger'))
        self.guarantee_letter_fsm = GuaranteeLetterFinalStateMachine(self.bot, getattr(self, 'trigger'))
        self.recommendation_letter_fsm = RecommendationLetterFinalStateMachine(self.bot, getattr(self, 'trigger'))
        self.confirmation_letter_fsm = ConfirmationLetterFinalStateMachine(self.bot, getattr(self, 'trigger'))
        self.invitation_letter_fsm = InvitationLetterFinalStateMachine(self.bot, getattr(self, 'trigger'))
        self.cover_letter_fsm = CoverLetterFinalStateMachine(self.bot, getattr(self, 'trigger'))

        self.trigger = getattr(self, 'trigger')

    def get_current_fsm(self) -> Optional[AbstractFinalStateMachine]:
        if self.machine.get_model_state(self).name == 'cooperation-offer':
            return self.cooperation_offer_fsm
        elif self.machine.get_model_state(self).name == 'guarantee-letter':
            return self.guarantee_letter_fsm
        elif self.machine.get_model_state(self).name == 'recommendation-letter':
            return self.recommendation_letter_fsm
        elif self.machine.get_model_state(self).name == 'confirmation-letter':
            return self.confirmation_letter_fsm
        elif self.machine.get_model_state(self).name == 'invitation-letter':
            return self.invitation_letter_fsm
        elif self.machine.get_model_state(self).name == 'cover-letter':
            return self.cover_letter_fsm
        else:
            return self.default_fsm

    def cooperation_offer_handler(self, message: Message):
        self.cooperation_offer_fsm.initialize(message)
        self.trigger('start-to-cooperation-offer')

    def guarantee_letter_handler(self, message: Message):
        self.guarantee_letter_fsm.initialize(message)
        self.trigger('start-to-guarantee-letter')

    def recommendation_letter_handler(self, message: Message):
        self.recommendation_letter_fsm.initialize(message)
        self.trigger('start-to-recommendation-letter')

    def confirmation_letter_handler(self, message: Message):
        self.confirmation_letter_fsm.initialize(message)
        self.trigger('start-to-confirmation-letter')

    def cover_letter_handler(self, message: Message):
        self.cover_letter_fsm.initialize(message)
        self.trigger('start-to-cover-letter')

    def invitation_letter_handler(self, message: Message):
        self.invitation_letter_fsm.initialize(message)
        self.trigger('start-to-invitation-letter')

    def run(self):
        self.bot.polling()


if __name__ == "__main__":
    bot = TelegramBotMainFSM()
    bot.run()
