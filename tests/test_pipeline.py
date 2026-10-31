
import json
import pandas as pd
import main

from pathlib import Path


def test_pipeline_end_to_end():
    main.run_pipeline()

    project_root = Path(__file__).resolve().parent.parent

    output_dir = project_root / "data" / "output"
    reject_dir = project_root / "data" / "rejects"
    report_dir = project_root / "reports"

    # Check curated output files
    assert (output_dir / "curated_customers.csv").exists()
    assert (output_dir / "curated_orders.csv").exists()

    # Check reject files
    assert (reject_dir / "customers_rejects.csv").exists()
    assert (reject_dir / "orders_rejects.csv").exists()

    # Find the latest metrics report
    metrics_files = list(report_dir.glob("run_metrics_*.json"))
    assert len(metrics_files) > 0

    latest_report = max(
        metrics_files,
        key=lambda file: file.stat().st_mtime
    )

    with open(latest_report, "r", encoding="utf-8") as file:
        metrics = json.load(file)

    assert metrics["status"] == "SUCCESS"
    assert metrics["customers_received"] == 8
    assert metrics["customers_accepted"] == 5
    assert metrics["customers_rejected"] == 3
    assert metrics["orders_received"] == 10
    assert metrics["orders_accepted"] == 6
    assert metrics["orders_rejected"] == 4


def test_pipeline_with_empty_datasets(monkeypatch):

    project_root = Path(__file__).resolve().parent.parent

    # Create empty customer dataset
    empty_customers = pd.DataFrame(
        columns=[
            "customer_id",
            "customer_name",
            "email",
            "city"
        ]
    )

    # Create empty order dataset
    empty_orders = pd.DataFrame(
        columns=[
            "order_id",
            "customer_id",
            "order_date",
            "amount",
            "order_status"
        ]
    )

    # Create empty malformed records DataFrame
    empty_malformed = pd.DataFrame(
        columns=[
            "line_number",
            "raw_record",
            "reject_reason"
        ]
    )

    # Mock customer ingestion
    monkeypatch.setattr(
        main,
        "read_customers_with_rejects",
        lambda: (empty_customers, empty_malformed)
    )

    # Mock order ingestion
    monkeypatch.setattr(
        main,
        "read_orders_with_rejects",
        lambda: (empty_orders, empty_malformed)
    )

    # Execute pipeline with empty datasets
    main.run_pipeline()

    # Check generated output files
    customers_output = pd.read_csv(
        project_root / "data" / "output" / "curated_customers.csv"
    )

    orders_output = pd.read_csv(
        project_root / "data" / "output" / "curated_orders.csv"
    )

    assert len(customers_output) == 0
    assert len(orders_output) == 0

