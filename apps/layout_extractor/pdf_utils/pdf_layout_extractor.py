# pdf_processing/PDFLayoutExtractor.py

from .pdf_document import PDFDocument
from .pdf_block_classifier import PDFBlockClassifier
from .pdf_page_parser import PDFPageParser
from .pdf_visualizer import PDFVisualizer

class PDFLayoutExtractor:
    def __init__(self, file_path, output_dir, visualize_dir):
        self.document = PDFDocument(file_path, output_dir, visualize_dir)
        self.classifier = PDFBlockClassifier()
        self.parser = PDFPageParser(self.classifier)
        self.visualizer = PDFVisualizer(self.document)
    
    def extract_layout(self):
        for page_num in range(1, self.document.get_page_count()):
            page = self.document.get_page(page_num)
            if page is not None:
                page_data = self.parser.parse(page)
                self.document.save_json(page_data, page_num)
            else:
                print(f"Пропуск страницы {page_num} из-за ошибки загрузки.")
        
    def visualize_pages(self, num_pages):
        for i in range(num_pages):
            self.visualizer.visualize_page(i)
    
    def close_document(self):
        """Закрывает PDF-документ."""
        self.document.close()
