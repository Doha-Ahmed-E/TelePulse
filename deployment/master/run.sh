#!/usr/bin/bash

if [ -z "$(ls -A "$NAMEDIR")" ]; then
  echo "Formatting namenode name directory: $NAMEDIR"
  hdfs namenode -format
fi

echo "Starting Hadoop name node..."
hdfs --daemon start namenode

echo "Starting Hadoop secondary name node..."
hdfs --daemon start secondarynamenode

echo "Starting Hadoop resource manager..."
yarn --daemon start resourcemanager

if [ ! -f "$NAMEDIR"/initialized ]; then
  echo "Configuring Hive..."
  hdfs dfs -mkdir -p  /user/hive/warehouse
  schematool -dbType postgres -initSchema
  touch "$NAMEDIR"/initialized
fi

echo "Starting Hive Metastore..."
hive --service metastore &

echo "Starting Hive server2..."
hiveserver2 &

if ! hdfs dfs -test -d /tmp
then
  echo "Formatting directory: /tmp"
  hdfs dfs -mkdir -p  /tmp
fi
if ! hdfs dfs -test -d "$SPARK_LOGS_HDFS_PATH"
then
  echo "Formatting directory: $SPARK_LOGS_HDFS_PATH"
  hdfs dfs -mkdir -p  "$SPARK_LOGS_HDFS_PATH"
fi
if ! hdfs dfs -test -d "$SPARK_JARS_HDFS_PATH"
then
  echo "Formatting directory: $SPARK_JARS_HDFS_PATH"
  hdfs dfs -mkdir -p  "$SPARK_JARS_HDFS_PATH"
  hdfs dfs -put "$SPARK_HOME"/jars/* "$SPARK_JARS_HDFS_PATH"/
fi

echo "Initializing TelePulse HDFS directories..."

until hdfs dfs -test -d /telepulse/raw
do
  if hdfs dfs -mkdir -p /telepulse/raw 2>/dev/null
  then
    break
  fi

  echo "Waiting for HDFS to become ready..."
  sleep 2
done

echo "HDFS directory /telepulse/raw is ready."

echo "Starting Spark master node..."
spark-class org.apache.spark.deploy.master.Master \
    --host master \
    --port 7077 \
    --webui-port 8080