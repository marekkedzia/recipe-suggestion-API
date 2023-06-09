from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors
import requests


def add_space(story):
    story.append(Spacer(1, 12))


def create_title(data, story, title_style):
    title = f"{data['title']}"
    title_style.textColor = colors.black
    title_style.backColor = colors.lightgrey
    title_style.borderRadius = 20
    title_style.borderWidth = 1
    title_style.borderColor = colors.black
    title_style.fontSize = 24
    title_style.fontName = 'Helvetica-Bold'
    title_style.leading = 30
    title_style.spaceBefore = 12

    add_space(story)
    story.append(Paragraph(title, title_style))


def create_ingredients(data, story, normal_style, doc):
    ingredients_data = []
    for ingredient in data['ingredients']:
        ingredients_data.append([Paragraph(
            f"{ingredient['measures']['amount']} {ingredient['measures']['unitLong']} {ingredient['nameClean']}",
            normal_style)])

    ingredients_table = Table(ingredients_data, colWidths=[doc.width])
    ingredients_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.gray),
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
    ]))
    ingredients_style = ParagraphStyle(name="Ingredients", fontSize=18, spaceAfter=12, alignment=TA_LEFT,
                                       fontWeight='bold')
    ingredients_paragraph = Paragraph("<strong>Ingredients:</strong>",
                                      ingredients_style)
    add_space(story)
    story.append(ingredients_paragraph)
    add_space(story)
    story.append(ingredients_table)


def create_image(data, story, doc):
    def is_ok(status_code):
        return status_code == 200

    def calculate_width(width):
        return width * 0.7

    def calculate_height(height):
        return height * 2 / 4 * 0.6

    image_url = data['image']
    response = requests.get(image_url)
    if is_ok(response.status_code):
        img = Image(BytesIO(response.content), width=calculate_width(doc.width), height=calculate_height(doc.height))
        add_space(story)
        add_space(story)
        story.append(img)
        add_space(story)


def create_summary(data, story, text_style):
    summary = f"{data['summary']}"
    text_style.spaceAfter = 18
    story.append(Paragraph(summary, text_style))
    add_space(story)


def create_instructions(data, story, normal_style):
    instructions = f"{data['instructions']}"
    instructions = instructions.replace("Directions:", "").strip()
    instructions_list = instructions.split('.')
    instructions_list = [step.strip() for step in instructions_list if step.strip() != '']
    instructions_list = [f"{i}. {step}" for i, step in enumerate(instructions_list, start=1)]
    instructions_text = '<br/>'.join(instructions_list)
    instructions_style = ParagraphStyle(name="Instructions", fontSize=18, spaceAfter=12, alignment=TA_LEFT,
                                        fontWeight='bold')
    instructions_paragraph = Paragraph("<strong>Instructions:</strong>",
                                       instructions_style)
    add_space(story)
    story.append(instructions_paragraph)
    add_space(story)
    story.append(Paragraph(instructions_text, normal_style))


def generate_pdf_file(recipe_dict):
    data = recipe_dict
    buffer = BytesIO()
    document = BaseDocTemplate(buffer, pagesize=letter)
    frame = Frame(document.leftMargin, document.bottomMargin, document.width, document.height, id='normal')
    document.addPageTemplates([PageTemplate(id='main', frames=frame)])
    document_content = []

    title_style = ParagraphStyle(name="Title", fontSize=18, alignment=TA_CENTER, spaceAfter=12, fontWeight='bold')
    normal_style = ParagraphStyle(name="Normal", fontSize=12, spaceAfter=12, alignment=TA_JUSTIFY)

    create_title(data, document_content, title_style)
    create_image(data, document_content, document)
    create_summary(data, document_content, normal_style)
    create_ingredients(data, document_content, normal_style, document)
    create_instructions(data, document_content, normal_style)

    document.build(document_content)
    buffer.seek(0)

    return buffer
