import argparse

class ArgsParser:
    """Парсер аргументов командной строки для извлечения и визуализации PDF-разметки."""
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='PDF Layout Extractor')
        
        self.parser.add_argument(
            '-i', '--input', 
            required=True, 
            help='Путь к входному PDF-файлу'
        )
        
        self.parser.add_argument(
            '-od', '--output_dir', 
            default='json', 
            help='Путь к директории для сохранения документов'
        )

        self.parser.add_argument(
            '-vd', '--visualization_dir', 
            default='visualizations', 
            help='Путь к директории для сохранения визуализаций'
        )

        self.parser.add_argument(
            '-p', '--pages', 
            type=int, 
            default=1, 
            help='Количество страниц для визуализации разметки'
        )
        
        self.args = self.parser.parse_args()
    
    @property
    def input(self):
        return self.args.input
    
    @property
    def pages_to_visualize(self):
        return self.args.pages
    
    @property
    def output_dir(self):
        return self.args.output_dir

    @property
    def visualization_dir(self):
        return self.args.visualization_dir
