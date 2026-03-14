from pathlib import Path

path = Path('d:/HungryBot/data/food_dataset.txt')
text = path.read_text(encoding='utf-8')
blocks = [b.strip() for b in text.split('\n\n') if b.strip()]

rating_by_type = {
    'restaurant': '4.5',
    'street food': '4.4',
    'specialty': '4.6',
    'dessert': '4.3',
    'beverage': '4.2',
    'seafood': '4.5',
    'grocery': '4.0',
    'snack': '4.1'
}

def infer_tags(food, typ, city):
    tags = set()
    typ_lower = typ.strip().lower()
    city_lower = city.strip().lower()
    if typ_lower:
        tags.add(typ_lower)
    if city_lower:
        tags.add(city_lower)

    for kw in ['biryani', 'fish', 'seafood', 'sweet', 'meat', 'vegetarian', 'street', 'tea', 'pitha', 'spice', 'dessert', 'beverage']:
        if kw in food.lower():
            tags.add(kw)

    return ', '.join(sorted(tags))

new_blocks = []
for block in blocks:
    lines = [l for l in block.splitlines() if l.strip()]
    kv = {l.split(':', 1)[0].strip().lower(): l.split(':', 1)[1].strip() for l in lines if ':' in l}
    typ = kv.get('type', '')
    food = kv.get('food', '')
    city = kv.get('city', '')

    if 'rating' not in kv:
        default_rating = rating_by_type.get(typ.strip().lower(), '4.2')
        lines.append(f'Rating: {default_rating}')

    if 'tags' not in kv:
        tags = infer_tags(food, typ, city)
        if tags:
            lines.append(f'Tags: {tags}')

    new_blocks.append('\n'.join(lines))

path.write_text('\n\n'.join(new_blocks) + '\n', encoding='utf-8')
print('updated')