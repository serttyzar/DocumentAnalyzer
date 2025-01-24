import random
from faker import Faker
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from generators.generator import ContentGenerator
from localization.locale_strategy import LocaleStrategy


class FormulaGenerator(ContentGenerator):
    def __init__(self, font_size, locale_strategy: LocaleStrategy):
        self.font_size = font_size
        self.locale_strategy = locale_strategy
        
    def generate(self, document):
        formula_paragraph = document.add_paragraph()
        formula = random.choice([
            "E = mc²", "a² + b² = c²", "∫f(x) dx = F(x) + C", "F = G(m₁m₂)/r²",
            "sin²θ + cos²θ = 1", "x = (-b ± √(b²-4ac)) / 2a"
        ])
        formula_run = formula_paragraph.add_run(formula)
        formula_run.font.size = Pt(12)
        formula_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER