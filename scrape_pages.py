import  time

import requests
from bs4 import BeautifulSoup

PAGE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def clean_price(text):
   return float(text.strip().replace("£", ""))


books = []
for page in range(1, 4):
   response = requests.get(PAGE_URL.format(page))
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")
for card in soup.select("article.product_pod"):
    books.append({
"title": card.h3.a["title"],
"price": clean_price(card.select_one("p.price_color").get_text()),
"rating": RATINGS[card.select_one("p.star-rating")["class"][1]],
})
print(f"Сторінка {page}: усього книжок {len(books)}")
time.sleep(0.5) # не навантажуємо сайт

cheapest = min(books, key=lambda b: b["price"])
print("Найдешевша:", cheapest["title"], cheapest["price"])
 