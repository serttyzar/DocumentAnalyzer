
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import io
import os
import json

class PDFVisualizer:
    def __init__(self, document):
        self.document = document
    
    def visualize_page(self, page_num):
        page = self.document.get_page(page_num)
        json_path = os.path.join(self.document.document_folder, f"page_{page_num + 1}.json")
        with open(json_path, "r", encoding="utf-8") as f:
            page_data = json.load(f)

        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        
        plt.figure(figsize=(10, 10))
        plt.imshow(img, aspect="auto")

        colors = {
            "title": "red", "paragraph": "blue", "table": "green", "picture": "purple", "formula": "lime",
            "table_signature": "orange", "picture_signature": "yellow", "formula_signature": "coral",
            "numbered_list": "brown", "marked_list": "cyan", "footer": "gray"
        }

        for key, color in colors.items():
            for coords in page_data.get(key, []):
                x0, y0, x1, y1 = coords
                rect = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, linewidth=1, edgecolor=color, facecolor="none")
                plt.gca().add_patch(rect)

        output_image_path = os.path.join(self.document.visualization_folder, f"page_{page_num + 1}_visualization.png")
        plt.savefig(output_image_path)
        plt.close()
        print(f"Image for page {page_num + 1} saved at {output_image_path}")
