import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    layout="wide"
)

st.title("E-commerce Analytics Dashboard")
st.write("Sales, profit, product and customer analytics based on a fictional e-commerce data warehouse.")


@st.cache_data
def load_sales_fact() -> pd.DataFrame:
    query = """
    SELECT
        order_id,
        order_item_id,
        customer_id,
        product_id,
        order_date,
        order_month,
        order_status,
        product_name,
        category,
        brand,
        quantity,
        unit_price,
        cost,
        revenue,
        profit
    FROM sales_fact;
    """

    return pd.read_sql(query, engine)


sales_df = load_sales_fact()

sales_df["order_date"] = pd.to_datetime(sales_df["order_date"])

st.sidebar.header("Filters")

categories = sorted(sales_df["category"].unique())
selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)

filtered_df = sales_df[sales_df["category"].isin(selected_categories)]

total_revenue = filtered_df["revenue"].sum()
total_profit = filtered_df["profit"].sum()
total_orders = filtered_df["order_id"].nunique()
average_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"{total_revenue:,.2f}")
col2.metric("Total Profit", f"{total_profit:,.2f}")
col3.metric("Orders", f"{total_orders:,}")
col4.metric("Average Order Value", f"{average_order_value:,.2f}")

monthly_sales = (
    filtered_df
    .groupby("order_month", as_index=False)
    .agg({
        "revenue": "sum",
        "profit": "sum"
    })
)

st.subheader("Monthly Revenue and Profit")

monthly_chart = px.line(
    monthly_sales,
    x="order_month",
    y=["revenue", "profit"],
    markers=True,
    title="Monthly Revenue and Profit"
)

st.plotly_chart(monthly_chart, use_container_width=True)

category_sales = (
    filtered_df
    .groupby("category", as_index=False)
    .agg({
        "revenue": "sum",
        "profit": "sum"
    })
    .sort_values("revenue", ascending=False)
)

st.subheader("Revenue and Profit by Category")

category_chart = px.bar(
    category_sales,
    x="category",
    y=["revenue", "profit"],
    barmode="group",
    title="Revenue and Profit by Category"
)

st.plotly_chart(category_chart, use_container_width=True)

top_products = (
    filtered_df
    .groupby(["product_id", "product_name", "category"], as_index=False)
    .agg({
        "revenue": "sum",
        "quantity": "sum"
    })
    .sort_values("revenue", ascending=False)
    .head(10)
)

st.subheader("Top 10 Products by Revenue")
st.dataframe(top_products, use_container_width=True)