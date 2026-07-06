import random
from pathlib import Path
from datetime import timedelta

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


def generate_orders(customers_df: pd.DataFrame, number_of_orders: int = 3000) -> pd.DataFrame:
    statuses = ["created", "paid", "shipped", "cancelled", "returned"]
    status_weights = [0.05, 0.25, 0.55, 0.10, 0.05]

    customer_ids = customers_df["customer_id"].tolist()
    orders = []

    for order_id in range(1, number_of_orders + 1):
        orders.append({
            "order_id": order_id,
            "customer_id": random.choice(customer_ids),
            "order_date": fake.date_time_between(start_date="-2y", end_date="now"),
            "status": random.choices(statuses, weights=status_weights, k=1)[0]
        })

    return pd.DataFrame(orders)


def generate_order_items(
    orders_df: pd.DataFrame,
    products_df: pd.DataFrame
) -> pd.DataFrame:
    order_items = []
    order_item_id = 1

    product_ids = products_df["product_id"].tolist()
    product_prices = dict(zip(products_df["product_id"], products_df["price"]))

    for order_id in orders_df["order_id"]:
        number_of_items = random.randint(1, 5)

        selected_products = random.sample(product_ids, number_of_items)

        for product_id in selected_products:
            quantity = random.randint(1, 4)
            unit_price = product_prices[product_id]

            order_items.append({
                "order_item_id": order_item_id,
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price
            })

            order_item_id += 1

    return pd.DataFrame(order_items)


def generate_payments(
    orders_df: pd.DataFrame,
    order_items_df: pd.DataFrame
) -> pd.DataFrame:
    payment_methods = ["card", "bank_transfer", "cash_on_delivery", "paypal"]
    payments = []

    order_totals = (
        order_items_df
        .assign(item_total=order_items_df["quantity"] * order_items_df["unit_price"])
        .groupby("order_id", as_index=False)["item_total"]
        .sum()
    )

    order_totals_map = dict(zip(order_totals["order_id"], order_totals["item_total"]))

    for payment_id, (_, row) in enumerate(orders_df.iterrows(), start=1):
        order_id = row["order_id"]
        order_date = row["order_date"]
        status = row["status"]

        if status == "cancelled":
            payment_status = "failed"
            paid_at = None
            amount = 0
        else:
            payment_status = "paid"
            paid_at = order_date + timedelta(minutes=random.randint(1, 180))
            amount = round(order_totals_map[order_id], 2)

        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_method": random.choice(payment_methods),
            "payment_status": payment_status,
            "paid_at": paid_at,
            "amount": amount
        })

    return pd.DataFrame(payments)

def generate_returns(
    orders_df: pd.DataFrame,
    order_items_df: pd.DataFrame,
    number_of_returns: int = 300
) -> pd.DataFrame:
    reasons = [
        "Damaged product",
        "Wrong size",
        "Product not as described",
        "Late delivery",
        "Customer changed mind",
        "Defective item"
    ]

    returnable_orders = orders_df[orders_df["status"].isin(["shipped", "returned"])]

    eligible_items = order_items_df[
        order_items_df["order_id"].isin(returnable_orders["order_id"])
    ]

    selected_items = eligible_items.sample(
        n=min(number_of_returns, len(eligible_items)),
        random_state=42
    )

    order_dates = dict(zip(orders_df["order_id"], orders_df["order_date"]))
    returns = []

    for return_id, row in enumerate(selected_items.itertuples(index=False), start=1):
        order_date = order_dates[row.order_id]
        return_date = order_date + timedelta(days=random.randint(1, 30))

        refunded_amount = round(row.quantity * row.unit_price, 2)

        returns.append({
            "return_id": return_id,
            "order_id": row.order_id,
            "product_id": row.product_id,
            "return_date": return_date.date(),
            "reason": random.choice(reasons),
            "refunded_amount": refunded_amount
        })

    return pd.DataFrame(returns)


def main() -> None:
    customers_df = generate_customers()
    products_df = generate_products()
    orders_df = generate_orders(customers_df)
    order_items_df = generate_order_items(orders_df, products_df)
    payments_df = generate_payments(orders_df, order_items_df)
    returns_df = generate_returns(orders_df, order_items_df)

    customers_df.to_csv(RAW_DATA_DIR / "customers.csv", index=False)
    products_df.to_csv(RAW_DATA_DIR / "products.csv", index=False)
    orders_df.to_csv(RAW_DATA_DIR / "orders.csv", index=False)
    order_items_df.to_csv(RAW_DATA_DIR / "order_items.csv", index=False)
    payments_df.to_csv(RAW_DATA_DIR / "payments.csv", index=False)
    returns_df.to_csv(RAW_DATA_DIR / "returns.csv", index=False)

    print("Generated customers.csv")
    print("Generated products.csv")
    print("Generated orders.csv")
    print("Generated order_items.csv")
    print("Generated payments.csv")
    print("Generated returns.csv")


if __name__ == "__main__":
    main()