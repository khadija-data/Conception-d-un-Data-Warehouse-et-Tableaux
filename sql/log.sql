CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.load_logs (
    log_id SERIAL PRIMARY KEY,
    table_name TEXT,
    loaded_rows INTEGER,
    status TEXT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO staging.load_logs (
    table_name,
    loaded_rows,
    status
)
SELECT
    'staging.annonces_raw',
    COUNT(*),
    CASE
        WHEN COUNT(*) > 0 THEN 'SUCCESS'
        ELSE 'EMPTY_TABLE'
    END
FROM staging.annonces_raw;

SELECT *
FROM staging.load_logs
ORDER BY loaded_at DESC;