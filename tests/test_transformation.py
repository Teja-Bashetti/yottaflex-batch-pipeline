import pandas as pd

from transformation import transform_customers, transform_orders


def test_customer_transformation():
    data = pd.DataFrame([{
        "customer_id": " C101 ",
        "customer_name": " Rahul ",
        "email": "RAHUL@GMAIL.COM",
        "city": "bangalore"
    }])

    result = transform_customers(data)

    assert result.iloc[0]["customer_id"] == "C101"
    assert result.iloc[0]["customer_name"] == "Rahul"
    assert result.iloc[0]["email"] == "rahul@gmail.com"
    assert result.iloc[0]["city"] == "Bangalore"


def test_order_transformation():
    data = pd.DataFrame([{
        "order_id": " O101 ",
        "customer_id": " C101 ",
        "order_date": "2026-10-25",
        "amount": "1500",
        "order_status": "completed"
    }])

    result = transform_orders(data)

    assert result.iloc[0]["order_id"] == "O101"
    assert result.iloc[0]["customer_id"] == "C101"
    assert result.iloc[0]["amount"] == 1500
    assert pd.api.types.is_numeric_dtype(result["amount"])
    assert result.iloc[0]["order_status"] == "COMPLETED"
    assert pd.api.types.is_datetime64_any_dtype(result["order_date"])