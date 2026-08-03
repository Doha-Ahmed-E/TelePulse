#!/usr/bin/env bash

set -euo pipefail

CONTAINER="infrastructure-master-1"

echo "Running Spark bootstrap..."

docker exec "$CONTAINER" bash -lc '
cd /home/jupyter/telepulse &&
PYTHONPATH=/home/jupyter/telepulse \
spark-submit processing/bootstrap/bootstrap.py
'


echo "Bootstrap completed successfully."