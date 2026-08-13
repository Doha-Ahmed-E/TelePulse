# TelePulse

A production-inspired batch data engineering platform built with **Hadoop, Spark, Hive, Docker, and FastAPI** for processing large-scale mobile network activity data.

## Architecture

```text
Historical CSVs
      │
      ▼
     HDFS
      │
      ▼
   Spark ETL
      │
      ├── Validate
      ├── Transform
      └── Load
            │
            ▼
     Hive Warehouse
            │
            ▼
      Analytics Views
            │
            ▼
       FastAPI API
            │
            ▼
        Frontend
````

## Tech Stack

* Python
* Docker / Docker Compose
* Hadoop HDFS
* YARN
* Apache Spark
* Apache Hive
* FastAPI
* JavaScript / HTML / CSS

## Project Structure

```text
TelePulse/
├── api/
├── data/
│   ├── archive/
│   └── uploads/
│       ├── incoming/
│       ├── processed/
│       └── rejected/
├── docs/
├── infrastructure/
├── processing/
│   ├── bootstrap/
│   ├── common/
│   ├── hive/
│   └── ingestion/
├── scripts/
├── frontend/
├── Makefile
└── README.md
```

## Getting Started

```bash
cd TelePulse

make base      # One-time Docker base image build
make up        # Start the Hadoop/Spark/Hive cluster

./scripts/bootstrap.sh
```

The bootstrap process loads the historical dataset into the Hive warehouse.

### Incremental Ingestion

Uploaded files are placed in:

```text
data/uploads/incoming/
```

They can be processed with:

```bash
./scripts/run_ingestion.sh <filename>
```

Successfully processed files are moved to:

```text
data/uploads/processed/
```

Failed files are moved to:

```text
data/uploads/rejected/
```

The project also includes an upload API and a frontend upload interface for submitting new datasets.

## Dataset

TelePulse uses the **Telecom Italia Big Data Challenge** dataset:

[https://www.kaggle.com/datasets/marcodena/mobile-phone-activity](https://www.kaggle.com/datasets/marcodena/mobile-phone-activity)

Place the historical files under:

```text
data/archive/
```

## HDFS Safe Mode

On the first startup, Hadoop may temporarily keep the NameNode in safe mode while DataNodes register.

If ingestion fails with:

```text
Name node is in safe mode
```

wait a few seconds and retry.

Check the current state with:

```bash
docker compose -f deployment/docker-compose.yml exec master \
hdfs dfsadmin -safemode get
```

If necessary:

```bash
docker compose -f deployment/docker-compose.yml exec master \
hdfs dfs -chmod 1777 /tmp
```

## Current Status

*  Dockerized Hadoop/Spark/Hive cluster
*  HDFS data lake
*  Spark ETL pipeline
*  Hive warehouse and analytics views
*  Historical bootstrap
*  Incremental ingestion
*  Schema validation and transformation
*  Processed/rejected file workflow
*  Upload API
*  Analytics API
*  Frontend dashboard

## Roadmap

* Improve analytics query performance
* Complete the dashboard
* Improve ingestion monitoring and error handling
* Further refine the production-style batch architecture

## License

Educational and portfolio project.