import pytesseract
from PIL import Image


def extract_menu_text(image):

    img = Image.open(image)

    text = pytesseract.image_to_string(img)

    return text