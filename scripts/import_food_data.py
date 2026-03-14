import argparse
import csv
import json
from pathlib import Path

DATA_PATH = Path('data/food_dataset.txt')

DEFAULT_FIELDS = ['Food', 'City', 'Place', 'Type', 'Description', 'Rating', 'Tags', 'Cuisine', 'Vendor', 'Budget', 'Subdistrict']


def format_block(record):
    lines = []
    for field in DEFAULT_FIELDS:
        value = record.get(field) or record.get(field.lower())
        if value:
            lines.append(f"{field}: {value}")
    return "\n".join(lines)


def import_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]

    return data


def import_csv(file_path):
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)


def append_blocks(records):
    existing = DATA_PATH.read_text(encoding='utf-8') if DATA_PATH.exists() else ''
    blocks = [b.strip() for b in existing.split('\n\n') if b.strip()]

    for rec in records:
        blocks.append(format_block(rec))

    DATA_PATH.write_text('\n\n'.join(blocks).strip() + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Import food entries into data/food_dataset.txt')
    parser.add_argument('file', help='Input JSON or CSV file containing food records')
    args = parser.parse_args()

    path = Path(args.file)
    ext = path.suffix.lower()

    if ext in ['.json']:
        records = import_json(path)
    elif ext in ['.csv']:
        records = import_csv(path)
    else:
        raise ValueError('Unsupported input format: use .json or .csv')

    if not records:
        print('No records found to import.')
        return

    append_blocks(records)
    print(f'Imported {len(records)} records to {DATA_PATH}.')


if __name__ == '__main__':
    main()