# TelePulse

A production-inspired batch data engineering platform built with **Hadoop**, **Spark**, **Hive**, and **Docker** for processing large-scale mobile network activity data.

TelePulse transforms historical telecom activity datasets into an analytics-ready data warehouse using a modular Spark ETL pipeline running on a distributed Hadoop cluster.

---

# Features

- Dockerized Hadoop ecosystem
- HDFS data lake
- Spark batch ETL pipeline
- Hive data warehouse
- Historical dataset bootstrap
- Data validation
- Data transformation
- Analytics views
- Modular processing package
- Deployment script for processing code
- Foundation for incremental batch ingestion

---

# Architecture

```text
                    Local Machine
                    ─────────────

          Processing Code        Historical Dataset
                 │                      │
                 ▼                      ▼
     deploy_processing.sh     upload_archive.sh
                 │                      │
                 ▼                      ▼
        Hadoop Master Container      HDFS
                 │                      │
                 └──────────┬───────────┘
                            ▼
                     bootstrap.sh
                            │
                            ▼
                  Spark Validation
                            │
                            ▼
                Spark Transformation
                            │
                            ▼
                  Hive Warehouse
                            │
                            ▼
                    Analytics Views
```

---

# Technology Stack

- Python
- Docker
- Docker Compose
- Hadoop HDFS
- YARN
- Apache Spark
- Apache Hive

---

# Project Structure

```text
TelePulse/
│
├── api/
│
├── data/
│   ├── archive/
│   ├── incoming/
│   ├── processed/
│   └── rejected/
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
└── README.md
```

---

# Prerequisites

- Docker
- Docker Compose

---

# Dataset

TelePulse uses the **Telecom Italia Big Data Challenge** dataset.

https://www.kaggle.com/datasets/marcodena/mobile-phone-activity

Download the dataset and extract the required files into:

```text
data/archive/
```

Example:

```text
data/
└── archive/
    ├── ISTAT_census_variables_2011.csv
    ├── Italian_provinces.geojson
    ├── milano-grid.geojson
    ├── sms-call-internet-mi-2013-11-01.csv
    ├── sms-call-internet-mi-2013-11-02.csv
    ├── ...
    ├── mi-to-provinces-2013-11-01.csv
    ├── mi-to-provinces-2013-11-02.csv
    └── ...
```

---

# Getting Started

Clone the repository:

```bash
git clone https://github.com/Doha-Ahmed-E/TelePulse.git
cd TelePulse
```

Start the Hadoop cluster:

```bash
docker compose up -d
```

Deploy the processing package into the master container:

```bash
./scripts/deploy_processing.sh
```

Upload the historical archive to HDFS:

```bash
./scripts/upload_archive.sh
```

Initialize the warehouse:

```bash
./scripts/bootstrap.sh
```

Verify the deployment:

```bash
./scripts/check.sh
```

---

# Available Scripts

## deploy_processing.sh

Copies the latest `processing/` package from the local project into the Hadoop master container.

Run this script whenever processing code changes.

---

## upload_archive.sh

Uploads the historical dataset from `data/archive/` into HDFS.

Destination:

```text
/telepulse/archive
```

---

## bootstrap.sh

Initializes the TelePulse warehouse.

The script performs the following steps:

1. Reads historical datasets from HDFS
2. Validates source schemas
3. Applies data transformations
4. Creates Hive warehouse tables
5. Loads transformed data
6. Creates analytics views

---

## check.sh

Runs validation queries to verify that the warehouse was created successfully.

---

# Verifying the Warehouse

Open a Hive shell:

```bash
docker exec -it infrastructure-master-1 hive
```

```sql
USE telepulse;

SHOW TABLES;

SHOW VIEWS;
```

You should see the warehouse tables together with the analytics views created during the bootstrap process.

You can also verify that the historical archive exists in HDFS:

```bash
docker exec infrastructure-master-1 \
hdfs dfs -ls -R /telepulse
```

---

# Current Pipeline

```text
Historical CSV Files
        │
        ▼
upload_archive.sh
        │
        ▼
HDFS (/telepulse/archive)
        │
        ▼
Spark Bootstrap
        │
        ├── Read CSV files
        ├── Validate schema
        ├── Transform data
        ├── Create Hive tables
        ├── Load warehouse
        └── Create analytics views
                │
                ▼
        Hive Data Warehouse
```

---

# Current Status

✅ Dockerized Hadoop cluster

✅ HDFS storage

✅ Spark ETL pipeline

✅ Hive warehouse

✅ Analytics views

✅ Historical bootstrap pipeline

✅ Modular processing package

---

# Roadmap

The next development phase introduces incremental batch ingestion.

Planned additions include:

- Upload API
- Incoming data pipeline
- Schema validation for uploaded files
- Accepted / rejected file workflow
- Incremental Spark ingestion
- Analytics REST API
- Dashboard integration

---

# License

This project is intended for educational and portfolio purposes.