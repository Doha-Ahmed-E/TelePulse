from pyhive import hive

HIVE_HOST = "master"
HIVE_PORT = 10000
HIVE_DATABASE = "telepulse"
HIVE_USERNAME = "jupyter"


def get_hive_connection():
    return hive.Connection(
        host=HIVE_HOST,
        port=HIVE_PORT,
        database=HIVE_DATABASE,
        username=HIVE_USERNAME,
    )