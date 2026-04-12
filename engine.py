import pytesseract
from pytesseract import Output
from score import score_text

def run_tesseract_with_data (img, config):
    data = pytesseract.image_to_data(img, config=config, output_type= Output.DICT)
    return score_text(data)