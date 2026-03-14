import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.append(str(root))

from backend.tools.ocr_tool import build_clip_cache

count = build_clip_cache()
print(f"CLIP cache built for {count} labels.")