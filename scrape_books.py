import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

response = requests.get(URL)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

cards = soup.select("article.product_pod")
print(f"Знайдено книжок: {len(cards)}")

for number, card in enumerate(cards, 1):
    title = card.h3.a["title"]
    price = card.select_one("p.price_color").get_text()
    rating_word = card.select_one("p.star-rating")["class"][1]
    print(f"{number:2}. {title[:38]:38} {price:>7}  {'*' * RATINGS[rating_word]}")