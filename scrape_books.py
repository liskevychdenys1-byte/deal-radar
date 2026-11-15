
import sqlite3
import requests
import time
import re
from bs4 import BeautifulSoup

DB_NAME = "deals.db"

RATINGS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price REAL,
    source TEXT,
    rating INTEGER,
    old_price REAL,
    currency TEXT,
    category TEXT,
    availability TEXT
)
""")


cursor.execute("DELETE FROM products")


for page in range(1, 51):

    url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    print(f"Завантаження сторінки {page}...")

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
    except requests.RequestException as error:
        print("Помилка завантаження:", error)
        break

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    if not books:
        break

    for book in books:


        title = book.find("h3").find("a")["title"]


        price_text = book.find("p", class_="price_color").text
        price = float(re.sub(r"[^\d.]", "", price_text))


        rating_element = book.find("p", class_="star-rating")
        rating_word = rating_element["class"][1]
        rating = RATINGS[rating_word]


        availability = book.find(
            "p", class_="instock availability"
        ).text.strip()

        # Запис у базу даних
        cursor.execute("""
            INSERT INTO products
            (title, price, source, rating, old_price,
             currency, category, availability)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title,
            price,
            "Books to Scrape",
            rating,
            None,
            "£",
            "Books",
            availability
        ))

    conn.commit()
    time.sleep(0.5)


cursor.execute("SELECT COUNT(*) FROM products")
total = cursor.fetchone()[0]

print("\nЗавантаження завершено!")
print("Усього книжок у базі:", total)

conn.close()
