#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
CONTAINER="infrastructure-master-1"

echo "Deploying processing code..."

docker cp \
    "$ROOT/processing/." \
    "$CONTAINER":/home/jupyter/telepulse/processing

echo "Done."