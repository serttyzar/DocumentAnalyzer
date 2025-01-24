import argparse

class ArgsParser():
    """Парсер аргументов командной строки"""
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Генератор документов')
        self.parser.add_argument('-c', '--count', help='Кол-во документов', default=1)
        self.parser.add_argument('-o', '--output', help='Путь к директории для сохранения документов', default='docs')
        self.args = self.parser.parse_args()
        
    
    @property
    def count(self):
        return int(self.args.count)
    
    @property
    def output(self):
        return self.args.output