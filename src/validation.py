
import pandas as pd


def check_required_columns(df, required_columns, dataset_name):
    """Check whether all mandatory columns exist."""

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing columns: {missing_columns}"
        )


def is_blank(value):
    """Check whether a value is null or empty."""

    if pd.isna(value):
        return True

    return isinstance(value, str) and value.strip() == ""


def validate_customers(customers_df):

    required_columns = [
        "customer_id",
        "customer_name",
        "email",
        "city"
    ]

    check_required_columns(
        customers_df,
        required_columns,
        "Customers"
    )

    valid_records = []
    rejected_records = []
    seen_ids = set()

    # Optimized iteration using itertuples()
    for values in customers_df.itertuples(index=False, name=None):

        record = dict(zip(customers_df.columns, values))
        reasons = []

        # Check mandatory fields
        for column in required_columns:
            if is_blank(record[column]):
                reasons.append(f"{column} is null or empty")

        customer_id = record["customer_id"]

        # Check duplicate customer IDs
        if not is_blank(customer_id):
            customer_id = str(customer_id).strip()

            if customer_id in seen_ids:
                reasons.append("Duplicate customer_id")
            else:
                seen_ids.add(customer_id)

        # Basic email validation
        email = record["email"]

        if not is_blank(email):
            email = str(email).strip()

            if "@" not in email or "." not in email.split("@")[-1]:
                reasons.append("Invalid email format")

        if reasons:
            record["reject_reason"] = "; ".join(reasons)
            rejected_records.append(record)
        else:
            valid_records.append(record)

    return (
        pd.DataFrame(valid_records, columns=required_columns),
        pd.DataFrame(
            rejected_records,
            columns=required_columns + ["reject_reason"]
        )
    )


def validate_orders(orders_df, valid_customer_ids):

    required_columns = [
        "order_id",
        "customer_id",
        "order_date",
        "amount",
        "order_status"
    ]

    check_required_columns(
        orders_df,
        required_columns,
        "Orders"
    )

    valid_records = []
    rejected_records = []
    seen_ids = set()

    allowed_statuses = {
        "COMPLETED",
        "PENDING",
        "SHIPPED"
    }

    # Optimized iteration using itertuples()
    for values in orders_df.itertuples(index=False, name=None):

        record = dict(zip(orders_df.columns, values))
        reasons = []

        # Check mandatory fields
        for column in required_columns:
            if is_blank(record[column]):
                reasons.append(f"{column} is null or empty")

        order_id = record["order_id"]

        # Check duplicate order IDs
        if not is_blank(order_id):
            order_id = str(order_id).strip()

            if order_id in seen_ids:
                reasons.append("Duplicate order_id")
            else:
                seen_ids.add(order_id)

        # Check customer foreign key
        customer_id = record["customer_id"]

        if not is_blank(customer_id):
            customer_id = str(customer_id).strip()

            if customer_id not in valid_customer_ids:
                reasons.append("Customer ID does not exist")

        # Validate order date
        order_date = pd.to_datetime(
            record["order_date"],
            errors="coerce"
        )

        if pd.isna(order_date):
            reasons.append("Invalid order_date")

        # Validate amount
        amount = pd.to_numeric(
            record["amount"],
            errors="coerce"
        )

        if pd.isna(amount):
            reasons.append("Amount is not numeric")
        elif amount <= 0:
            reasons.append("Amount must be greater than zero")

        # Validate order status
        status = record["order_status"]

        if not is_blank(status):
            if str(status).strip().upper() not in allowed_statuses:
                reasons.append("Invalid order_status")

        if reasons:
            record["reject_reason"] = "; ".join(reasons)
            rejected_records.append(record)
        else:
            valid_records.append(record)

    return (
        pd.DataFrame(valid_records, columns=required_columns),
        pd.DataFrame(
            rejected_records,
            columns=required_columns + ["reject_reason"]
        )
    )


if __name__ == "__main__":

    from ingestion import read_customers, read_orders

    customers_df = read_customers()
    orders_df = read_orders()

    valid_customers, rejected_customers = validate_customers(
        customers_df
    )

    valid_customer_ids = set(
        valid_customers["customer_id"].astype(str).str.strip()
    )

    valid_orders, rejected_orders = validate_orders(
        orders_df,
        valid_customer_ids
    )

    print("\nCUSTOMER VALIDATION")
    print(f"Valid customers: {len(valid_customers)}")
    print(f"Rejected customers: {len(rejected_customers)}")

    print("\nORDER VALIDATION")
    print(f"Valid orders: {len(valid_orders)}")
    print(f"Rejected orders: {len(rejected_orders)}")
