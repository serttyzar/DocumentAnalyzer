# Детекция элементов документов 

### Пронин Никита Андреевич  
### Петров Илья Денисович  

---

## Суть проекта  
**Глобальная задача**: разработать детектор элементов документа по картинке  

### Подзадачи:  
1. Создать генератор документов (`docx` или `pdf`) для получения обучающей выборки  
2. Сформировать из документов набор данных: картинки и координатную разметку к ним  
3. Обучить модель на этих данных  

---

## **doc_generator**  
В целях генерации датасета была создана структура классов, а также консольная утилита для запуска скрипта.

![Слайд 3](Слайд3.png)

### Особенности решения:
- Рандомная генерация с убывающей вероятностью появления для каждого класса  
- Разнообразные формулы  
- Картинки из датасета в 3000 изображений ([ссылка на датасет](https://www.kaggle.com/datasets/pankajkumar2002/random-image-sample-dataset))  
- Генерация графиков с помощью `matplotlib`  
- Код структурирован по модулям  
- Эффективная генерация документов с использованием нескольких ядер процессора  

---

## **layout_extractor**  
В целях разметки датасета была создана структура классов и консольная утилита.

![Слайд 4](Слайд4.png)

### Особенности решения:
- Выделение всех заданных классов с почти стопроцентной точностью  
- Использование библиотеки `PyMuPdf` вместо предложенной в техническом задании  
- Возможность визуализации результата разметки (активируется отдельным флагом при запуске)  

---

## **Model training**  
Для решения задачи использовался созданный датасет, а модели дообучались на основе `YOLOv10`.  

![Слайд 5](Слайд5.png)

### Обученные версии моделей:
- `Detectron2`  
- `YOLOv10nano`  
- `YOLOv10small`  
- `YOLOv10medium`  

Модель **YOLOv10medium**, обученная на 100 эпохах, была выбрана по итогам рассмотрения метрик и визуальной оценки.  

### График Precision & mAP50-95  

![Слайд 6](Слайд6.png)

---

## **Веб и контейнеризация**  
Для использования модели был создан Swagger с помощью `FastAPI`.  

- При загрузке изображения Swagger возвращает JSON с разметкой.  
- Создан Docker-образ для быстрого развёртывания проекта.  

![Слайд 8](Слайд8.png)

---

## **Что дальше?**
Пространство для улучшений:  
- Тестирование моделей с более серьёзными параметрами  
- Использование более мощных вычислительных ресурсов  
- Расширение генерации, включая многоколоночные абзацы  

---

## Итог  
По результатам работы было выполнено ТЗ, созданы утилиты для датасета и обучена модель с **precision=0.966**.

---

