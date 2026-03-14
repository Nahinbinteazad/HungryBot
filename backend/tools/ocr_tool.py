import os
import pickle
import pytesseract
from pathlib import Path
from PIL import Image

CLIP_CACHE_PATH = Path('data/clip_food_embeddings.pkl')
_clip_model = None
_clip_processor = None
_clip_labels = None
_clip_text_embeddings = None


def extract_menu_text(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    return text


def _get_clip_model():
    global _clip_model, _clip_processor
    if _clip_model is not None and _clip_processor is not None:
        return _clip_model, _clip_processor

    try:
        from transformers import CLIPModel, CLIPProcessor
        _clip_model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
        _clip_processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
        return _clip_model, _clip_processor
    except Exception as e:
        raise RuntimeError('CLIP model unavailable: ' + str(e))


def _build_clip_text_embeddings(candidate_labels):
    model, processor = _get_clip_model()
    import torch

    batch_text = processor(text=candidate_labels, images=None, return_tensors='pt', padding=True)
    with torch.no_grad():
        text_features = model.get_text_features(**batch_text)
    text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)

    CLIP_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CLIP_CACHE_PATH, 'wb') as f:
        pickle.dump({'labels': candidate_labels, 'embeddings': text_features}, f)

    return text_features


def _load_clip_text_embeddings(candidate_labels):
    global _clip_labels, _clip_text_embeddings

    if _clip_labels == candidate_labels and _clip_text_embeddings is not None:
        return _clip_text_embeddings

    if CLIP_CACHE_PATH.exists():
        try:
            with open(CLIP_CACHE_PATH, 'rb') as f:
                data = pickle.load(f)
            if data.get('labels') == candidate_labels:
                _clip_labels = candidate_labels
                _clip_text_embeddings = data.get('embeddings')
                return _clip_text_embeddings
        except Exception:
            pass

    _clip_text_embeddings = _build_clip_text_embeddings(candidate_labels)
    _clip_labels = candidate_labels
    return _clip_text_embeddings


def classify_food_image(image, candidate_labels=None, max_results=5):
    """Classify food image.

    Priorities:
    1) CLIP image matching against precomputed candidate text embeddings.
    2) OpenAI Vision (if key + package available).
    3) OCR text matching fallback.
    """
    # CLIP semantic match
    if candidate_labels:
        try:
            model, processor = _get_clip_model()
            import torch

            text_embeddings = _load_clip_text_embeddings(candidate_labels)

            img = Image.open(image).convert('RGB')
            image_input = processor(images=img, return_tensors='pt')
            with torch.no_grad():
                image_embeddings = model.get_image_features(**image_input)
            image_embeddings = image_embeddings / image_embeddings.norm(p=2, dim=-1, keepdim=True)

            scores = (image_embeddings @ text_embeddings.T).squeeze(0)
            topk = torch.topk(scores, min(max_results, len(candidate_labels)))
            result = []
            for idx, score in zip(topk.indices.tolist(), topk.values.tolist()):
                result.append(f"{candidate_labels[idx]} ({score:.3f})")
            return result
        except Exception:
            pass

    # OpenAI Vision classification
    try:
        import openai
    except ImportError:
        openai = None

    if openai and os.getenv('OPENAI_API_KEY'):
        try:
            with open(image, 'rb') as f:
                result = openai.Image.create(
                    file=f,
                    model='gpt-image-1',
                    prompt='Identify the food in this image and return the top 5 likely Bangladeshi dishes.'
                )
            text_result = result.get('data', [{}])[0].get('b64_json', '')
            return [text_result] if text_result else []
        except Exception:
            pass

    # Fallback: OCR text matching
    text = extract_menu_text(image).lower()
    if not candidate_labels:
        return []

    matches = []
    for food in candidate_labels:
        if food.lower() in text:
            matches.append(food)
            if len(matches) >= max_results:
                break
    return matches


def build_clip_cache(candidate_labels=None):
    """Build and cache CLIP text embeddings for candidate labels."""
    if candidate_labels is None:
        from backend.database.vector_store import get_food_list
        candidate_labels = get_food_list()

    _load_clip_text_embeddings(candidate_labels)
    return len(candidate_labels)