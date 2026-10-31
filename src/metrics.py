
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "reports"
LOG_DIR = REPORT_DIR / "logs"


def generate_run_id():
    """Generate a unique ID for every pipeline execution."""
    return str(uuid4())


def get_current_time():
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


def setup_logger(run_id):
    """Configure pipeline logging."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("yottaflex_pipeline")
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        log_file = LOG_DIR / "pipeline.log"

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        console_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logger.info("Run ID: %s", run_id)

    return logger


def save_run_metrics(metrics):
    """Save execution metrics as a JSON report."""

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    run_id = metrics["run_id"]

    report_file = REPORT_DIR / f"run_metrics_{run_id}.json"

    with open(report_file, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4)

    return report_file


def save_reconciliation_report(metrics):
    """Save record-level reconciliation counts."""

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    run_id = metrics["run_id"]

    report_file = REPORT_DIR / f"reconciliation_{run_id}.csv"

    rows = [
        {
            "dataset": "customers",
            "input_records": metrics["customers_received"],
            "accepted_records": metrics["customers_accepted"],
            "rejected_records": metrics["customers_rejected"]
        },
        {
            "dataset": "orders",
            "input_records": metrics["orders_received"],
            "accepted_records": metrics["orders_accepted"],
            "rejected_records": metrics["orders_rejected"]
        }
    ]

    import pandas as pd

    pd.DataFrame(rows).to_csv(report_file, index=False)

    return report_file

