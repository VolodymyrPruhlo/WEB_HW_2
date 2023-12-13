from abc import ABC, abstractmethod


class DisplayAdapter(ABC):
    @abstractmethod
    def display(self, data):
        pass


class InputAdapter(ABC):
    @abstractmethod
    def replace_input(self, data):
        pass


class ConsoleDisplayAdapter(DisplayAdapter):
    def display(self, data):
        print(data)


class UserInputAdapter(InputAdapter):
    def replace_input(self, data):
        return input(data)