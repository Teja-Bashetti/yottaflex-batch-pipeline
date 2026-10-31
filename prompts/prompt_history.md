# AI Prompt History

## 1. Purpose

This document records the AI assistance used during the development of the YottaFlex batch data engineering pipeline.

AI was used as a development assistant to support project planning, implementation guidance, debugging, testing, performance optimization, and documentation.

All generated or suggested code was reviewed, executed, tested, and understood before being included in the project.

## 2. Representative Prompts Used

The following prompts represent the main areas where AI assistance was used during development. They are summaries of the prompts and may not reproduce the original wording verbatim.

### 2.1 Project Planning and Architecture

**Prompt:**  
Help me plan a Python-based batch data engineering pipeline for the YottaFlex assignment. Suggest a modular project structure and explain the responsibilities of each module.

**AI Assistance:**
- Suggested the project folder structure.
- Explained the responsibilities of ingestion, validation, transformation, publishing, and monitoring modules.
- Helped break the assignment into manageable implementation stages.

### 2.2 Data Ingestion

**Prompt:**  
Help me implement CSV ingestion using Python and Pandas. Explain how to handle malformed CSV records and missing input files.

**AI Assistance:**
- Helped implement CSV reading logic.
- Added malformed-record detection based on column counts.
- Added file existence checks and clear error messages.

### 2.3 Data Validation

**Prompt:**  
Help me implement customer and order validation with required-field checks, duplicate detection, email validation, date validation, amount validation, and customer referential integrity.

**AI Assistance:**
- Helped define data quality rules.
- Implemented valid and rejected record separation.
- Added rejection reasons for invalid records.
- Helped cover business-specific validation scenarios.

### 2.4 Data Transformation and Publishing

**Prompt:**  
Help me implement transformation logic for customer and order datasets and publish curated and rejected records into separate CSV files.

**AI Assistance:**
- Suggested standardization of text fields.
- Helped implement date and numeric conversions.
- Implemented separate curated and rejected output paths.

### 2.5 Logging, Metrics, and Reconciliation

**Prompt:**  
Help me add run IDs, execution timestamps, processing duration, record counts, error tracking, JSON metrics, and reconciliation reports to the pipeline.

**AI Assistance:**
- Helped implement unique run IDs.
- Added structured execution logging.
- Added success and failure metrics.
- Implemented reconciliation checks to compare received, accepted, and rejected records.

### 2.6 Synthetic Data Generation

**Prompt:**  
Help me generate reproducible synthetic customer and order CSV datasets with 100,000 records each to test pipeline scalability.

**AI Assistance:**
- Helped create a Python data generator.
- Added deterministic random seed usage.
- Generated 100,000 customer records and 100,000 order records.

### 2.7 Automated Testing

**Prompt:**  
Help me write pytest test cases for ingestion, validation, transformation, publishing, and end-to-end pipeline execution. Include empty datasets and invalid records.

**AI Assistance:**
- Helped organize automated tests.
- Suggested positive and negative test scenarios.
- Helped verify expected accepted and rejected record counts.

### 2.8 Performance Optimization

**Prompt:**  
Review the validation logic and suggest ways to improve performance when processing large CSV datasets.

**AI Assistance:**
- Identified row-wise `iterrows()` processing as an optimization opportunity.
- Suggested using `itertuples()` to reduce iteration overhead.
- Helped prepare a before-and-after performance benchmark.

### 2.9 Idempotency Testing

**Prompt:**  
Explain how to verify that running the same batch pipeline multiple times with identical input files does not append duplicate output records.

**AI Assistance:**
- Explained overwrite-based publishing.
- Suggested comparing SHA256 hashes of curated output files across repeated runs.
- Helped interpret the test results.

### 2.10 Project Documentation

**Prompt:**  
Help me prepare professional project documentation covering the README, data dictionary, design decisions, setup instructions, validation rules, and operational behavior.

**AI Assistance:**
- Helped organize technical documentation.
- Explained implementation choices and trade-offs.
- Helped document the pipeline's limitations and possible future improvements.

## 3. Human Review and Verification

AI suggestions were not accepted blindly. The implementation was reviewed and executed locally.

The following verification activities were performed:

- Executed the pipeline using sample customer and order CSV files.
- Verified accepted and rejected record counts.
- Tested malformed records and invalid business data.
- Executed automated tests using pytest.
- Generated and processed synthetic datasets containing 100,000 customers and 100,000 orders.
- Tested successful and failed pipeline executions.
- Verified run metrics and reconciliation reports.
- Compared SHA256 hashes to verify repeatable output for identical input files.

## 4. Responsible AI Usage

AI was used to accelerate development and support learning. The developer reviewed the code, tested the implementation, understood the processing logic, and verified the results.

No real customer or confidential production data was used. Synthetic datasets were used for development and testing.

## 5. Summary

AI assistance supported the development lifecycle, including planning, coding, debugging, testing, optimization, and documentation. Final implementation decisions and local verification were performed as part of the project development process.
