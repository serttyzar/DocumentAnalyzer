from abc import ABC, abstractmethod


class LocaleStrategy(ABC):
    @abstractmethod
    def get_locale(self):
        pass