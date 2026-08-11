"""
Shared constants used by TelePulse processing pipelines.
"""
# Data 

LOCAL_UPLOAD_ROOT = "data/uploads"

LOCAL_INCOMING_ROOT = f"{LOCAL_UPLOAD_ROOT}/incoming"
LOCAL_PROCESSED_ROOT = f"{LOCAL_UPLOAD_ROOT}/processed"
LOCAL_REJECTED_ROOT = f"{LOCAL_UPLOAD_ROOT}/rejected"

# Hive

DATABASE_NAME = "telepulse"

SMS_TABLE = "sms_call_internet"

PROVINCE_TABLE = "cell_provinces"


# HDFS

ARCHIVE_ROOT = "/telepulse/archive"

RAW_ROOT = "/telepulse/raw"
PROCESSED_ROOT = "/telepulse/processed"
REJECTED_ROOT = "/telepulse/rejected"

SMS_ARCHIVE_PATH = (
    f"{ARCHIVE_ROOT}/sms-call-internet-mi-2013-11-*.csv"
)

PROVINCE_ARCHIVE_PATH = (
    f"{ARCHIVE_ROOT}/mi-to-provinces-2013-11-*.csv"
)


# Spark

BOOTSTRAP_APP_NAME = "TelePulse Bootstrap"

INGESTION_APP_NAME = "TelePulse Ingestion"