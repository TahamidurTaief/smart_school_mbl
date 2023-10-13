from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf.pisa import pisa


def save_pdf(params:dict):
    template = get_template("hod/view_routine.html")