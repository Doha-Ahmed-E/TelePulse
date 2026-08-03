USE telepulse;

SHOW TABLES;
SHOW VIEWS;

SELECT COUNT(*) AS sms_rows
FROM sms_call_internet;

SELECT COUNT(*) AS province_rows
FROM cell_provinces;

SELECT *
FROM sms_call_internet
LIMIT 5;

SELECT *
FROM cell_provinces
LIMIT 5;