import os
import random
from datetime import datetime, timedelta, timezone
import psycopg2
from faker import Faker

SEED = 42
random.seed(SEED)
fake = Faker()
fake.seed_instance(SEED)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"), port=os.getenv("DB_PORT", 5432),
    dbname=os.getenv("DB_NAME", "warehouse"), user=os.getenv("DB_USER", "dw_user"),
    password=os.getenv("DB_PASSWORD", "dw_password"),
)
conn.autocommit = True
cur = conn.cursor()

cur.execute("""
CREATE SCHEMA IF NOT EXISTS raw;
CREATE TABLE IF NOT EXISTS raw.customers (
  customer_id integer PRIMARY KEY, first_name text, last_name text,
  email text, signup_date date, country text
);
CREATE TABLE IF NOT EXISTS raw.products (
  product_id integer PRIMARY KEY, product_name text, category text,
  price numeric(12,2), active boolean
);
CREATE TABLE IF NOT EXISTS raw.orders (
  order_id integer PRIMARY KEY, customer_id integer, order_date timestamptz,
  status text, shipping_country text
);
CREATE TABLE IF NOT EXISTS raw.order_items (
  order_item_id integer PRIMARY KEY, order_id integer, product_id integer,
  quantity integer, unit_price numeric(12,2)
);
CREATE TABLE IF NOT EXISTS raw.payments (
  payment_id integer PRIMARY KEY, order_id integer, payment_date timestamptz,
  amount numeric(12,2), payment_method text, status text
);
""")
cur.execute("TRUNCATE raw.order_items, raw.payments, raw.orders, raw.products, raw.customers CASCADE")

countries = ["United States", "Canada", "United Kingdom", "Germany", "Australia", "India"]
categories = ["Electronics", "Home", "Sports", "Books", "Beauty", "Apparel"]
methods = ["credit_card", "paypal", "bank_transfer", "gift_card"]
statuses = ["completed", "completed", "completed", "shipped", "cancelled"]

customers = []
for i in range(1, 501):
    first, last = fake.first_name(), fake.last_name()
    customers.append((i, first, last, f"{first}.{last}.{i}@example.com".lower(),
                      fake.date_between(start_date="-3y", end_date="-30d"), random.choice(countries)))
cur.executemany("INSERT INTO raw.customers VALUES (%s,%s,%s,%s,%s,%s)", customers)

products = []
for i in range(1, 81):
    category = random.choice(categories)
    products.append((i, f"{fake.word().title()} {category} {i}", category,
                     round(random.uniform(8, 500), 2), random.random() > 0.08))
cur.executemany("INSERT INTO raw.products VALUES (%s,%s,%s,%s,%s)", products)
price_by_product = {p[0]: p[3] for p in products}

orders, items, payments = [], [], []
base = datetime.now(timezone.utc) - timedelta(days=365)
item_id = payment_id = 1
for order_id in range(1, 4001):
    customer_id = random.randint(1, 500)
    order_dt = base + timedelta(days=random.randint(0, 364), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    status = random.choice(statuses)
    country = next(c[5] for c in customers if c[0] == customer_id)
    orders.append((order_id, customer_id, order_dt, status, country))
    total = 0
    for _ in range(random.randint(1, 5)):
        product_id = random.randint(1, 80)
        qty = random.randint(1, 4)
        unit_price = price_by_product[product_id]
        total += qty * unit_price
        items.append((item_id, order_id, product_id, qty, unit_price))
        item_id += 1
    if status != "cancelled":
        payments.append((payment_id, order_id, order_dt + timedelta(minutes=random.randint(1, 120)), round(total, 2), random.choice(methods), "paid"))
        payment_id += 1

cur.executemany("INSERT INTO raw.orders VALUES (%s,%s,%s,%s,%s)", orders)
cur.executemany("INSERT INTO raw.order_items VALUES (%s,%s,%s,%s,%s)", items)
cur.executemany("INSERT INTO raw.payments VALUES (%s,%s,%s,%s,%s,%s)", payments)
print(f"Loaded {len(customers)} customers, {len(products)} products, {len(orders)} orders, {len(items)} line items, {len(payments)} payments")
cur.close(); conn.close()
