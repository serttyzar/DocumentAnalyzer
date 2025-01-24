import json
from PIL import Image, ImageDraw

# Шаг 1: Загрузка изображения
image_path = "pdf_images/file_1_page_1.png"  # Укажите путь к вашей картинке
image = Image.open(image_path)

# Шаг 2: Загрузка координат из JSON
json_path = "json/1/page_1.json"  # Укажите путь к вашему JSON файлу
with open(json_path, 'r') as file:
    rectangles = json.load(file)  # Ожидается, что это будет список словарей с координатами

# Шаг 3: Рисуем прямоугольники
draw = ImageDraw.Draw(image)
print(rectangles.values())
scale_w = 3301 / 792
scale_h = 2550 / 612
for rects in list(rectangles.values())[2:]:
    for rect in rects:
        x1, y1, x2, y2 = scale_w * rect[0], scale_h * rect[1], scale_w * rect[2], scale_h * rect[3]
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)  # Рисуем прямоугольник

# Шаг 4: Сохраняем изображение с прямоугольниками
output_path = "check_visualisations/1.png"  # Укажите путь для сохранения
image.save(output_path)

print(f"Изображение сохранено в {output_path}")
