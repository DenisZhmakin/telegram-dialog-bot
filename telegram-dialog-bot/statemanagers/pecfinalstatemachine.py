from json import loads
from pathlib import Path
from typing import Callable

from telebot import TeleBot
from telebot.types import Message
from transitions import Machine

from keyboard import main_keyboard, start_keyboard, create_arrows_keyboard


class PecFinalStateMachine:
    def __init__(self, bot: TeleBot, p_trigger: Callable):
        self.data = loads(Path("data/proposal-to-expand-cooperation.json").read_text())

        transitions = [
            {'trigger': 'initialize', 'source': 'start', 'dest': 'step1'},
            {'trigger': 'step1-next', 'source': 'step1', 'dest': 'step2'},
            {'trigger': 'step1-previous', 'source': 'step1', 'dest': 'step1'},
            {'trigger': 'step2-next', 'source': 'step2', 'dest': 'step3'},
            {'trigger': 'step2-previous', 'source': 'step2', 'dest': 'step1'},
            {'trigger': 'step3-next', 'source': 'step3', 'dest': 'step4'},
            {'trigger': 'step3-previous', 'source': 'step3', 'dest': 'step2'},
            {'trigger': 'step4-next', 'source': 'step4', 'dest': 'step4'},
            {'trigger': 'step4-previous', 'source': 'step4', 'dest': 'step3'},
            {'trigger': 'back-to-start',
             'source': ['start', 'step1', 'step2', 'step3', 'step4', 'print'],
             'dest': 'start'}
        ]

        self.machine = Machine(model=self,
                               states=['start', 'step1', 'step2', 'step3', 'step4', 'print'],
                               transitions=transitions,
                               initial='start')

        self.p_trigger = p_trigger
        self.trigger = getattr(self, 'trigger')
        self.bot = bot

    def initialize(self, message: Message):
        self.trigger('back-to-start')
        self.bot.reply_to(message, "Добро пожаловать в режим `Предложение о расширении сотрудничества`.",
                          reply_markup=start_keyboard)

    def begin_button_handler(self, message: Message):
        self.trigger('initialize')
        self.show_keyboard(message)

    def next_button_handler(self, message: Message):
        self.trigger(f"{self.machine.get_model_state(self).name}-next")
        self.show_keyboard(message)

    def previous_button_handler(self, message: Message):
        self.trigger(f"{self.machine.get_model_state(self).name}-previous")
        self.show_keyboard(message)

    def update_button_handler(self, message: Message):
        self.bot.reply_to(message, self.machine.get_model_state(self).name)

    def show_keyboard(self, message: Message):
        state_name = self.machine.get_model_state(self).name
        description = [elem['description'] for elem in self.data if elem['step'] == state_name][0]

        self.bot.reply_to(message, description,
                          reply_markup=create_arrows_keyboard(description))

    def text_handler(self, message: Message):

        self.bot.reply_to(message, "Введенные данные сохранены")

    def back_to_menu_handler(self, message: Message):
        self.bot.reply_to(message,
                          "Вы вернулись в главное меню чат-бота для деловой переписке",
                          reply_markup=main_keyboard)
        self.p_trigger('back-to-start')
        self.trigger('back-to-start')
