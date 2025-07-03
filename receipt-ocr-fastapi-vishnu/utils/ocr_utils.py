import pytesseract
from pdf2image import convert_from_path
import tempfile

def extract_text(pdf_path):
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(pdf_path, output_folder=path)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)
    return text
