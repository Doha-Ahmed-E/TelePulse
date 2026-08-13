#!/bin/bash

FILE="$1"

if [ -z "$FILE" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

docker compose -f deployment/docker-compose.yml exec \
    -w /home/jupyter/telepulse \
    master \
    bash -c "PYTHONPATH=/home/jupyter/telepulse spark-submit \
    --master spark://master:7077 \
    processing/ingestion/ingest.py \
    data/uploads/incoming/$FILE"