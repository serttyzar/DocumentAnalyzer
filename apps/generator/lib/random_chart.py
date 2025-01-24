import random
import matplotlib.pyplot as plt
from io import BytesIO

class ChartGenerator:
    """Генератор случайных графиков"""
    @staticmethod
    def generate_random_chart():
        """Генерирует и возвращает случайный график"""

        def generate_random_color():
            """Генерирует случайный цвет в формате RGB"""
            return (random.random(), random.random(), random.random())
    
        chart_type = random.choice(['line', 'bar', 'pie', 'scatter'])
        fig, ax = plt.subplots(figsize=(40, 24))

        if chart_type == 'line':
            x = range(10)
            y = [random.randint(1, 10) for _ in x]
            ax.plot(x, y, marker='o', color=generate_random_color(), linestyle='-', linewidth=3)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")

        elif chart_type == 'bar':
            x = range(5)
            y = [random.randint(1, 10   ) for _ in x]
            ax.bar(x, y, color=generate_random_color())
            ax.set_xlabel("Категории")
            ax.set_ylabel("Значения")

        elif chart_type == 'pie':
            sizes = [random.randint(10, 30) for _ in range(5)]
            labels = [f'Категория {i+1}' for i in range(5)]
            ax.pie(sizes, labels=labels, autopct='%1.1f%%')

        elif chart_type == 'scatter':
            x = [random.randint(1, 10) for _ in range(10)]
            y = [random.randint(1, 10) for _ in range(10)]
            ax.scatter(x, y, color=generate_random_color(), s=800)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")

        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close(fig)
        image_stream.seek(0)
        
        return image_stream
