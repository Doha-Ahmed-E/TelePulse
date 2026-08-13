#!/usr/bin/env bash

# Bootstrap TelePulse by:
#   1. Copying the historical archive into the master container
#   2. Uploading it to HDFS
#   3. Running the Spark bootstrap job

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"

CONTAINER=$(docker compose \
    -f "$ROOT/deployment/docker-compose.yml" \
    ps -q master)

if [ -z "$CONTAINER" ]; then
    echo "Master container is not running."
    echo "Start the platform first:"
    echo "  cd deployment && docker compose up -d"
    exit 1
fi

TEMP_DIR="/tmp/telepulse/archive"
HDFS_DIR="/telepulse/archive"

echo "Cleaning previous temporary archive..."
docker exec --user root "$CONTAINER" rm -rf /tmp/telepulse

echo "Creating temporary directory..."
docker exec "$CONTAINER" mkdir -p "$TEMP_DIR"

echo "Copying archive into container..."
docker cp \
    "$ROOT/data/archive/." \
    "$CONTAINER:$TEMP_DIR"

echo "Creating HDFS archive directory..."
docker exec  "$CONTAINER" bash -lc "
hdfs dfs -mkdir -p $HDFS_DIR
"

echo "Uploading archive to HDFS..."
docker exec "$CONTAINER" bash -lc "
hdfs dfs -put -f $TEMP_DIR/* $HDFS_DIR
"

echo "Cleaning temporary files..."
docker exec "$CONTAINER" rm -rf /tmp/telepulse

echo "Running Spark bootstrap..."

docker exec "$CONTAINER" bash -lc '
cd /home/jupyter/telepulse
PYTHONPATH=/home/jupyter/telepulse \
spark-submit processing/bootstrap/bootstrap.py
'

echo "Bootstrap completed successfully."