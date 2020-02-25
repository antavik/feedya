#!/bin/bash
set -e # exit immediately if a command exits with a non-zero status.

OWNER="feedya"
DB_NAME="feedya_db"
POSTGRES="psql --username postgres"

# create database for superset
echo "Creating database: $DB_NAME"
$POSTGRES <<EOSQL
CREATE DATABASE $DB_NAME OWNER $OWNER;
EOSQL