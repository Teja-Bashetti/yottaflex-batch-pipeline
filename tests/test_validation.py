import pytest

import pandas as pd

from validation import validate_customers, validate_orders

import pandas as pd

def test_empty_customers():
    customers_df = pd.DataFrame(
        columns=["customer_id", "customer_name", "email", "city"]
    )

    valid, rejected = validate_customers(customers_df)

    assert len(valid) == 0
    assert len(rejected) == 0


def test_empty_orders():
    orders_df = pd.DataFrame(
        columns=[
            "order_id",
            "customer_id",
            "order_date",
            "amount",
            "order_status"
        ]
    )

    valid_customer_ids = {"C101"}

    valid, rejected = validate_orders(
        orders_df,
        valid_customer_ids
    )

    assert len(valid) == 0
    assert len(rejected) == 0

def test_customers_missing_required_column():
    data = pd.DataFrame([{
        "customer_id": "C101",
        "customer_name": "Rahul",
        "city": "Bangalore"
    }])

    with pytest.raises(ValueError, match="Customers is missing columns"):
        validate_customers(data)


def test_orders_missing_required_column():
    data = pd.DataFrame([{
        "order_id": "O101",
        "customer_id": "C101",
        "order_date": "2026-10-25",
        "order_status": "COMPLETED"
    }])

    with pytest.raises(ValueError, match="Orders is missing columns"):
        validate_orders(data, {"C101"})

def test_valid_customer():
    data = pd.DataFrame([
        {
            "customer_id": "C101",
            "customer_name": "Rahul",
            "email": "rahul@gmail.com",
            "city": "Bangalore"
        }
    ])

    valid, rejected = validate_customers(data)

    assert len(valid) == 1
    assert len(rejected) == 0


def test_duplicate_customer_id():
    data = pd.DataFrame([
        {
            "customer_id": "C101",
            "customer_name": "Rahul",
            "email": "rahul@gmail.com",
            "city": "Bangalore"
        },
        {
            "customer_id": "C101",
            "customer_name": "Teja",
            "email": "teja@gmail.com",
            "city": "Hyderabad"
        }
    ])

    valid, rejected = validate_customers(data)

    assert len(valid) == 1
    assert len(rejected) == 1
    assert "Duplicate customer_id" in rejected.iloc[0]["reject_reason"]


def test_null_customer_id():
    data = pd.DataFrame([
        {
            "customer_id": None,
            "customer_name": "Rahul",
            "email": "rahul@gmail.com",
            "city": "Bangalore"
        }
    ])

    valid, rejected = validate_customers(data)

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "customer_id is null or empty" in rejected.iloc[0]["reject_reason"]


def test_invalid_customer_email():
    data = pd.DataFrame([
        {
            "customer_id": "C101",
            "customer_name": "Rahul",
            "email": "bad-email",
            "city": "Bangalore"
        }
    ])

    valid, rejected = validate_customers(data)

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Invalid email format" in rejected.iloc[0]["reject_reason"]


def test_valid_order():
    data = pd.DataFrame([
        {
            "order_id": "O101",
            "customer_id": "C101",
            "order_date": "2026-10-25",
            "amount": 1500,
            "order_status": "COMPLETED"
        }
    ])

    valid_customer_ids = {"C101"}

    valid, rejected = validate_orders(data, valid_customer_ids)

    assert len(valid) == 1
    assert len(rejected) == 0


def test_negative_order_amount():
    data = pd.DataFrame([
        {
            "order_id": "O101",
            "customer_id": "C101",
            "order_date": "2026-10-25",
            "amount": -500,
            "order_status": "COMPLETED"
        }
    ])

    valid, rejected = validate_orders(data, {"C101"})

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Amount must be greater than zero" in rejected.iloc[0]["reject_reason"]


def test_invalid_order_date():
    data = pd.DataFrame([
        {
            "order_id": "O101",
            "customer_id": "C101",
            "order_date": "invalid-date",
            "amount": 1500,
            "order_status": "COMPLETED"
        }
    ])

    valid, rejected = validate_orders(data, {"C101"})

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Invalid order_date" in rejected.iloc[0]["reject_reason"]


def test_unknown_customer_reference():
    data = pd.DataFrame([
        {
            "order_id": "O101",
            "customer_id": "C999",
            "order_date": "2026-10-25",
            "amount": 1500,
            "order_status": "COMPLETED"
        }
    ])

    valid, rejected = validate_orders(data, {"C101"})

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "Customer ID does not exist" in rejected.iloc[0]["reject_reason"]
def test_non_numeric_order_amount():
    data = pd.DataFrame([{
        "order_id": "O110",
        "customer_id": "C101",
        "order_date": "2026-10-28",
        "amount": "abc",
        "order_status": "COMPLETED"
    }])

    valid, rejected = validate_orders(data, {"C101"})

    assert valid.empty
    assert len(rejected) == 1
    assert "Amount is not numeric" in rejected.iloc[0]["reject_reason"]


def test_invalid_order_status():
    data = pd.DataFrame([{
        "order_id": "O111",
        "customer_id": "C101",
        "order_date": "2026-10-28",
        "amount": "1500",
        "order_status": "CANCELLED_UNKNOWN"
    }])

    valid, rejected = validate_orders(data, {"C101"})

    assert valid.empty
    assert len(rejected) == 1
    assert "Invalid order_status" in rejected.iloc[0]["reject_reason"]