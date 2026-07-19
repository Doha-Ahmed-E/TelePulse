#!/bin/bash
set -e

echo "Building base image..."
docker build -t hadoop-hive-spark-base base

echo "Building master..."
docker build -t hadoop-hive-spark-master master

echo "Building worker..."
docker build -t hadoop-hive-spark-worker worker

echo "Building history..."
docker build -t hadoop-hive-spark-history history

echo "Done!"