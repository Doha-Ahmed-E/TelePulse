#!/bin/bash

set -e

CONTAINER=infrastructure-master-1

echo "Creating HDFS directories..."

docker exec $CONTAINER hdfs dfs -mkdir -p /telepulse/raw
docker exec $CONTAINER hdfs dfs -mkdir -p /telepulse/merged

echo "Uploading raw files..."
docker cp data/raw/. $CONTAINER:/tmp/raw
docker exec $CONTAINER bash -c \
"hdfs dfs -put -f /tmp/raw/* /telepulse/raw"

echo "Uploading merged files..."
docker cp data/merged/. $CONTAINER:/tmp/merged
docker exec $CONTAINER bash -c \
"hdfs dfs -put -f /tmp/merged/* /telepulse/merged"

echo "Done!"
docker exec $CONTAINER hdfs dfs -ls -R /telepulse