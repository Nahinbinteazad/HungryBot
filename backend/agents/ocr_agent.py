from backend.tools.ocr_tool import extract_menu_text


def ocr_agent(image):

    text = extract_menu_text(image)

    return f"Detected Menu Items:\n{text}"