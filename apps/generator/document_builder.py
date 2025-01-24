import random
from re import L
from typing import Dict
from docx import Document
from generators import ContentGenerator, FootnoteGenerator, TextGenerator, ListGenerator, FormulaGenerator, HeadingGenerator, TableGenerator, ImageGenerator, HeaderFooterGenerator, FormulaImageGenerator
from lib.random_picture import RandomPictureGenerator
from localization import LocaleStrategy


class DocumentBuilder:
    """Билдер для генерации документа"""
    generators: Dict[str, ContentGenerator]
    
    paragraph_font_size = random.randint(8, 16)
    heading_font_size = paragraph_font_size + random.randint(2, 5)
    image_font_size = paragraph_font_size - random.choice([0, 1, 1, 1, 2, 2, 2, 3])
    table_font_size = paragraph_font_size - random.choice([0, 1, 2])
    
    def __init__(self, document: Document, locale_strategies: Dict[str, LocaleStrategy], picture_generator: RandomPictureGenerator) -> None:
        self.document = document
        self.locale_strategies = locale_strategies
        self.picture_generator = picture_generator
        self.generators = {
                   "text": TextGenerator(font_size=self.paragraph_font_size, locale_strategy=self.locale_strategies['faker']),
                   "heading": HeadingGenerator(font_size=self.heading_font_size, locale_strategy=self.locale_strategies['faker']),
                   "table": TableGenerator(font_size=self.table_font_size, locale_strategy=self.locale_strategies['mimesis']),
                   "image": ImageGenerator(font_size=self.image_font_size, locale_strategy=self.locale_strategies['faker'], picture_generator=self.picture_generator),
                   "list": ListGenerator(font_size=self.paragraph_font_size, locale_strategy=self.locale_strategies['faker']),
                   "formula": FormulaGenerator(font_size=self.paragraph_font_size, locale_strategy=self.locale_strategies['faker']),
                   "footnote": FootnoteGenerator(font_size=self.paragraph_font_size, locale_strategy=self.locale_strategies['faker']),
                   "header_footer": HeaderFooterGenerator(font_size=self.paragraph_font_size, locale_strategy=self.locale_strategies['faker']),
                   "formula_image": FormulaImageGenerator(font_size=self.paragraph_font_size, locale_strategy=self.locale_strategies['faker'])
        }
    def add_element(self, element_type):
        """Добавляет (генерирует) элемент в документ"""
        generator = self.generators[element_type]
        generator.generate(self.document)
        
    def build(self):
        """Собирает документ"""
        self.generators['header_footer'].generate(self.document)
        return self.document