
import csv
import random
from pathlib import Path
from datetime import date, timedelta


# Project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Store generated files separately
OUTPUT_DIR = PROJECT_ROOT / "data" / "generated"


def generate_customers(total_customers=100_000):
    """
    Generate synthetic customer records.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    customers_file = OUTPUT_DIR / "customers_100k.csv"

    cities = [
        "Bangalore",
        "Hyderabad",
        "Chennai",
        "Mumbai",
        "Pune",
        "Delhi",
        "Kolkata"
    ]

    with open(
        customers_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "customer_id",
            "customer_name",
            "email",
            "city"
        ])

        for i in range(1, total_customers + 1):

            writer.writerow([
                f"C{i:06d}",
                f"Customer_{i}",
                f"customer{i}@example.com",
                random.choice(cities)
            ])

    print(f"Customers generated: {total_customers}")
    print(f"File saved: {customers_file}")


def generate_orders(
    total_orders=100_000,
    total_customers=100_000
):
    """
    Generate synthetic order records.
    """

    orders_file = OUTPUT_DIR / "orders_100k.csv"

    statuses = [
        "COMPLETED",
        "PENDING",
        "SHIPPED"
    ]

    start_date = date(2025, 1, 1)

    with open(
        orders_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "order_id",
            "customer_id",
            "order_date",
            "amount",
            "order_status"
        ])

        for i in range(1, total_orders + 1):

            customer_number = random.randint(
                1,
                total_customers
            )

            order_date = start_date + timedelta(
                days=random.randint(0, 600)
            )

            amount = round(
                random.uniform(100, 10000),
                2
            )

            writer.writerow([
                f"O{i:06d}",
                f"C{customer_number:06d}",
                order_date.isoformat(),
                amount,
                random.choice(statuses)
            ])

    print(f"Orders generated: {total_orders}")
    print(f"File saved: {orders_file}")


def main():

    random.seed(42)

    print("Starting synthetic data generation...")

    generate_customers(100_000)

    generate_orders(
        total_orders=100_000,
        total_customers=100_000
    )

    print("\nData generation completed successfully!")


if __name__ == "__main__":
    main()
