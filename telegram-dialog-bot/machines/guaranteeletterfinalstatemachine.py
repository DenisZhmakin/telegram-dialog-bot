from io import BytesIO
from json import loads
from pathlib import Path
from typing import Callable

from docxtpl import DocxTemplate
from telebot import TeleBot
from telebot.types import Message
from transitions import Machine

from keyboard import start_keyboard, main_keyboard, create_arrows_keyboard, print_keyboard
from machines.abstractfinalstatemachine import AbstractFinalStateMachine


class GuaranteeLetterFinalStateMachine(AbstractFinalStateMachine):
    def __init__(self, bot: TeleBot, parent_trigger: Callable):
        self.data = loads(Path("data/letter-of-guarantee.json").read_text())

        transitions = [
            {'trigger': 'initialize', 'source': 'start', 'dest': 'step1'},
            {'trigger': 'step1-next', 'source': 'step1', 'dest': 'step2'},
            {'trigger': 'step1-previous', 'source': 'step1', 'dest': 'step1'},
            {'trigger': 'step2-next', 'source': 'step2', 'dest': 'step3'},
            {'trigger': 'step2-previous', 'source': 'step2', 'dest': 'step1'},
            {'trigger': 'step3-next', 'source': 'step3', 'dest': 'step4'},
            {'trigger': 'step3-previous', 'source': 'step3', 'dest': 'step2'},
            {'trigger': 'step4-next', 'source': 'step4', 'dest': 'step5'},
            {'trigger': 'step4-previous', 'source': 'step4', 'dest': 'step3'},
            {'trigger': 'step5-next', 'source': 'step5', 'dest': 'print'},
            {'trigger': 'step5-previous', 'source': 'step5', 'dest': 'step4'},
            {'trigger': 'back-to-start',
             'source': ['start', 'step1', 'step2', 'step3', 'step4', 'step5', 'print'],
             'dest': 'start'}
        ]

        self.machine = Machine(model=self,
                               states=['start', 'step1', 'step2', 'step3', 'step4', 'step5', 'print'],
                               transitions=transitions,
                               initial='start')

        self.parent_trigger = parent_trigger
        self.trigger = getattr(self, 'trigger')
        self.bot = bot

    def initialize(self, message: Message):
        self.bot.reply_to(message, "Добро пожаловать в режим `Формирование гарантийного письма от организации`.",
                          reply_markup=start_keyboard)
        self.trigger('back-to-start')

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
        self.show_keyboard(message)

    def show_keyboard(self, message: Message):
        state_name = self.machine.get_model_state(self).name

        if state_name == "print":
            description = "Все данные для шаблоны собраны, нажмите кнопку `Печать`, чтобы получить документ."
            keyboard = print_keyboard
        else:
            description = [elem['description'] for elem in self.data if elem['step'] == state_name][0]
            keyboard = create_arrows_keyboard(description)

        self.bot.reply_to(message, description, reply_markup=keyboard)

    def text_handler(self, message: Message):
        for elem in self.data:
            if elem['step'] == self.machine.get_model_state(self).name:
                elem['value'] = message.text
        self.trigger(f"{self.machine.get_model_state(self).name}-next")
        self.show_keyboard(message)

    def print_document(self, message: Message):
        document = DocxTemplate("files/letter-of-guarantee.docx")

        context = {}

        for elem in self.data:
            context[elem['template_var']] = elem['value']

        document.render(context)

        file = BytesIO()
        file.name = 'Гарантийное письмо.docx'
        document.save(file)
        file.seek(0)

        self.bot.send_document(message.chat.id, file)

    def back_to_menu_handler(self, message: Message):
        self.bot.reply_to(message,
                          "Вы вернулись в главное меню чат-бота для деловой переписке",
                          reply_markup=main_keyboard)
        self.parent_trigger('back-to-start')
        self.trigger('back-to-start')
