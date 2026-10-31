# Design Decisions – YottaFlex Batch Pipeline

## 1. Overview

This document explains the technical choices and architectural decisions made while developing the YottaFlex batch data engineering pipeline.

The objective was to build a simple, maintainable, testable, and reproducible batch processing solution.

## 2. Technology Selection

### Python

**Decision:** Python was selected as the primary programming language.

**Reason:**
- Easy to develop and maintain.
- Provides strong data engineering libraries.
- Supports file processing, validation, and automation.
- Suitable for building batch processing applications.

### Pandas

**Decision:** Pandas was selected for data ingestion, validation, and transformation.

**Reason:**
- Provides DataFrame-based processing.
- Supports CSV data handling.
- Makes data cleaning and transformation easier.
- Supports filtering, type conversion, and record validation.

**Trade-off:**

Pandas processes data in memory. It is suitable for this assignment's sample and 100K-record datasets, but very large datasets may require chunk-based processing or a distributed processing framework.

### CSV

**Decision:** CSV was selected as the input and output file format.

**Reason:**
- Simple and human-readable.
- Easy to generate synthetic datasets.
- Supported directly by Pandas and Python.
- Suitable for demonstrating batch ingestion and publishing.

**Trade-off:**

CSV does not provide a strict schema or built-in data types. Therefore, explicit schema and business validations are implemented in Python.

### Pytest

**Decision:** Pytest was selected for automated testing.

**Reason:**
- Simple test structure.
- Supports individual module testing.
- Supports edge-case and end-to-end testing.
- Helps identify regressions when code changes.

### Logging and JSON Metrics

**Decision:** Python logging and JSON files were selected for execution monitoring.

**Reason:**
- Capture pipeline execution details.
- Track unique run IDs.
- Record execution status and duration.
- Store accepted and rejected record counts.
- Capture errors and stack traces.

## 3. Pipeline Architecture Decisions

The pipeline is divided into separate modules.

| Module | Responsibility |
|---|---|
| ingestion.py | Read source CSV files and identify malformed rows |
| validation.py | Apply schema and business validations |
| transformation.py | Clean and standardize accepted records |
| publishing.py | Publish curated and rejected datasets |
| metrics.py | Generate run metrics, logs and reconciliation reports |
| main.py | Orchestrate the complete pipeline |
| data_generator.py | Generate synthetic test datasets |

**Reason for separation:**

Each module has a specific responsibility. This improves maintainability, readability, debugging, and unit testing.

## 4. Data Quality and Reject Handling

**Decision:** Invalid records are separated from valid records rather than silently discarded.

**Reason:**
- Prevent invalid records from entering curated datasets.
- Preserve rejected records for investigation.
- Record rejection reasons.
- Support data quality monitoring.

Two categories of rejects are handled:

1. Malformed CSV records.
2. Business validation failures.

## 5. Customer and Order Relationship

**Decision:** Customer records are validated before order records.

**Reason:**

Orders contain customer IDs that reference the customers dataset.

The pipeline first identifies valid customer IDs and then checks whether each order references an existing valid customer.

This prevents orders with invalid customer references from entering curated output.

## 6. Idempotency

**Decision:** Output CSV files are overwritten instead of appending records.

**Reason:**
- Prevent duplicate accumulation during repeated executions.
- Ensure reproducible outputs for identical inputs.
- Simplify local batch reruns.

**Testing approach:**

The pipeline was executed twice using the same input files. SHA256 hashes of the curated output files were compared. Both runs generated matching hashes.

## 7. Reconciliation

**Decision:** Record-count reconciliation is performed before publishing.

**Formula:**

Received Records = Accepted Records + Rejected Records

**Reason:**

This ensures every ingested record is accounted for as either accepted or rejected.

## 8. Error Handling

**Decision:** Exceptions are logged and failed execution metrics are saved.

**Reason:**
- Identify pipeline failures.
- Capture error tracebacks.
- Record failed run status.
- Preserve execution metrics even when processing fails.

The finally block is used to save execution metrics regardless of whether the pipeline succeeds or fails.

## 9. Synthetic Data Generation

**Decision:** A Python-based data generator was implemented.

**Reason:**
- Avoid using real customer information.
- Create reproducible test datasets.
- Validate the pipeline with larger datasets.
- Support performance benchmarking.

The generator creates 100,000 customer records and 100,000 order records.

## 10. Future Improvements

Potential improvements include:

- Chunk-based CSV processing for larger datasets.
- DuckDB integration for analytical SQL processing.
- Cloud storage integration using Amazon S3.
- Configurable validation rules.
- Stage-level performance metrics.
- Automated CI/CD using GitHub Actions.
- Distributed processing using Apache Spark when dataset scale requires it.

## 11. Conclusion

The selected architecture focuses on modularity, data quality, reproducibility, observability, and automated testing.

The implementation provides a complete local batch-processing workflow while keeping the design extensible for future enhancements.
