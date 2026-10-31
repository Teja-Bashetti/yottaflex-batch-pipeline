# Data Dictionary – YottaFlex Batch Pipeline

## 1. Overview

This document describes the source datasets, column definitions, expected data types, validation rules, and reject handling implemented in the YottaFlex batch data pipeline.

The pipeline processes two datasets:

- Customers
- Orders

---

## 2. Customers Dataset

**Source file:** `data/input/customers.csv`

**Curated output:** `data/output/curated_customers.csv`

**Reject output:** `data/rejects/customers_rejects.csv`

| Column Name | Data Type | Description | Validation Rule |
|---|---|---|---|
| customer_id | String | Unique identifier for each customer | Required, non-empty, unique |
| customer_name | String | Name of the customer | Required, non-empty |
| email | String | Customer email address | Required, non-empty, basic email format check |
| city | String | Customer's city | Required, non-empty |

### Customer Transformation Rules

- Remove leading and trailing spaces.
- Convert email addresses to lowercase.
- Convert city names to title case.
- Trim customer IDs and customer names.

### Customer Rejection Rules

A customer record is rejected when:

- Customer ID is missing or empty.
- Customer name is missing or empty.
- Email is missing or empty.
- City is missing or empty.
- Customer ID is duplicated.
- Email does not pass the implemented basic format check.

---

## 3. Orders Dataset

**Source file:** `data/input/orders.csv`

**Curated output:** `data/output/curated_orders.csv`

**Reject output:** `data/rejects/orders_rejects.csv`

| Column Name | Data Type | Description | Validation Rule |
|---|---|---|---|
| order_id | String | Unique identifier for each order | Required, non-empty, unique |
| customer_id | String | Customer associated with the order | Required and must reference a valid customer |
| order_date | Date | Date on which the order was placed | Required and must be a valid date |
| amount | Numeric | Monetary value of the order | Required, numeric and greater than zero |
| order_status | String | Current status of the order | Required and must be an allowed status |

### Allowed Order Status Values

- COMPLETED
- PENDING
- SHIPPED

### Order Transformation Rules

- Trim leading and trailing spaces from order ID.
- Trim leading and trailing spaces from customer ID.
- Convert order date into a date format.
- Convert amount into a numeric data type.
- Remove extra spaces from order status.
- Convert order status to uppercase.

### Order Rejection Rules

An order record is rejected when:

- Order ID is missing or empty.
- Customer ID is missing or empty.
- Order date is missing or invalid.
- Amount is missing or non-numeric.
- Amount is zero or negative.
- Order status is missing or invalid.
- Order ID is duplicated.
- Referenced customer ID does not exist in the valid customer dataset.

---

## 4. Reject Dataset Structure

Rejected records are stored separately for investigation.

### Business Validation Rejects

The rejected record contains the original dataset columns and an additional field:

| Column Name | Description |
|---|---|
| reject_reason | Explains why the record failed validation |

Multiple validation failures can be recorded in the same reject_reason field, separated by semicolons.

### Malformed CSV Rejects

Records with an incorrect number of columns are captured with:

| Column Name | Description |
|---|---|
| line_number | Original CSV line number |
| raw_record | Original malformed row representation |
| reject_reason | Reason the row was rejected |

---

## 5. Data Reconciliation

The pipeline validates record counts after ingestion and validation.

**Reconciliation formula:**

Received Records = Accepted Records + Rejected Records

### Sample Reconciliation Results

| Dataset | Received | Accepted | Rejected |
|---|---:|---:|---:|
| Customers | 8 | 5 | 3 |
| Orders | 10 | 6 | 4 |

Both datasets must satisfy the reconciliation formula.

---

## 6. Data Quality Considerations

- Customer IDs and order IDs are treated as unique identifiers.
- Orders must reference valid customers.
- Invalid records are not included in curated datasets.
- Rejected records are retained separately for investigation.
- Synthetic sample data is used for testing and demonstration purposes.

## 7. Notes

The data types and validation rules documented here reflect the current Python pipeline implementation. The email validation is a basic format check and is not a full verification of email deliverability.