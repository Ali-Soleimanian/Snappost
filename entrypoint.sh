#!/bin/bash
set -e

wait_for_postgres() {
  echo "Waiting for PostgreSQL to be ready..."
  echo "Host: $DOCKER_POSTGRES_HOST"
  echo "Port: ${POSTGRES_PORT:-5432}"
  echo "User: $POSTGRES_USER"
  echo "DB: $POSTGRES_DB"

  until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -p "${POSTGRES_PORT:-5432}" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
    echo "Postgres is unavailable - sleeping"
    sleep 2
  done

  echo "PostgreSQL is up - continuing..."
}

wait_for_postgres

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
PORT=${FASTAPI_PORT:-8000}
exec python run.py