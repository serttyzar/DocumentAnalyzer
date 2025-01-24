import os
import json
import fitz  # PyMuPDF

class PDFDocument:
    """Управляет PDF-документом и папками для сохранения выходных данных."""
    
    def __init__(self, file_path, output_json_folder="json", output_vis_folder="visualizations"):
        self.file_path = file_path
        document_name = os.path.splitext(os.path.basename(file_path))[0]
        self.document_folder = os.path.join(output_json_folder, document_name)
        self.visualization_folder = os.path.join(output_vis_folder, document_name)
        os.makedirs(self.document_folder, exist_ok=True)
        os.makedirs(self.visualization_folder, exist_ok=True)
        self.doc = fitz.open(self.file_path)  # Открываем PDF один раз для всех страниц
    
    def get_page_count(self):
        """Возвращает количество страниц в PDF."""
        return self.doc.page_count
    
    def save_json(self, data, page_num):
        """Сохраняет данные страницы в JSON файл."""
        output_file = os.path.join(self.document_folder, f"page_{page_num + 1}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def get_page(self, page_num):
        """Возвращает страницу из PDF, если она существует."""
        if page_num < 0 or page_num >= self.get_page_count():
            raise IndexError(f"Номер страницы {page_num} вне диапазона.")
        try:
            page = self.doc[page_num]
            if page is None:
                raise ValueError(f"Не удалось получить страницу {page_num}")
            return page
        except Exception as e:
            print(f"Ошибка при доступе к странице {page_num}: {e}")
            return None
    
    def close(self):
        """Закрывает PDF-документ."""
        self.doc.close()
