import os
from docx2pdf import convert
import pypdfium2 as pdfium

# Входная и выходная директории
input_dir = "C:\\Users\\burce\\DocumentAlalyzer\\dataset_yolo\\for_predict\\dip"
pdf_output_dir = "C:\\Users\\burce\\DocumentAlalyzer\\dataset_yolo\\for_predict\\dip"
image_output_dir = "C:\\Users\\burce\\DocumentAlalyzer\\dataset_yolo\\for_predict\\dip"

# Создаем выходные директории, если их нет
if not os.path.exists(pdf_output_dir):
    os.makedirs(pdf_output_dir)

if not os.path.exists(image_output_dir):
    os.makedirs(image_output_dir)

# Перебираем все файлы в входной директории
for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        # docx_path = os.path.join(input_dir, filename)
        pdf_path = os.path.join(pdf_output_dir, f"{os.path.splitext(filename)[0]}.pdf")
        
        # Конвертируем DOCX в PDF
        # convert(docx_path, pdf_path)
        # print(f"Сконвертирован: {filename} -> {pdf_path}")

        # Открываем PDF и сохраняем каждую страницу как изображение
        pdf = pdfium.PdfDocument(pdf_path)
        for i, page in enumerate(pdf):
            # Рендеринг страницы с указанным разрешением (300 dpi)
            pdf_bitmap = page.render(300/72)  # Убрали color
            pil_image = pdf_bitmap.to_pil()  # Конвертируем в PIL Image для сохранения

            # Сохраняем изображение страницы
            image_filename = f"{os.path.splitext(filename)[0]}_{i + 1}.png"
            image_path = os.path.join(image_output_dir, image_filename)
            pil_image.save(image_path, "PNG")
            print(f"Страница {i + 1} сохранена как изображение: {image_path}")

print("Конвертация завершена!")
