## Power BI Connection

Prerequisites:
- Docker Desktop
- Hive ODBC Driver installed

Start the cluster:

docker compose up -d

Verify Spark Thrift Server:

beeline -u jdbc:hive2://localhost:10000

Power BI settings:

Host: localhost
Port: 10000
Database: telepulse
Authentication: None