class Product:
    def __init__(self, title, price, source, rating=None, old_price=None, currency="£"):
        self.title = title
        self.price = price
        self.source = source
        self.rating = rating
        self.old_price = old_price
        self.currency = currency

    def discount(self):
        if not self.old_price:
            return 0
        return round((1 - self.price / self.old_price) * 100)

    def is_cheap(self, limit):
        return self.price < limit

    def is_deal(self):
        return self.discount() >= 50

    def __str__(self):
        text = f"{self.title:34} {self.currency}{self.price:.2f}"
        if self.discount():
            text += f" -{self.discount()}%"
        return text