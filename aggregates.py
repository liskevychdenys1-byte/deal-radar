import sqlite3

conn = sqlite3.connect("deals.db")
cur = conn.cursor()

print("Усього товарів:", cur.execute("SELECT COUNT(*) FROM products").fetchone()[0])
print("Середня ціна всіх товарів:", cur.execute("SELECT ROUND(AVG(price), 2) FROM products").fetchone()[0])

print("\nСтатистика по джерелах:")
sql = """
SELECT source, currency, COUNT(*) AS items, ROUND(AVG(price), 2) AS avg_price,
       MIN(price) AS cheapest, MAX(price) AS priciest
FROM products
GROUP BY source, currency
"""
for row in cur.execute(sql):
    print("  ", row)

print("\nСкільки книжок кожного рейтингу:")
for row in cur.execute("SELECT rating, COUNT(*) FROM products WHERE source = 'books' GROUP BY rating ORDER BY rating"):
    print("  ", row)

conn.close()