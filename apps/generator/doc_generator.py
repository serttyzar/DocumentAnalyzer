import random

from docx import Document
from docx.enum.section import WD_ORIENT
from uuid import uuid4
from functools import partial
from multiprocessing import Pool
from tqdm import tqdm
from document_builder import DocumentBuilder
from localization.faker_locale_strategy import FakerLocaleStrategy
from localization.mimesis_locale_strategy import MimesisLocaleStrategy
from lib.random_picture import RandomPictureGenerator

class DocumentGenerator():
    element_weights = {
            "text": 1.0,
            "heading": 1.0,
            "table": 1.0,
            "image": 1.0,
            "list": 1.0,
            # "formula": 1.0,
            "footnote": 1.0,
            "formula_image": 1.0
    }
    
    """Генератор документов"""
    def __init__(self):
        self.document = Document()
        self.locale_strategies = {
            "faker": FakerLocaleStrategy(),
            "mimesis": MimesisLocaleStrategy(),
        }
        self.picture_generator = RandomPictureGenerator(image_dir='images')
        self.builder = DocumentBuilder(
            document=self.document,
            locale_strategies=self.locale_strategies,
            picture_generator=self.picture_generator)
        
    def create_document(self, file_name):
        """Создает документ"""

        self.set_orientation()
        num_elements = random.randint(10, 25)

        for _ in range(num_elements):
            element_type = self.choose_element_type()
            self.builder.add_element(element_type)
        
        self.document = self.builder.build()
        self.document.save(file_name)
    
    def choose_element_type(self):
        chosen_type = random.choices(
            population=list(self.element_weights.keys()),
            weights=list(self.element_weights.values()), 
            k=1
        )[0]
        
        self.element_weights[chosen_type] = max(0.1, self.element_weights[chosen_type] * 0.7)
        
        return chosen_type

    def set_orientation(self):
        """Устанавливает ориентацию страницы и количество колонок"""

        section = self.document.sections[0]
        if random.choice([True, False]):
            section.orientation = WD_ORIENT.LANDSCAPE
            section.page_width, section.page_height = section.page_height, section.page_width       

        if random.choice([True, False]):
            section.columns = 2

def generate_single_document(output_folder: str, _):
    """Генерирует один документ"""
    generator = DocumentGenerator()
    generator.create_document(f'{output_folder}/{uuid4()}.docx')
    
def generate_multiple_documents(count: int, output_folder: str):
    """Генерирует несколько документов параллельно"""
    print(f"Генерация {count} документов")
    with Pool() as pool:
        generate_doc = partial(generate_single_document, output_folder)
        list(tqdm(
            pool.imap(generate_doc, range(count)),
            total=count,
            desc="Генерация документов",
            unit="док."
        ))