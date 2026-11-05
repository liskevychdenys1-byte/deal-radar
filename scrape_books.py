
import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

response = requests.get(URL, timeout=20)
response.raise_for_status()
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")

cards = soup.select("article.product_pod")
books = []

print(f"Знайдено книжок: {len(cards)}")

for number, card in enumerate(cards, 1):
    # Назва
    title = card.h3.a["title"].strip()

    # Ціна: перетворюємо на число
    price_text = card.select_one("p.price_color").get_text()
    price = float(price_text.replace("£", "").replace("Â", "").strip())

    # Рейтинг
    rating_word = card.select_one("p.star-rating")["class"][1]
    rating = RATINGS[rating_word]

    # Наявність
    availability = card.select_one("p.instock").get_text(strip=True)

    # Зберігаємо дані книжки
    books.append({
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability
    })

    print(
        f"{number:2}. {title[:38]:38} "
        f"£{price:6.2f}  "
        f"{'*' * rating}  "
        f"{availability}"
    )

# Сортування за ціною
cheapest_books = sorted(books, key=lambda book: book["price"])

print("\n===== 5 НАЙДЕШЕВШИХ КНИЖОК =====")

for book in cheapest_books[:5]:
    print(
        f"{book['title']} | "
        f"£{book['price']:.2f} | "
        f"Рейтинг: {book['rating']} | "
        f"{book['availability']}"
    )

# Кількість книжок із рейтингом 5
five_star_count = sum(1 for book in books if book["rating"] == 5)

print(f"\nКількість книжок із рейтингом 5: {five_star_count}")
