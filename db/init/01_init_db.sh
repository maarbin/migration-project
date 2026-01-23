#!/bin/bash
set -e


echo "Initialization of the database..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    CREATE DATABASE legacy_db;
    CREATE DATABASE target_db;
EOSQL

echo "Creating tables in legacy_db..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "legacy_db" -f /docker-entrypoint-initdb.d/02_legacy_schema.sql

echo "Creating tables in target_db..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "target_db" -f /docker-entrypoint-initdb.d/03_target_schema.sql

echo "Initialization succeeded"