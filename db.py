
import sqlite3
from datetime import datetime

DB_PATH = "radar.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT UNIQUE NOT NULL,
    currency TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT NOT NULL,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    price     REAL NOT NULL,
    old_price REAL,
    rating    REAL,
    UNIQUE (title, source_id)
);

CREATE TABLE IF NOT EXISTS price_history (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id),
    price      REAL NOT NULL,
    checked_at TEXT NOT NULL
);
"""


class Database:

    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path)
        self.conn.executescript(SCHEMA)

    def close(self):
        self.conn.close()

    def _source_id(self, name, currency):
        self.conn.execute(
            "INSERT OR IGNORE INTO sources (name, currency) VALUES (?, ?)",
            (name, currency)
        )
        return self.conn.execute(
            "SELECT id FROM sources WHERE name = ?", (name,)
        ).fetchone()[0]

    def add_product(self, product):


        source_id = self._source_id(product.source, product.currency)

        self.conn.execute(
            "INSERT INTO products "
            "(title, source_id, price, old_price, rating) "
            "VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(title, source_id) DO UPDATE SET "
            "price = excluded.price, "
            "old_price = excluded.old_price, "
            "rating = excluded.rating",
            (
                product.title,
                source_id,
                product.price,
                product.old_price,
                product.rating
            ),
        )

        product_id = self.conn.execute(
            "SELECT id FROM products WHERE title = ? AND source_id = ?",
            (product.title, source_id)
        ).fetchone()[0]

        self.conn.execute(
            "INSERT INTO price_history "
            "(product_id, price, checked_at) VALUES (?, ?, ?)",
            (
                product_id,
                product.price,
                datetime.now().isoformat(timespec="seconds")
            ),
        )

        return product_id



    def count_by_rating(self):


        cur = self.conn.cursor()

        cur.execute("""
            SELECT rating, COUNT(*)
            FROM products
            WHERE rating IS NOT NULL
            GROUP BY rating
            ORDER BY rating DESC
        """)

        return cur.fetchall()



    def priciest(self, n):


        cur = self.conn.cursor()

        cur.execute("""
            SELECT p.title, p.price, s.currency
            FROM products p
            JOIN sources s ON p.source_id = s.id
            ORDER BY p.price DESC
            LIMIT ?
        """, (n,))

        return cur.fetchall()



    def count_games_discounted_50(self):

        cur = self.conn.cursor()

        cur.execute("""
            SELECT COUNT(*)
            FROM products
            WHERE old_price > 0
              AND price <= old_price * 0.5
        """)

        return cur.fetchone()[0]

    def update_from(self, products):
        for product in products:
            self.add_product(product)

        self.conn.commit()

        return len(products)

    def count(self):
        return self.conn.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

    def find(self, word):
        sql = (
            "SELECT p.id, p.title, p.price, s.currency "
            "FROM products p "
            "JOIN sources s ON p.source_id = s.id "
            "WHERE p.title LIKE ? "
            "ORDER BY p.price LIMIT 10"
        )

        return self.conn.execute(
            sql, (f"%{word}%",)
        ).fetchall()

    def cheaper_than(self, limit, source):
        sql = (
            "SELECT p.id, p.title, p.price, s.currency "
            "FROM products p "
            "JOIN sources s ON p.source_id = s.id "
            "WHERE s.name = ? AND p.price < ? "
            "ORDER BY p.price"
        )

        return self.conn.execute(
            sql, (source, limit)
        ).fetchall()

    def top_discounts(self, n=5):
        sql = (
            "SELECT p.id, p.title, p.price, p.old_price, "
            "ROUND((1 - p.price / p.old_price) * 100) AS discount, "
            "s.currency "
            "FROM products p "
            "JOIN sources s ON p.source_id = s.id "
            "WHERE p.old_price IS NOT NULL AND p.old_price > 0 "
            "ORDER BY discount DESC LIMIT ?"
        )

        return self.conn.execute(sql, (n,)).fetchall()

    def stats_by_source(self):
        sql = (
            "SELECT s.name, s.currency, COUNT(*), "
            "ROUND(AVG(p.price), 2), MIN(p.price), MAX(p.price) "
            "FROM products p "
            "JOIN sources s ON p.source_id = s.id "
            "GROUP BY s.id"
        )

        return self.conn.execute(sql).fetchall()

    def price_history(self, product_id):
        sql = (
            "SELECT checked_at, price "
            "FROM price_history "
            "WHERE product_id = ? "
            "ORDER BY checked_at"
        )

        return self.conn.execute(
            sql, (product_id,)
        ).fetchall()

    def price_drop(self, product_id):


        sql = """
            SELECT price
            FROM price_history
            WHERE product_id = ?
            ORDER BY checked_at DESC
            LIMIT 2
        """

        rows = self.conn.execute(
            sql, (product_id,)
        ).fetchall()

        if len(rows) == 2 and rows[0][0] < rows[1][0]:
            return rows[1][0], rows[0][0]

        return None
