import csv
import json


def save_json(products, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump([p.to_dict() for p in products], file, ensure_ascii=False, indent=2)


def save_csv(products, path):
    rows = [p.to_dict() for p in products]
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)