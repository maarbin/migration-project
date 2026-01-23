# Data Migration Project: Legacy to Modern CRM

A comprehensive end-to-end data migration project simulating a real-world scenario of moving data from a legacy SQL system to a modern CRM architecture.

## Architecture

The project utilizes containerization to simulate an Enterprise environment:

1.  **PostgreSQL (Docker):** A single instance hosting two isolated databases:
    -   **Source (`legacy_db`):** Contains the `raw_data` schema. Populated with intentionally corrupted data (invalid dates, duplicates, mixed types) to simulate a legacy system.
    -   **Target (`target_db`):** Contains the `crm` schema. Represents the strict, normalized destination structure (Modern).
2.  **Python (ETL):** Scripts for data generation, ingestion, and transformation (using `pandas`, `sqlalchemy`, `pydantic`).

## Prerequisites

-   **Python 3.12+**
-   **uv**
-   **Docker & Docker Compose**

## Installation & Usage

### 1. Environment Setup
Install project dependencies:
```bash
uv sync
```
### 2. Infrastructure Launch (Docker)

Initialization scripts (db/initś/01_init_db.sh) will automatically create the databases and schemas upon the first launch.

```bash
docker compose up -d
```
### 3. Data Ingestion Pipeline

Step A: Generate Dirty Data (Staging) Generates a CSV file with realistic data quality issues (simulating a client data dump).
```bash
uv run python src/utils/data_generator.py
```
Output: data/raw/customers_dump.csv

Step B: Seed Legacy Database Loads the CSV data into the PostgreSQL source database.
```bash
uv run python src/utils/seed_legacy_db.py
```

*Current Status:* Ingestion Phase complete. Ready for Data Profiling and ETL Implementation.