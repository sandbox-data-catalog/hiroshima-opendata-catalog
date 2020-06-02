#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE datapusher OWNER ckan ENCODING 'utf-8';
    GRANT ALL PRIVILEGES ON DATABASE datastore TO ckan;
EOSQL
