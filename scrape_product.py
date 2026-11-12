class Product:
    def __init__(self, title, price, source, rating=None, old_price=None, currency="$"):
        self.title = title
        self.price = price
        self.source = source
        self.rating = rating
        self.old_price = old_price
        self.currency = currency

    def discount(self):
        """Знижка у відсотках (0, якщо старої ціни немає)."""
        if not self.old_price:
            return 0
        return round((1 - self.price / self.old_price) * 100)

    def to_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "currency": self.currency,
            "old_price": self.old_price,
            "discount": self.discount(),
            "rating": self.rating,
            "source": self.source,
        }

    def __str__(self):
        text = f"{self.title[:34]:34} {self.currency}{self.price:>6.2f}"
        if self.discount():
            text += f"  -{self.discount()}%"
        return text

