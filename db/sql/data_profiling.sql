-- Table info
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'raw_data' AND table_name = 'legacy';

-- Table head
SELECT *
FROM raw_data.legacy
LIMIT 5;

-- Completness
SELECT 
    COUNT(*) - COUNT(full_name) AS names_null,
    COUNT(*) - COUNT(email) AS email_null,
    COUNT(*) - COUNT(phone) AS phone_null,
    COUNT(*) - COUNT(registration_date) AS date_null,
    COUNT(*) - COUNT(account_status) AS status_null
FROM raw_data.legacy;

-- Types of account status
SELECT account_status, COUNT(account_status) AS total
FROM raw_data.legacy
GROUP BY account_status
ORDER BY total DESC;

-- Duplicates of mails
SELECT COUNT(*) - COUNT(DISTINCT email) AS duplicates
FROM raw_data.legacy;

-- Formats of phone
SELECT 
    COUNT(*) AS total,
    regexp_replace(phone, '\d', 'X', 'g') AS normalized_phone
FROM raw_data.legacy
GROUP BY normalized_phone
ORDER BY total DESC;

-- Dates to ISO
CREATE VIEW iso_dates AS
    SELECT 
        registration_date,
        CASE
            WHEN registration_date LIKE '%/%' THEN to_date(registration_date, 'DD/MM/YYYY')
            WHEN registration_date LIKE '%.%' THEN  to_date(registration_date, 'DD/MM/YYYY')
            ELSE to_date(registration_date, 'YYYY-MM-DD')
        END AS registration_date_clean
    FROM raw_data.legacy;

-- Check dates range
SELECT 
    MIN(registration_date_clean) AS min_date,
    MAX(registration_date_clean) AS max_date
FROM iso_dates;

-- Dates in the future
WITH countsCTE AS (
    SELECT
        COUNT(*) AS total,
        COALESCE(SUM(CASE WHEN registration_date_clean > CURRENT_DATE THEN 1 END), 0) AS future_dated
    FROM iso_dates
)
SELECT
    total,
    future_dated,
    ROUND((future_dated::NUMERIC / total) * 100, 2) AS future_dated_pct
FROM countsCTE;
