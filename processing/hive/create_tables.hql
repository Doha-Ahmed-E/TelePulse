CREATE DATABASE IF NOT EXISTS telepulse;

USE telepulse;

CREATE TABLE IF NOT EXISTS sms_call_internet (
    datetime BIGINT,
    cellid INT,
    countrycode INT,
    smsin DOUBLE,
    smsout DOUBLE,
    callin DOUBLE,
    callout DOUBLE,
    internet DOUBLE
)
STORED AS PARQUET;

CREATE TABLE IF NOT EXISTS cell_provinces (
    datetime BIGINT,
    cellid INT,
    provincename STRING,
    cell2province DOUBLE,
    province2cell DOUBLE
)
STORED AS PARQUET;