
from db import Database
from scrapers import BooksScraper, DealsScraper

db = Database()


def update():
    products = []
    for scraper in [BooksScraper(pages=5), DealsScraper(limit=20)]:
        products.extend(scraper.fetch())

    print(
        f"Оновлено товарів: {db.update_from(products)}. "
        f"У базі всього: {db.count()}"
    )


def search():
    word = input("Слово для пошуку: ")

    for product_id, title, price, currency in db.find(word):
        print(f"  #{product_id} {title[:50]:50} {currency}{price}")


def top_deals():
    for product_id, title, price, old_price, discount, currency in db.top_discounts(5):
        print(
            f"  #{product_id} {title[:34]:34} "
            f"-{int(discount)}%  {currency}{price} "
            f"(було {currency}{old_price})"
        )


def stats():
    for name, currency, items, avg_price, cheapest, priciest in db.stats_by_source():
        print(
            f"  {name}: {items} шт., середня {currency}{avg_price}, "
            f"від {currency}{cheapest} до {currency}{priciest}"
        )


def history():
    product_id = int(input("Номер товару (#): "))

    for checked_at, price in db.price_history(product_id):
        print(f"  {checked_at}  {price}")

    drop = db.price_drop(product_id)

    print(
        "  Ціна впала!" if drop
        else "  Падіння ціни не зафіксовано.",
        drop or ""
    )




def rating_stats():
    print("\nКількість книжок за рейтингом:")

    results = db.count_by_rating()

    if not results:
        print("Даних про рейтинги поки немає.")
    else:
        for rating, total in results:
            print(f"  Рейтинг {rating}: {total} книжок")


def priciest_products():
    n = int(input("Скільки товарів показати? "))

    if n <= 0:
        print("Введи число більше нуля.")
        return

    results = db.priciest(n)

    print(f"\nТоп-{n} найдорожчих товарів:")

    if not results:
        print("Товарів поки немає.")
    else:
        for title, price, currency in results:
            print(f"  {title}: {price} {currency}")


def discount_stats():
    total = db.count_games_discounted_50()

    print(
        f"\nКількість товарів зі знижкою від 50%: {total}"
    )




MENU = {
    "1": ("Оновити дані", update),
    "2": ("Пошук за словом", search),
    "3": ("Топ-5 знижок", top_deals),
    "4": ("Статистика по джерелах", stats),
    "5": ("Історія цін товару", history),
    "6": ("Кількість книжок за рейтингом", rating_stats),
    "7": ("Найдорожчі товари", priciest_products),
    "8": ("Товари зі знижкою від 50%", discount_stats),
}




try:
    while True:
        print("\n=== DEAL RADAR ===")

        for key, (label, _) in MENU.items():
            print(f"{key}. {label}")

        print("0. Вихід")

        choice = input("Обери пункт: ")

        if choice == "0":
            break

        if choice in MENU:
            MENU[choice][1]()
        else:
            print("Такого пункту немає.")

finally:
    db.close()

print("До зустрічі!")
