from fastapi import FastAPI, File, UploadFile, HTTPException
from api.model import ImageModel
from api.utils import save_image
from api.schemas import ResponseModel

app = FastAPI(
    title="YOLOv10 Image Detection API",
    description="API для детекции объектов с использованием модели YOLOv10",
    version="1.0.0"
)

MODEL_PATH = "models/epoch100.pt"

model = ImageModel(model_path=MODEL_PATH)

@app.post("/detect", response_model=ResponseModel)
async def detect_objects(file: UploadFile = File(...)):
    """
    Загружает изображение, выполняет детекцию объектов и возвращает результаты.
    """
    if not file.filename.endswith(("jpg", "jpeg", "png")):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    image_path = save_image(file)
    result = model.process_image(image_path)

    return ResponseModel(detections=result["detections"])
