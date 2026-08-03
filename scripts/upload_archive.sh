#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
CONTAINER="infrastructure-master-1"

docker exec "$CONTAINER" mkdir -p \
    /home/jupyter/telepulse/temp
TEMP_DIR="/home/jupyter/telepulse/temp/archive"

echo "Cleaning previous archive..."
docker exec "$CONTAINER" rm -rf "$TEMP_DIR"

echo "Creating temporary directory..."
docker exec "$CONTAINER" mkdir -p "$TEMP_DIR"

echo "Copying archive..."
docker cp \
    "$ROOT/data/archive/." \
    "$CONTAINER":"$TEMP_DIR"

echo "Uploading to HDFS..."
docker exec "$CONTAINER" bash -c \
    "hdfs dfs -mkdir -p /telepulse/archive"

docker exec "$CONTAINER" bash -c \
    "hdfs dfs -put -f $TEMP_DIR/* /telepulse/archive"

echo "Cleaning temporary files..."
docker exec "$CONTAINER" rm -rf "$TEMP_DIR"