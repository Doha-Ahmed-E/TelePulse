#!/usr/bin/env bash
set -e

# venv and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Environment ready."

# build and start the cluster
echo "Building images..."
./scripts/build_images.sh

echo "Starting cluster..."
docker compose -f infrastructure/docker-compose.yml up -d
echo "Waiting for Hadoop..."
sleep 30

# merge datasets and upload to HDFS
echo "Merging datasets..."
python3 scripts/merge_datasets.py

echo "Uploading to HDFS..."
./scripts/upload_to_hdfs.sh

