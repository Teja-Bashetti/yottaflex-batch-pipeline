
import time
import traceback
import pandas as pd

from ingestion import (
    read_customers_with_rejects,
    read_orders_with_rejects
)

from validation import validate_customers, validate_orders
from transformation import transform_customers, transform_orders
from publishing import publish_outputs

from metrics import (
    generate_run_id,
    get_current_time,
    setup_logger,
    save_run_metrics,
    save_reconciliation_report
)


def run_pipeline(customers_file=None, orders_file=None):

    # Generate unique Run ID
    run_id = generate_run_id()

    # Configure logger
    logger = setup_logger(run_id)

    # Capture start time
    start_time = get_current_time()
    start_clock = time.perf_counter()

    # Initialize metrics
    metrics = {
        "run_id": run_id,
        "start_time": start_time,
        "end_time": None,
        "duration_seconds": 0,
        "status": "RUNNING",

        # Input file locations
        "input_files": {
            "customers": str(
                customers_file or "data/input/customers.csv"
            ),
            "orders": str(
                orders_file or "data/input/orders.csv"
            )
        },

        # Curated output file locations
        "output_files": {
            "customers": "data/output/curated_customers.csv",
            "orders": "data/output/curated_orders.csv"
        },

        # Rejected records file locations
        "reject_files": {
            "customers": "data/rejects/customers_rejects.csv",
            "orders": "data/rejects/orders_rejects.csv"
        },

        # Pipeline execution error count
        "error_count": 0,

        # Record counts
        "customers_received": 0,
        "customers_accepted": 0,
        "customers_rejected": 0,
        "orders_received": 0,
        "orders_accepted": 0,
        "orders_rejected": 0
    }

    reconciliation_ready = False

    try:
        logger.info("YOTTAFLEX BATCH PIPELINE STARTED")

        # STEP 1: Read source data
        logger.info("STEP 1: Reading source data")

        if customers_file is None:
            customers_df, malformed_customers = (
                read_customers_with_rejects()
            )
        else:
            customers_df, malformed_customers = (
                read_customers_with_rejects(customers_file)
            )

        if orders_file is None:
            orders_df, malformed_orders = (
                read_orders_with_rejects()
            )
        else:
            orders_df, malformed_orders = (
                read_orders_with_rejects(orders_file)
            )

        # STEP 2: Validate customers
        logger.info("STEP 2: Validating customers")

        valid_customers, validation_rejected_customers = (
            validate_customers(customers_df)
        )

        # Get valid customer IDs for order validation
        valid_customer_ids = set(
            valid_customers["customer_id"].astype(str).str.strip()
        )

        # STEP 3: Validate orders
        logger.info("STEP 3: Validating orders")

        valid_orders, validation_rejected_orders = validate_orders(
            orders_df,
            valid_customer_ids
        )

        # Combine validation rejects and malformed CSV rejects
        rejected_customers = pd.concat(
            [validation_rejected_customers, malformed_customers],
            ignore_index=True,
            sort=False
        )

        rejected_orders = pd.concat(
            [validation_rejected_orders, malformed_orders],
            ignore_index=True,
            sort=False
        )

        # STEP 4: Update record counts
        logger.info("STEP 4: Updating record counts")

        metrics.update({
            "customers_received": (
                len(customers_df) + len(malformed_customers)
            ),
            "customers_accepted": len(valid_customers),
            "customers_rejected": len(rejected_customers),

            "orders_received": (
                len(orders_df) + len(malformed_orders)
            ),
            "orders_accepted": len(valid_orders),
            "orders_rejected": len(rejected_orders)
        })

        reconciliation_ready = True

        # STEP 5: Reconciliation checks
        logger.info("STEP 5: Performing reconciliation")

        assert (
            metrics["customers_received"]
            == metrics["customers_accepted"]
            + metrics["customers_rejected"]
        ), "Customer reconciliation failed"

        assert (
            metrics["orders_received"]
            == metrics["orders_accepted"]
            + metrics["orders_rejected"]
        ), "Order reconciliation failed"

        logger.info("Customer reconciliation passed")
        logger.info("Order reconciliation passed")

        # STEP 6: Transform accepted records
        logger.info("STEP 6: Transforming accepted records")

        valid_customers = transform_customers(valid_customers)
        valid_orders = transform_orders(valid_orders)

        logger.info("Customer transformation completed")
        logger.info("Order transformation completed")

        # STEP 7: Publish output files
        logger.info("STEP 7: Publishing output files")

        publish_outputs(
            valid_customers,
            valid_orders,
            rejected_customers,
            rejected_orders
        )

        metrics["status"] = "SUCCESS"

        logger.info("YOTTAFLEX BATCH PIPELINE COMPLETED SUCCESSFULLY")

    except Exception:
        # Capture pipeline failure
        metrics["status"] = "FAILED"
        metrics["error_count"] = 1
        metrics["error"] = traceback.format_exc()

        logger.exception("Pipeline execution failed")

        raise

    finally:
        # Capture end time and execution duration
        metrics["end_time"] = get_current_time()

        metrics["duration_seconds"] = round(
            time.perf_counter() - start_clock,
            3
        )

        # Save JSON metrics report
        report_file = save_run_metrics(metrics)

        logger.info("Metrics report saved: %s", report_file)

        # Save reconciliation report
        if reconciliation_ready:
            reconciliation_file = save_reconciliation_report(metrics)

            logger.info(
                "Reconciliation report saved: %s",
                reconciliation_file
            )

        logger.info("Run ID: %s", run_id)
        logger.info("Pipeline status: %s", metrics["status"])
        logger.info("Error count: %s", metrics["error_count"])

        logger.info(
            "Execution duration: %s seconds",
            metrics["duration_seconds"]
        )


if __name__ == "__main__":
    run_pipeline()
