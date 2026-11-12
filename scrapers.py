import time

import requests
from bs4 import BeautifulSoup

from scrape_product import Product

# Деякі API вимагають, щоб клієнт «представився» (замініть nick на свій нік GitHub)
HEADERS = {"User-Agent": "DealRadar/1.0 (https://github.com/hmmmarta)"}
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class BaseScraper:
    name = "base"

    def __init__(self, delay=0.5):
        self.delay = delay

    def get(self, url, **params):
        """Безпечний запит: повертає відповідь або None, якщо щось пішло не так."""
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()
        except requests.RequestException as error:
            print(f"[{self.name}] помилка запиту: {error}")
            return None
        response.encoding = "utf-8"
        time.sleep(self.delay)  # ввічлива пауза
        return response

    def fetch(self):
        raise NotImplementedError("Кожен збирач має свій метод fetch()")

class BooksScraper(BaseScraper):
    name = "books"
    PAGE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

    def __init__(self, pages=5, delay=0.5):
        super().__init__(delay)
        self.pages = pages

    def fetch(self):
        products = []
        for page in range(1, self.pages + 1):
            response = self.get(self.PAGE_URL.format(page))
            if response is None:
                break
            soup = BeautifulSoup(response.text, "html.parser")
            for card in soup.select("article.product_pod"):
                price = float(card.select_one("p.price_color").get_text().strip().replace("£", ""))
                rating = RATINGS[card.select_one("p.star-rating")["class"][1]]
                products.append(Product(card.h3.a["title"], price, self.name, rating=rating, currency="£"))
        return products


class DealsScraper(BaseScraper):
    name = "deals"
    API_URL = "https://www.cheapshark.com/api/1.0/deals"

    def __init__(self, limit=20, delay=0.5):
        super().__init__(delay)
        self.limit = limit

    def fetch(self):
        response = self.get(self.API_URL, storeID=1, pageSize=self.limit)
        if response is None:
            return []
        products = []
        for deal in response.json():
            percent = float(deal.get("steamRatingPercent") or 0)
            products.append(Product(
                deal["title"],
                float(deal["salePrice"]),
                self.name,
                rating=round(percent / 20, 1),
                old_price=float(deal["normalPrice"]),
            ))
        return products