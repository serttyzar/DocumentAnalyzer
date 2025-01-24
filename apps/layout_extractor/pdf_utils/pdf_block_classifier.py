import re

class PDFBlockClassifier:
    def classify(self, text, spans):
        if self.is_numbered_list(text):
            return 'numbered_list'
        elif self.is_marked_list(text):
            return 'marked_list'
        elif self.is_table_signature(text):
            return 'table_signature'
        elif self.is_picture_signature(text):
            return 'picture_signature'
        elif self.is_formula_signature(text):
            return 'formula_signature'
        elif self.is_title(text, spans):
            return 'title'
        else:
            return 'paragraph'
    
    def is_numbered_list(self, text):
        return bool(re.match(r'^\d+\.\s', text))
    
    def is_marked_list(self, text):
        return bool(re.match(r'^(?:\uf0b7|•)\s', text))

    def is_table_signature(self, text):
        return bool(re.match(r'^\s*(Табл\. \d+|Таблица \d+ -|Таблица\.)', text))
    
    def is_picture_signature(self, text):
        return bool(re.match(r'^\s*(Рис\.|Рисунок)\s*\d+', text))
    
    def is_title(self, text, spans):
        return any('Bold' in span['font'] or 'Italic' in span['font'] for span in spans)

    def is_formula_signature(self, text):
        return bool(re.match(r'^\s*Формула\s*\d+', text))