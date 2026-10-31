# YottaFlex Batch Data Engineering Pipeline

## 1. Project Overview

This project implements a batch data engineering pipeline using Python and Pandas. It ingests customer and order CSV files, validates records against business rules, transforms valid data, and publishes curated datasets.

Invalid and malformed records are separated into reject files with rejection reasons for further investigation.

The pipeline also supports execution metrics, reconciliation checks, error logging, automated testing, and repeatable processing.

## 2. Business Requirements

The pipeline processes two datasets:

- Customers
- Orders

It performs the following operations:

1. Read customer and order CSV files.
2. Identify malformed records.
3. Validate required fields and business rules.
4. Detect duplicate records.
5. Validate customer references in orders.
6. Transform accepted records.
7. Publish curated datasets.
8. Store rejected records separately.
9. Generate execution metrics and reconciliation reports.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline development |
| Pandas | Data processing and transformation |
| CSV | Source and output file format |
| Pytest | Automated testing |
| Logging | Pipeline execution monitoring |
| JSON | Run metrics reporting |
| PowerShell | Local execution environment |
| Git | Version control |

## 4. Pipeline Architecture

```text
Customer CSV       Order CSV
     |                 |
     +--------+--------+
              |
         Ingestion
              |
     Malformed Row Check
              |
         Validation
              |
    +---------+----------+
    |                    |
Valid Records       Rejected Records
    |                    |
Transformation       Reject Handling
    |                    |
Curated Outputs      Reject CSV Files
    |
    +------ Metrics and Reconciliation
```

## 5. Data Quality Rules

### Customer validations

- Customer ID must not be null or empty.
- Customer name must not be null or empty.
- Email must not be null or empty.
- Email must have a valid basic email format.
- Customer IDs must be unique.
- City must not be null or empty.

### Order validations

- Order ID must not be null or empty.
- Order ID must be unique.
- Customer ID must exist in the valid customer dataset.
- Order date must be valid.
- Amount must be numeric and greater than zero.
- Order status must be COMPLETED, PENDING, or SHIPPED.

## 6. Project Structure

```text
yottaflex-batch-pipeline/
|
├── config/
├── data/
│   ├── input/
│   ├── backup/
│   ├── output/
│   ├── rejects/
│   └── generated/
|
├── docs/
├── prompts/
├── reports/
├── src/
│   ├── ingestion.py
│   ├── validation.py
│   ├── transformation.py
│   ├── publishing.py
│   ├── metrics.py
│   ├── main.py
│   └── data_generator.py
|
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## 7. Setup Instructions

### Step 1: Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd yottaflex-batch-pipeline
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

## 8. Running the Pipeline

Execute the pipeline using:

```bash
python src/main.py
```

The pipeline reads the default input files from:

```text
data/input/customers.csv
data/input/orders.csv
```

## 9. Generating Large Synthetic Datasets

To generate 100,000 customer and 100,000 order records:

```bash
python src/data_generator.py
```

Generated files are stored in:

```text
data/generated/
```

The pipeline can also be executed with custom input files using:

```powershell
python -c "import sys; sys.path.insert(0, 'src'); from main import run_pipeline; from pathlib import Path; root=Path('data/generated'); run_pipeline(root/'customers_100k.csv', root/'orders_100k.csv')"
```

## 10. Running Automated Tests

Execute:

```bash
pytest -v
```

The test suite covers ingestion, validation, transformations, publishing, and end-to-end pipeline scenarios.

## 11. Monitoring and Reconciliation

Each execution generates:

- Unique run ID.
- Pipeline start and end timestamps.
- Execution duration.
- Pipeline status.
- Input, output, and reject file paths.
- Accepted and rejected record counts.
- Error count and traceback when execution fails.

Metrics are stored as JSON files in:

```text
reports/
```

Reconciliation reports compare received, accepted, and rejected record counts.

The reconciliation rule is:

```text
Received Records = Accepted Records + Rejected Records
```

## 12. Idempotency and Error Handling

The pipeline was tested by executing it multiple times using the same input files.

SHA256 hashes of the curated output files matched across both runs, confirming that the same input produced identical output content.

Missing input files are handled using FileNotFoundError. Failed executions are logged, marked as FAILED, and recorded in the metrics JSON report.

## 13. Current Sample Dataset Results

| Dataset | Received | Accepted | Rejected |
|---|---:|---:|---:|
| Customers | 8 | 5 | 3 |
| Orders | 10 | 6 | 4 |

Both datasets passed reconciliation checks.

## 14. Future Improvements

- Add configurable business rules.
- Add stage-level performance metrics.
- Introduce DuckDB-based analytical processing.
- Add automated CI/CD integration.
- Extend the pipeline for larger datasets and cloud storage.

## 15. Disclaimer

All sample customer and order records used in this project are synthetic and created for demonstration and testing purposes.