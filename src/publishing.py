
from pathlib import Path
import pandas as pd


# Project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Output directories
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
REJECT_DIR = PROJECT_ROOT / "data" / "rejects"


def save_csv(df, file_path):
    """
    Save a DataFrame as a CSV file.
    Create the parent directory if it does not exist.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(file_path, index=False)

    print(f"File published: {file_path}")


def publish_outputs(
    valid_customers,
    valid_orders,
    rejected_customers,
    rejected_orders
):
    """Publish curated records and rejected records."""

    # Curated output files
    save_csv(
        valid_customers,
        OUTPUT_DIR / "curated_customers.csv"
    )

    save_csv(
        valid_orders,
        OUTPUT_DIR / "curated_orders.csv"
    )

    # Rejected records
    save_csv(
        rejected_customers,
        REJECT_DIR / "customers_rejects.csv"
    )

    save_csv(
        rejected_orders,
        REJECT_DIR / "orders_rejects.csv"
    )

    print("\nPublishing completed successfully!")
