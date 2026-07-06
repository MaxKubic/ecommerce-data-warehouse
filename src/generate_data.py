import random
from pathlib import Path

import pandas as pd
from faker import Faker


fake = Faker("cs_CZ")
random.seed(42)
Faker.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_customers(number_of_customers: int = 500) -> pd.DataFrame:
    customers = []

    for customer_id in range(1, number_of_customers + 1):
        customers.append({
            "customer_id": customer_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "city": fake.city(),
            "country": "Czech Republic",
            "created_at": fake.date_between(start_date="-3y", end_date="today")
        })

    return pd.DataFrame(customers)


def generate_products(number_of_products: int = 100) -> pd.DataFrame:
    categories = ["Electronics", "Fashion", "Home", "Sport", "Beauty", "Books"]
    brands = ["NovaTech", "UrbanWear", "HomePro", "FitLine", "BeautyLab", "BookHouse"]

    products = []

    for product_id in range(1, number_of_products + 1):
        price = round(random.uniform(100, 5000), 2)
        cost = round(price * random.uniform(0.4, 0.8), 2)

        products.append({
            "product_id": product_id,
            "product_name": f"Product {product_id}",
            "category": random.choice(categories),
            "brand": random.choice(brands),
            "price": price,
            "cost": cost
        })

    return pd.DataFrame(products)


def main() -> None:
    customers_df = generate_customers()
    products_df = generate_products()

    customers_df.to_csv(RAW_DATA_DIR / "customers.csv", index=False)
    products_df.to_csv(RAW_DATA_DIR / "products.csv", index=False)

    print("Generated customers.csv")
    print("Generated products.csv")


if __name__ == "__main__":
    main()