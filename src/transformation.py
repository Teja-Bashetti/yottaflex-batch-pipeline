
import pandas as pd


def transform_customers(customers_df):
    """
    Clean and standardize customer data.
    """

    transformed_df = customers_df.copy()

    # Remove extra spaces from text columns
    transformed_df["customer_id"] = (
        transformed_df["customer_id"].astype(str).str.strip()
    )

    transformed_df["customer_name"] = (
        transformed_df["customer_name"].astype(str).str.strip()
    )

    transformed_df["email"] = (
        transformed_df["email"].astype(str).str.strip().str.lower()
    )

    transformed_df["city"] = (
        transformed_df["city"].astype(str).str.strip().str.title()
    )

    return transformed_df


def transform_orders(orders_df):
    """
    Clean and standardize order data.
    """

    transformed_df = orders_df.copy()

    # Remove extra spaces
    transformed_df["order_id"] = (
        transformed_df["order_id"].astype(str).str.strip()
    )

    transformed_df["customer_id"] = (
        transformed_df["customer_id"].astype(str).str.strip()
    )

    # Convert order_date into datetime
    transformed_df["order_date"] = pd.to_datetime(
        transformed_df["order_date"],
        errors="raise"
    )

    # Convert amount into numeric datatype
    transformed_df["amount"] = pd.to_numeric(
        transformed_df["amount"],
        errors="raise"
    )

    # Standardize order status
    transformed_df["order_status"] = (
        transformed_df["order_status"].astype(str).str.strip().str.upper()
    )

    return transformed_df
