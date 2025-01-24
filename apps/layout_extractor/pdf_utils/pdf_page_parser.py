from fitz import Page
import pandas as pd
import re

class PDFPageParser:
    def __init__(self, classifier):
        self.classifier = classifier
    
    def parse(self, page: Page):
        page_data = {
            "image_height": int(page.rect.height),
            "image_width": int(page.rect.width),
            "title": [],
            "paragraph": [],
            "table": [],
            "picture": [],
            "formula": [],
            "table_signature": [],
            "picture_signature": [],
            "formula_signature": [],
            "numbered_list": [],
            "marked_list": [],
            "footer": [],
        }
        table_coords = self.extract_tables(page, page_data)
        image_coords = self.extract_images(page, page_data)
        self.extract_text_blocks(page, page_data, table_coords + image_coords)
        return page_data
    
    def extract_tables(self, page, page_data):
        table_coords = []
        for table in page.find_tables():
            table_bbox = table.bbox
            pd_table = table.to_pandas()
            rows_cnt = 0
            for col_name, col_data in pd_table.items():
                if not any(col_data.isna()) or not bool(re.match(r'Col', col_name)):
                    rows_cnt += 1
            if rows_cnt <= 3:
                self.parse_table_on_columns(page_data, rows_cnt, table_bbox)
            else:
                page_data['table'].append(table_bbox)
            table_coords.append(table_bbox)
        return table_coords
    
    def extract_text_blocks(self, page, page_data, table_coords):
        """Извлекает текстовые блоки из страницы PDF, группируя последовательные блоки одного типа."""
        text_blocks = []
        blocks = page.get_text("dict", sort=True)["blocks"]
        page_data["footer"].append(blocks[0]["bbox"])
        page_data["footer"].append(blocks[-1]["bbox"])

        current_type = None
        current_block = [None, None, None, None]

        for block in blocks[1:-1]:
            if "lines" in block:
                text = "\n".join([span["text"] for line in block["lines"] for span in line["spans"]]).strip()
                bbox = block["bbox"]
                spans = [span for line in block["lines"] for span in line["spans"]]

                if any(self.is_bbox_in_table(bbox, coords) for coords in table_coords):
                    if current_type is not None and current_block[0] is not None:
                        #page_data[current_type].append(current_block)
                        text_blocks.append([current_type, current_block])
                    current_block = [None, None, None, None]
                    current_type = None
                    continue

                block_type = self.classifier.classify(text, spans)

                if text == '':
                    continue

                if current_type != block_type or block_type in ['formula_signature', 'picture_signature', 'table_signature'] \
                    or any(self.is_bbox_in_table(self.update_bbox(current_block, bbox), coords) for coords in table_coords):
                    if current_type is not None and current_block[2] - current_block[0] > 10:
                        #page_data[current_type].append(current_block)
                        text_blocks.append([current_type, current_block])
                    current_block = [None, None, None, None]
                    current_type = block_type
                current_block = self.update_bbox(current_block, bbox)

        if current_type and current_block[2] - current_block[0] > 10:
            #page_data[current_type].append(current_block)
            text_blocks.append([current_type, current_block])


        # Объединение блоков списков
        def merge_list_blocks(page_data, text_blocks):
            i = 0
            final_blocks = []
            threshold = 20
            while i < len(text_blocks):
                if text_blocks[i][0] == 'numbered_list':
                    j = i
                    new_block = text_blocks[i]
                    while j + 1 < len(text_blocks):
                        j += 1
                        if text_blocks[j][0] == 'paragraph':
                            if text_blocks[j][1][0] > new_block[1][0]:
                                new_block = [new_block[0], self.update_bbox(new_block[1], text_blocks[j][1])]
                            else:
                                final_blocks.append(new_block)
                                i = j
                                break
                        elif text_blocks[i][0] == 'numbered_list':
                            if text_blocks[j][1][0] - new_block[1][1] < threshold:
                                new_block = [new_block[0], self.update_bbox(new_block[1], text_blocks[j][1])]
                            else:
                                final_blocks.append(new_block)
                                i = j
                                break
                        else:
                            final_blocks.append(new_block)
                            i = j
                            break
                    else:
                        final_blocks.append(new_block)
                        i = j + 1 
                elif text_blocks[i][0] == 'marked_list':
                    j = i
                    new_block = text_blocks[i]
                    while j + 1 < len(text_blocks):
                        j += 1
                        if text_blocks[j][0] == 'paragraph':
                            if text_blocks[j][1][0] > new_block[1][0]:
                                new_block = [new_block[0], self.update_bbox(new_block[1], text_blocks[j][1])]
                            else:
                                final_blocks.append(new_block)
                                i = j
                                break
                        elif text_blocks[i][0] == 'marked_list':
                            if text_blocks[j][1][0] - new_block[1][1] < threshold:
                                new_block = [new_block[0], self.update_bbox(new_block[1], text_blocks[j][1])]
                            else:
                                final_blocks.append(new_block)
                                i = j
                                break
                        else:
                            final_blocks.append(new_block)
                            i = j
                            break   
                    else:
                        final_blocks.append(new_block)
                        i = j + 1     
                else:
                    final_blocks.append(text_blocks[i])
                    i += 1
            for type, bbox in final_blocks:
                page_data[type].append(bbox)

        merge_list_blocks(page_data, text_blocks)

        # перемещение формул из картинок
        for el in page_data["picture"]:
            x0, y0, x1, y1 = el
            check = False
            if len(page_data["picture_signature"]) == 0:
                page_data["formula"].append(el)
            else:
                for image_sign in page_data["picture_signature"]:
                    ix0, iy0, ix1, iy1 = image_sign
                    if y1 + 25 > iy0 or y0 - 25 < iy1 and not check:
                        break
                    else:
                        page_data["formula"].append(el)
                        check = True
                    
                for formula_sign in page_data["formula_signature"]:
                    ix0, iy0, ix1, iy1 = formula_sign
                    if y1 + 25 > iy0 and y0 < iy1 and not check:
                        page_data["formula"].append(el)
                    else:
                        break

        # Удаление элементов из "picture", которые находятся в "formula"
        if len(page_data["picture"]) > 0:
            for i in range(len(page_data["picture"]) - 1, -1, -1):  
                if page_data["picture"][i] in page_data["formula"]:
                    del page_data["picture"][i]

    def update_bbox(self, current_bbox, new_bbox):
        """Обновляет объединенные координаты bbox для текущего блока."""
        x0, y0, x1, y1 = current_bbox
        nx0, ny0, nx1, ny1 = new_bbox
        if x0 is None:
            return [nx0, ny0, nx1, ny1]
        return [min(x0, nx0), min(y0, ny0), max(x1, nx1), max(y1, ny1)]

    def extract_images(self, page, page_data):
        image_coords = []
        for image in page.get_image_info():
            page_data['picture'].append([*image['bbox']])
            image_coords.append(image['bbox'])
        return image_coords
    
    def parse_table_on_columns(self, page_data, columns, bbox):
        x0, y0, x1, y1 = bbox
        distance = (x1 - x0) / columns
        for i in range(columns):
            page_data['paragraph'].append((x0 + distance * i, y0, x0 + distance * (i + 1), y1))

    def is_bbox_in_table(self, bbox, table_bbox):
        return not (bbox[2] < table_bbox[0] or bbox[0] > table_bbox[2] or bbox[3] <= table_bbox[1] or bbox[1] >= table_bbox[3])