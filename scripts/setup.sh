#!/usr/bin/env bash

set -euo pipefail

echo "Building Docker images..."
./scripts/build_images.sh

echo "Starting cluster..."
docker compose -f infrastructure/docker-compose.yml up -d

echo "Waiting for Hadoop services..."
sleep 30

echo "Cluster is ready."