class Product:
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


        if self.discount():
            text += f" -{self.discount()}%"
        return text