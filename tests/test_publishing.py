import pandas as pd

from publishing import publish_outputs


def test_publish_outputs(tmp_path):
    customers = pd.DataFrame([{
        "customer_id": "C101",
        "customer_name": "Rahul",
        "email": "rahul@gmail.com",
        "city": "Bangalore"
    }])

    orders = pd.DataFrame([{
        "order_id": "O101",
        "customer_id": "C101",
        "order_date": "2026-10-25",
        "amount": 1500,
        "order_status": "COMPLETED"
    }])

    rejected_customers = pd.DataFrame(columns=[
        "customer_id", "customer_name", "email",
        "city", "reject_reason"
    ])

    rejected_orders = pd.DataFrame(columns=[
        "order_id", "customer_id", "order_date",
        "amount", "order_status", "reject_reason"
    ])

    # Temporary output folders for testing
    import publishing

    publishing.OUTPUT_DIR = tmp_path / "output"
    publishing.REJECT_DIR = tmp_path / "rejects"

    publish_outputs(
        customers,
        orders,
        rejected_customers,
        rejected_orders
    )

    assert (tmp_path / "output" / "curated_customers.csv").exists()
    assert (tmp_path / "output" / "curated_orders.csv").exists()
    assert (tmp_path / "rejects" / "customers_rejects.csv").exists()
    assert (tmp_path / "rejects" / "orders_rejects.csv").exists()

    saved_customers = pd.read_csv(
        tmp_path / "output" / "curated_customers.csv"
    )

    assert len(saved_customers) == 1
    assert saved_customers.iloc[0]["customer_id"] == "C101"