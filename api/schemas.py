from pydantic import BaseModel
from typing import List

class Detection(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float
    class_id: int
    confidence: float
    class_name: str

class ResponseModel(BaseModel):
    detections: List[Detection]
