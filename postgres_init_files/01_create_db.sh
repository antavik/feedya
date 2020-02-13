#!/bin/bash
set -e # exit immediately if a command exits with a non-zero status.

POSTGRES="psql --username postgres"

# create database for superset
echo "Creating database: feedya_db"
$POSTGRES <<EOSQL
CREATE DATABASE feedya_db OWNER feedya;
EOSQL