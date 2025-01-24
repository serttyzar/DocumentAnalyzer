import random
from faker import Faker
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from generators.generator import ContentGenerator
from localization.locale_strategy import LocaleStrategy


class HeadingGenerator(ContentGenerator):
    def __init__(self, font_size, locale_strategy):
        self.font_size = font_size
        self.locale_strategy: LocaleStrategy = locale_strategy
        
    def generate(self, document):
        fake = Faker(self.locale_strategy.get_locale())
        level = random.randint(1, 3)

        text = fake.sentence()
        title = document.add_heading(level=level)
        run = title.add_run(text)
        
        if random.choice([True, False]):
            run.bold = True
        if random.choice([True, False]):
            run.italic = True 

        run.font.size = Pt(self.font_size) 
        colors = [(0x3F, 0x2C, 0x36), (0x0, 0x0, 0x0), 
                                            (0x0, 0x0, 0x8B), (0x87, 0xCE, 0xFA)]

        run.font.color.rgb = RGBColor(*random.choice(colors))
        title.alignment =  random.choices([WD_PARAGRAPH_ALIGNMENT.CENTER, WD_PARAGRAPH_ALIGNMENT.LEFT, WD_PARAGRAPH_ALIGNMENT.RIGHT], weights=[0.8, 0.1, 0.1])[0]