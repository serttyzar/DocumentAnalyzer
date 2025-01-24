import random

from localization.locale_strategy import LocaleStrategy

class FakerLocaleStrategy(LocaleStrategy):
    def get_locale(self):
        return random.choice(['en_US', 'ru_RU'])