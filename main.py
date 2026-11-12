from scrapers import BooksScraper,  DealsScraper
from storage import save_json, save_csv

scrapers = [BooksScraper(pages=5), DealsScraper(limit=20)]

products = []
for scraper in scrapers:
    found = scraper.fetch()
    print(f"[{scraper.name}] зібрано: {len(found)}")
    products.extend(found)

print(f"\nУсього товарів: {len(products)}")

# ціни в різних валютах не порівнюємо: шукаємо найдешевше в кожному джерелі
for scraper in scrapers:
    group = [p for p in products if p.source == scraper.name]
    print(f"Найдешевше ({scraper.name}):", min(group, key=lambda p: p.price))

best_deal = max(products, key=lambda p: p.discount())
print("Найбільша знижка:", best_deal)

save_json(products, "products.json")
save_csv(products, "products.csv")
print("Збережено: products.json, products.csv")