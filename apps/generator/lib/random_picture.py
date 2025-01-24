import os
import random
from lib.random_chart import ChartGenerator

class RandomPictureGenerator:
    """Генератор случайных изображений"""
    def __init__(self, image_dir: str):
        self.image_dir = image_dir
        
    def get_random_image(self):
        """Возвращает случайное изображение из директории"""
        images = [os.path.join(self.image_dir, f) for f in os.listdir(self.image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        if images and random.choice([True, True, False, False, False]):
            return random.choice(images)
        return ChartGenerator.generate_random_chart()
    