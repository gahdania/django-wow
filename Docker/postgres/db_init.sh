#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE "$DJANGO_DB_USER" WITH NOSUPERUSER NOCREATEDB NOCREATEROLE LOGIN PASSWORD "$DJANGO_DB_PASSWORD';
    CREATE DATABASE "$DJANGO_DB_NAME" WITH OWNER "$DJANGO_DB_USER";
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DJANGO_DB_NAME" < db_base_postgres

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE ROLE "$MAIL_DB_USER" WITH NOSUPERUSER NOCREATEDB NOCREATEROLE LOGIN PASSWORD "$MAIL_DB_PASSWORD";
    CREATE DATABASE "$MAIL_DB_NAME" WITH OWNER "$MAIL_DB_USER";
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$" <
