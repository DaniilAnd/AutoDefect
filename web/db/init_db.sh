#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    user_id INT not null,
    image_path VARCHAR(255) not null,
    bbox_json JSONB not null,
    time_escalation TIMESTAMP not null,
    gps_coordinates JSONB not null,
    city VARCHAR(255) not null,
    street VARCHAR(255) not null,
    state VARCHAR(255) not null
);
EOSQL