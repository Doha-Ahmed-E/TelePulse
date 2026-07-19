#!/bin/bash
set -e

echo "Building base image..."
docker build -t hadoop-hive-spark-base infrastructure/base

echo "Building master..."
docker build -t hadoop-hive-spark-master infrastructure/master

echo "Building worker..."
docker build -t hadoop-hive-spark-worker infrastructure/worker

echo "Building history..."
docker build -t hadoop-hive-spark-history infrastructure/history

echo "Done!"