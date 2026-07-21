# TelePulse

## Prerequisites
- Docker
- Docker Compose
- Python


## Dataset

The TelePulse project uses the Telecom Italia Big Data Challenge dataset.

    https://www.kaggle.com/datasets/marcodena/mobile-phone-activity

Download the dataset and extract all files into:

```
data/raw/
```

Your folder should look similar to:

```
data/
├── raw/
│   ├── ISTAT_census_variables_2011.csv
│   ├── sms-call-internet-mi-2013-11-01.csv
│   ├── ...
│   ├── mi-to-provinces-2013-11-01.csv
│   ├── ...
│
├── merged/
│   ├── Italian_provinces.geojson
│   └── milano-grid.geojson
```

> The merged CSV files are generated automatically by the bootstrap script.



## Setup

```bash
git clone https://github.com/Doha-Ahmed-E/TelePulse.git
cd TelePulse
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

The bootstrap script automatically:

- Creates a Python virtual environment
- Installs Python dependencies
- Builds all Docker images
- Starts the Hadoop/Spark/Hive cluster
- Merges the raw datasets
- Uploads the datasets to HDFS
- Executes the Spark analytics pipeline



## Opening the Hadoop container

```bash
docker exec -it infrastructure-master-1 bash
```

## Verifying the project

Inside the container:

```bash
hdfs dfs -ls /telepulse
```

```bash
hive
```

```sql
USE telepulse;
SHOW TABLES;
SHOW VIEWS;
```

Expected tables:

- urban_vitality
- land_use_classification
- spatial_diversity

Expected views:

- vw_dashboard
- vw_dashboard_map
- vw_activity_summary
- vw_activity_ranking
- vw_business_zones
- vw_residential_zones
- vw_cell_summary
- vw_high_diversity
- vw_internet_hotspots
- vw_sms_hotspots
- vw_call_hotspots
- vw_kpi_summary
- vw_land_use
- vw_spatial_diversity
- vw_urban_vitality

## Power BI Connection

Inside the container: 

```bash
start-thriftserver.sh
```

```bash
hiveserver2
```

### Verify Spark Thrift Server 
in another container terminal:

```bash
beeline -u jdbc:hive2://localhost:10000
```
Power BI settings:

Host: localhost
Port: 10000
Database: telepulse
Authentication: None

