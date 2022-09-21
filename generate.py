from io import BytesIO
from docxtpl import DocxTemplate



def from_template(template, context):
    target_file = BytesIO()

    template = DocxTemplate(template)

    target_file = BytesIO()
    template.render(context)
    template.save(target_file)

    return target_file