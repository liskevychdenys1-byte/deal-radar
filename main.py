
from scrape_product import Product

products = [
    Product("Python for Beginners", 12, "Amazon", old_price=30),
    Product("Learning Python", 18, "Amazon", old_price=25),
    Product("Clean Code", 14, "Bookshop", old_price=28),
    Product("Laptop", 500, "Store", old_price=900),
    Product("Python Cookbook", 20, "Amazon", old_price=35),
]

# Дешеві книжки до £15
cheap_books = [
    product for product in products
    if product.is_cheap(15)
    and product.currency == "£"
]

# Товари зі знижкою від 50%
deals = [
    product for product in products
    if product.is_deal()
]

print("=== CHEAP BOOKS ===")

for product in cheap_books:
    print(product)

print("Кількість дешевих книжок:", len(cheap_books))

print("\n=== DEALS ===")

for product in deals:
    print(product)

print("Кількість товарів зі знижкою:", len(deals))

print("\nЗагальна кількість знайдених:", len(cheap_books) + len(deals))
