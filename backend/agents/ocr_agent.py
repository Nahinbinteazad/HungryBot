from backend.tools.ocr_tool import extract_menu_text, classify_food_image
from backend.database.vector_store import get_food_list


def ocr_agent(image):
    text = extract_menu_text(image)
    known_foods = get_food_list()
    detected_foods = classify_food_image(image, candidate_labels=known_foods, max_results=6)

    response = ["Detected Menu Items:", text.strip() if text.strip() else "(No text detected)"]

    if detected_foods:
        response.append("\nPossible foods detected in image:")
        for f in detected_foods:
            response.append(f"- {f}")
    else:
        response.append("\nCould not identify specific foods from the image. Try a clearer photo or use a menu image.")

    return "\n".join(response)