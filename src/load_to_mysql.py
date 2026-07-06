from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

DB_USER = "root"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "Warehouse"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


TABLE_LOAD_ORDER = [
    "customers",
    "products",
    "orders",
    "order_items",
    "payments",
    "returns",
]


def load_csv_to_mysql(table_name: str) -> None:
    file_path = RAW_DATA_DIR / f"{table_name}.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    df = pd.read_csv(file_path)

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(df)} rows into {table_name}")


def main() -> None:
    for table_name in TABLE_LOAD_ORDER:
        load_csv_to_mysql(table_name)

    print("All CSV files loaded into MySQL successfully.")


if __name__ == "__main__":
    main()