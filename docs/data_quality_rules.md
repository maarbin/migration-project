# Data Quality Rules

## Business Context
Migrating customer data from legacy system to modern system.
Source: CSV dumps from legacy systems.
Target: PostgreSQL database with normalized schema.

## 1. Email Deduplication
**Rule:** Email must be unique in target system.

**Logic:**
- Sort by `registration_date` DESC (most recent first)
- Keep first occurrence per email address
- Discard older duplicate records

**Logging:**
- Save removed duplicates to `logs/duplicates_removed.csv`
- Include: all fields + reason for removal

**Validation:**
```python
assert df['email'].is_unique, "Duplicates still exist after dedup"
```

## 2. Name Parsing
**Rule:** Split `full_name` into `first_name` and `last_name`.

**Logic:**
```
"John Smith" → first="John", last="Smith"
"Madonna" → first="Madonna", last="UNKNOWN"
"" → first="UNKNOWN", last="UNKNOWN"
```

**Edge Cases:**
- Preserve all characters (titles, suffixes, hyphens)
- No complex parsing - simple split on first space
- `UNKNOWN` indicates missing data for manual review

## 3. Date Validation
**Rule:** `registration_date` must be valid calendar date between business start and today.

**Constraints:**
- Format: YYYY-MM-DD
- Min date: 2020-01-01
- Max date: today

**Action if invalid:**
- Set `registration_date = NULL`
- Log warning with original value
- Record still migrates (date is not critical for CRM)

## 4. Required Fields (NOT NULL)
**Schema requirements:**
- `first_name`: VARCHAR(100) NOT NULL
- `last_name`: VARCHAR(100) NOT NULL  
- `email`: VARCHAR(255) NOT NULL

**Handling missing values:**
| Field | If NULL in source | Action |
|-------|------------------|--------|
| full_name | → | first="UNKNOWN", last="UNKNOWN" |
| email | → | **SKIP RECORD** (email is PK) |
| phone | → | Allow NULL (optional field) |

**Validation:**
```python
# Before load
assert df['first_name'].notna().all()
assert df['last_name'].notna().all()
assert df['email'].notna().all()
```

## 5. Data Type Conversions
| Legacy | Modern | Transformation |
|--------|--------|----------------|
| client_id (INT) | _source_system_id (INT) | Copy as-is |
| - | customer_id (UUID) | Generate new UUID |
| account_status (TEXT) | is_active (BOOLEAN) | "active" → TRUE, else FALSE |
| registration_date (TEXT) | registration_date (DATE) | Parse + validate |

## 6. Idempotency
**Rule:** Running migration multiple times produces same result (no duplicates).

**Implementation:**
```sql
-- Before insert, check existing
SELECT _source_system_id FROM crm.customers;

-- Only insert records NOT in existing IDs
INSERT INTO crm.customers (...) 
WHERE _source_system_id NOT IN (existing_ids);
```

## 7. Batch Processing
**Strategy:** Process in chunks of 1000 records.

**Transaction handling:**
```python
for batch in chunks(df, size=1000):
    try:
        with db.begin():  # Atomic transaction
            load_batch(batch)
    except Exception as e:
        # Rollback automatic
        log_error(batch, e)
        # Continue with next batch
```

**Logging:**
- Success: batch number + row count
- Failure: batch number + error + problematic rows

---

## Review Checklist
Before running production migration:

- [ ] Test with sample dataset (100 rows)
- [ ] Verify idempotency (run twice, check row count)
- [ ] Check audit logs created
- [ ] Validate all constraints in target DB
- [ ] Dry-run mode available (no actual writes)
```

---

# ETL Pipeline - Detailed Design

## 1. EXTRACT
- Input: `data/raw/customers_dump.csv`
- Action: `pd.read_csv()` into DataFrame
- Validation: File exists, has expected columns
- Logging: Row count, column names
- Output: `df_raw` (Pandas DataFrame)

## 2. TRANSFORM (Sequential steps)
- Input: `df_raw`
- Steps:
  a) `remove_duplicates(df)` - Email deduplication
  b) `parse_names(df)` - Split full_name
  c) `normalize_dates(df)` - Parse registration_date
  d) `convert_status(df)` - account_status → is_active
  e) `add_uuids(df)` - Generate customer_id
  f) `rename_columns(df)` - Map to target schema
- Logging: Each transformation logs changes made
- Output: `df_transformed`

## 3. VALIDATE
- Input: `df_transformed`
- Action: Apply Pydantic `CustomerModel` to each row
- Separation: Split into `valid_records` and `invalid_records`
- Logging: 
  - Save `invalid_records` to `logs/validation_errors.csv`
  - Log count of failures + common error types
- Output: `valid_records` (List[CustomerModel])

## 4. LOAD
- Input: `valid_records`
- Pre-check: Query existing `_source_system_id` from target DB
- Filter: Remove already-migrated records (idempotency)
- Action: Batch insert (1000 rows per transaction)
- Error handling: Rollback failed batch, continue with next
- Logging:
  - Each batch: success/failure + row count
  - Overall: total migrated, total skipped, total failed
- Output: Records in `crm.customers` table

## 5. AUDIT REPORT
- Generate summary:
  - Total rows processed
  - Duplicates removed
  - Validation failures
  - Successfully migrated
  - Already existing (skipped)
- Save to: `logs/migration_report_{timestamp}.txt`