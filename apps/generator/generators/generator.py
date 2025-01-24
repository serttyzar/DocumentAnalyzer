from abc import ABC, abstractmethod

class ContentGenerator(ABC):
    """Абстрактный класс для элементов генерации контента"""
    
    @abstractmethod
    def generate(self, document):
        pass