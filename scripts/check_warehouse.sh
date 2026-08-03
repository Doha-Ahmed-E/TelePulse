#!/usr/bin/env bash

set -euo pipefail

CONTAINER="infrastructure-master-1"

docker exec "$CONTAINER" \
    hive \
    -f /home/jupyter/telepulse/processing/hive/check.hql