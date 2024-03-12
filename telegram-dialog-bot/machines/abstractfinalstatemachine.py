from abc import ABC, abstractmethod

from telebot.types import Message


class AbstractFinalStateMachine(ABC):
    @abstractmethod
    def initialize(self, message: Message):
        pass

    @abstractmethod
    def begin_button_handler(self, message: Message):
        pass

    @abstractmethod
    def next_button_handler(self, message: Message):
        pass

    @abstractmethod
    def previous_button_handler(self, message: Message):
        pass

    @abstractmethod
    def update_button_handler(self, message: Message):
        pass

    @abstractmethod
    def print_document(self, message: Message):
        pass

    @abstractmethod
    def show_keyboard(self, message: Message):
        pass

    @abstractmethod
    def text_handler(self, message: Message):
        pass

    @abstractmethod
    def back_to_menu_handler(self, message: Message):
        pass

