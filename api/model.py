from ultralytics import YOLO
import torch

class ImageModel:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def process_image(self, image_path: str) -> dict:
        results = self.model(image_path)
        result = results[0]

        boxes = result.boxes
        class_names = result.names
        detections = []

        for box in boxes:
            try:
                if isinstance(box.xyxy, torch.Tensor):
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                else:
                    x1, y1, x2, y2 = box.xyxy[0]

                class_id = int(box.cls[0])
                confidence = box.conf[0].item() if isinstance(box.conf, torch.Tensor) else box.conf[0]
                detections.append({
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

        return {"detections": detections}
