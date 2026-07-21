#!/usr/bin/env bash
set -euo pipefail

# venv and install dependencies
python -m venv .venv
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
python data/merge_datasets.py

echo "Uploading to HDFS..."
./data/upload_to_hdfs.sh

docker exec infrastructure-master-1 \
    hdfs dfs -ls -R /telepulse

# copying processing scripts to the master node
docker exec infrastructure-master-1 mkdir -p /home/jupyter/telepulse
docker cp processing infrastructure-master-1:/home/jupyter/telepulse/

# running the pipeline
echo "Running the TelePulse spark pipeline..."
docker exec infrastructure-master-1 \
    spark-submit /home/jupyter/telepulse/processing/spark/pipeline.py

# running the hive scripts to create views
echo "Creating Hive views..."

docker exec infrastructure-master-1 hive -f \
    /home/jupyter/telepulse/processing/hive/create_views.hql

docker exec infrastructure-master-1 hive -f \
    /home/jupyter/telepulse/processing/hive/validation.hql



echo "TelePulse pipeline completed successfully!"