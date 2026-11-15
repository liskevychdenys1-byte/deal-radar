
import sqlite3
import os


db_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "deals.db"
)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()



def show(title, cursor):
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)

    columns = [description[0] for description in cursor.description]
    print(" | ".join(columns))
    print("-" * 65)

    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(" | ".join(str(value) for value in row))
    else:
        print("Результатів не знайдено.")

    print("Кількість результатів:", len(rows))



cursor.execute("""
    SELECT *
    FROM products
    WHERE category = 'Books'
      AND currency = '£'
      AND rating IN (4, 5)
      AND price < 20
    ORDER BY price ASC
""")
show("ЗАПИТ 1. Книжки з рейтингом 4 або 5 дешевші за £20", cursor)



cursor.execute("""
    SELECT *
    FROM products
    WHERE category = 'Games'
      AND currency = '$'
      AND price < 5
""")
show("ЗАПИТ 2. Ігри дешевші за $5", cursor)



cursor.execute("""
    SELECT *
    FROM products
    WHERE category = 'Books'
      AND title LIKE '%Love%'
""")
show("ЗАПИТ 3. Книжки зі словом Love у назві", cursor)



cursor.execute("""
    SELECT *
    FROM products
    ORDER BY price DESC
    LIMIT 5
""")
show("ЗАПИТ 4. П'ять найдорожчих товарів", cursor)



cursor.execute("""
    SELECT *,
           ROUND((1.0 - price / old_price) * 100, 2) AS discount
    FROM products
    WHERE category = 'Games'
      AND old_price > 0
      AND (1.0 - price / old_price) * 100 >= 70
""")
show("ЗАПИТ 5. Ігри зі знижкою від 70%", cursor)


conn.close()
print("\nРоботу програми завершено!")
