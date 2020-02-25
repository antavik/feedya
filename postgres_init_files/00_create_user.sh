#!/bin/bash
set -e # exit if a command exits with a not-zero exit code

USER="feedya"
POSTGRES="psql --username postgres"

# create a shared role to read & write general datasets into postgres
echo "Creating database role: feedya"
$POSTGRES <<-EOSQL
CREATE USER $USER WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	NOINHERIT
	NOREPLICATION
	PASSWORD '$POSTGRES_PASSWORD';
EOSQL