import shutil
from pathlib import Path

UPLOAD_FOLDER = Path("uploaded_images")
UPLOAD_FOLDER.mkdir(exist_ok=True)

def save_image(file) -> str:
    """
    Сохраняет файл на диск и возвращает путь.
    """
    file_path = UPLOAD_FOLDER / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return str(file_path)
