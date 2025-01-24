from ultralytics import YOLO
import json
import torch

# Загружаем модель
try:
    model = YOLO('models/best.pt')
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Выполняем инференс на изображении
try:
    results = model('pdf_images/file_1_page_1.png')
except Exception as e:
    print(f"Error performing inference: {e}")
    exit()

# Получаем первый результат из списка (если их несколько)
if not results:
    print("No results returned from the model.")
    exit()

result = results[0]

# Получаем коробки (детекции) и метки классов
boxes = result.boxes  # Список объектов Boxes

# Получаем имена классов из result.names
class_names = result.names

# Массив для хранения детекций
detections_json = []

# Перебираем все детекции
for box in boxes:
    try:
        # Получаем координаты bounding box
        if isinstance(box.xyxy, torch.Tensor):
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        else:
            x1, y1, x2, y2 = box.xyxy[0]
        
        # Получаем идентификатор класса
        class_id = int(box.cls[0])
        
        # Получаем уверенность модели
        if isinstance(box.conf, torch.Tensor):
            confidence = box.conf[0].item()
        else:
            confidence = box.conf[0]
        
        # Добавляем детекцию в список
        detections_json.append({
            'x1': float(x1),
            'y1': float(y1),
            'x2': float(x2),
            'y2': float(y2),
            'class_id': class_id,
            'confidence': float(confidence),
            'class_name': class_names.get(class_id, 'Unknown')
        })
    except Exception as e:
        print(f"Error processing box: {e}")
        continue

# Преобразуем список в JSON строку
try:
    results_json = json.dumps(detections_json, indent=4)
except Exception as e:
    print(f"Error converting to JSON: {e}")
    exit()

# Выводим результаты
print(results_json)