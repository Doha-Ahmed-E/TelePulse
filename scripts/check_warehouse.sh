#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"

CONTAINER=$(docker compose \
    -f "$ROOT/deployment/docker-compose.yml" \
    ps -q master)

docker exec "$CONTAINER" \
    hive \
    -f /home/jupyter/telepulse/processing/hive/check.hql