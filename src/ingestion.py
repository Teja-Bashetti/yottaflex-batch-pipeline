
import csv
from pathlib import Path
import pandas as pd


# Find the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Default input file paths
CUSTOMERS_FILE = PROJECT_ROOT / "data" / "input" / "customers.csv"
ORDERS_FILE = PROJECT_ROOT / "data" / "input" / "orders.csv"


def read_csv_with_rejects(file_path):
    """
    Read a CSV file and separate structurally malformed rows.
    """

    valid_records = []
    rejected_records = []

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.reader(file)
        headers = next(reader)

        for line_number, row in enumerate(reader, start=2):

            if len(row) != len(headers):

                rejected_records.append({
                    "line_number": line_number,
                    "raw_record": str(row),
                    "reject_reason": (
                        f"Expected {len(headers)} columns, "
                        f"received {len(row)} columns"
                    )
                })

            else:
                valid_records.append(dict(zip(headers, row)))

    valid_df = pd.DataFrame(valid_records, columns=headers)
    rejected_df = pd.DataFrame(rejected_records)

    return valid_df, rejected_df


def read_customers_with_rejects(file_path=None):
    """
    Read customer CSV using the supplied path.
    If no path is supplied, use the default sample file.
    """

    if file_path is None:
        file_path = CUSTOMERS_FILE

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Customers file not found: {file_path}"
        )

    valid_df, rejected_df = read_csv_with_rejects(file_path)

    print(f"Customers loaded: {len(valid_df)}")
    print(f"Malformed customer records: {len(rejected_df)}")

    return valid_df, rejected_df


def read_orders_with_rejects(file_path=None):
    """
    Read orders CSV using the supplied path.
    If no path is supplied, use the default sample file.
    """

    if file_path is None:
        file_path = ORDERS_FILE

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Orders file not found: {file_path}"
        )

    valid_df, rejected_df = read_csv_with_rejects(file_path)

    print(f"Orders loaded: {len(valid_df)}")
    print(f"Malformed order records: {len(rejected_df)}")

    return valid_df, rejected_df


def read_customers():
    """Read customer data from the default CSV."""

    if not CUSTOMERS_FILE.exists():
        raise FileNotFoundError(
            f"Customers file not found: {CUSTOMERS_FILE}"
        )

    customers_df = pd.read_csv(CUSTOMERS_FILE)

    print(f"Customers loaded: {len(customers_df)} records")

    return customers_df


def read_orders():
    """Read order data from the default CSV."""

    if not ORDERS_FILE.exists():
        raise FileNotFoundError(
            f"Orders file not found: {ORDERS_FILE}"
        )

    orders_df = pd.read_csv(ORDERS_FILE)

    print(f"Orders loaded: {len(orders_df)} records")

    return orders_df


if __name__ == "__main__":

    customers = read_customers()
    orders = read_orders()

    print("\nCustomer Data:")
    print(customers)

    print("\nOrder Data:")
    print(orders)
