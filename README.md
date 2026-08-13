# TelePulse

A production-inspired batch data engineering platform built with **Hadoop, Spark, Hive, and Docker** for processing large-scale mobile network activity data.

TelePulse ingests historical and newly uploaded telecom datasets, validates and transforms them with Spark, stores them in HDFS/Hive, and exposes analytics through a REST API.

---

## Architecture

```text
                    TelePulse
                        │
          ┌─────────────┴─────────────┐
          │                           │
   Historical Data              Upload API
          │                           │
          ▼                           ▼
   HDFS Archive              Incoming Directory
                                      │
                                      ▼
                                  File Watcher
                                      │
                                      ▼
                               Spark Ingestion
                                      │
                              ┌───────┴───────┐
                              │               │
                           Processed       Rejected
                              │               │
                              ▼               ▼
                            HDFS            HDFS
                              │
                              ▼
                         Hive Warehouse
                              │
                              ▼
                        Analytics API
````

---

## Technology Stack

* Python
* FastAPI
* Docker & Docker Compose
* Hadoop HDFS
* Apache Spark
* Apache Hive
* PyHive

---

## Project Structure

```text
TelePulse/
│
├── api/
│   ├── routes/
│   └── services/
│
├── data/
│   ├── archive/
│   └── uploads/
│       ├── incoming/
│       ├── processed/
│       └── rejected/
│
├── deployment/
│
├── docs/
│
├── infrastructure/
│
├── processing/
│   ├── bootstrap/
│   ├── common/
│   ├── hive/
│   └── ingestion/
│
├── scripts/
│
├── Makefile
└── README.md
```

---

## Dataset

TelePulse uses the **Telecom Italia Big Data Challenge** dataset.

[https://www.kaggle.com/datasets/marcodena/mobile-phone-activity](https://www.kaggle.com/datasets/marcodena/mobile-phone-activity)

Historical datasets should be placed in:

```text
data/archive/
```

---

## Getting Started

```bash
cd TelePulse

make base      # one-time setup
make up
./scripts/bootstrap.sh
```

The bootstrap process initializes the Hive warehouse and analytics views from the historical data.

Check HDFS with:

```bash
docker compose -f deployment/docker-compose.yml exec master \
hdfs dfs -ls -R /telepulse
```

---

## Incremental Ingestion

New datasets can be uploaded through the API:

```text
POST /upload
```

Uploaded files are placed in:

```text
data/uploads/incoming/
```

A background watcher monitors this directory and automatically triggers the Spark ingestion pipeline when a new supported CSV file appears.

The ingestion pipeline:

1. Detects the uploaded file
2. Validates the dataset type and schema
3. Uploads the file to HDFS
4. Processes it with Spark
5. Appends the data to the Hive warehouse
6. Moves successful files to `processed/`
7. Moves failed files to `rejected/`

You can also trigger ingestion manually:

```bash
./scripts/run_ingestion.sh <filename>
```

---

## Analytics API

The backend exposes analytics endpoints for the processed warehouse data:

```text
GET /analytics/overview
GET /analytics/cells
GET /analytics/hourly
GET /analytics/hourly?province=<province>
```

The API retrieves the latest data from Hive, so newly ingested files are reflected in subsequent analytics queries.

---

## HDFS Safe Mode

On the first startup, Hadoop may temporarily keep the NameNode in safe mode while DataNodes register.

Check the current state with:

```bash
docker compose -f deployment/docker-compose.yml exec master \
hdfs dfsadmin -safemode get
```

If ingestion fails because the NameNode is in safe mode, wait a few seconds and retry.

---

## Current Status

*  Dockerized Hadoop cluster
*  HDFS data lake
*  Spark ETL pipeline
*  Hive data warehouse
*  Historical bootstrap
*  Schema validation
*  Data transformation
*  Incremental ingestion
*  Upload API
*  Automatic folder watcher
*  Processed/rejected file workflow
*  Analytics REST API

---

## Roadmap

* Improve analytics query performance
* Add stronger ingestion monitoring and error reporting
* Improve API response optimization
* Add automated tests

---

## License

This project is intended for educational and portfolio purposes.
