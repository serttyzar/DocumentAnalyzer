import random

from mimesis.locales import Locale
from localization.locale_strategy import LocaleStrategy


class MimesisLocaleStrategy(LocaleStrategy):
    def get_locale(self):
        return random.choice([Locale.EN, Locale.RU])