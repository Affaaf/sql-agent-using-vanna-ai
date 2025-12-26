import random
import os

import mysql.connector
from faker import Faker
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB")
}


fake = Faker()

PRODUCT_CATEGORIES = ["Electronics", "Clothing", "Home", "Books", "Sports"]

def insert_data(users_count=10, products_count=10, orders_count=20):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Insert users
    for _ in range(users_count):
        cursor.execute("""
            INSERT INTO users (email, first_name, last_name)
            VALUES (%s, %s, %s)
        """, (
            fake.unique.email(),
            fake.first_name(),
            fake.last_name()
        ))

    # Insert products
    for _ in range(products_count):
        cursor.execute("""
            INSERT INTO products (name, category, price, stock_quantity)
            VALUES (%s, %s, %s, %s)
        """, (
            fake.word().capitalize(),
            random.choice(PRODUCT_CATEGORIES),
            round(random.uniform(10, 500), 2),
            random.randint(1, 100)
        ))

    # Fetch user and product IDs
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id, price FROM products")
    products = cursor.fetchall()

    # Insert orders
    for _ in range(orders_count):
        product_id, price = random.choice(products)
        quantity = random.randint(1, 5)

        cursor.execute("""
            INSERT INTO orders (user_id, product_id, quantity, total_price)
            VALUES (%s, %s, %s, %s)
        """, (
            random.choice(user_ids),
            product_id,
            quantity,
            price * quantity
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(" Sample e-commerce data inserted successfully.")


if __name__ == "__main__":
    insert_data()