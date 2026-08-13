"""
Expected schemas for TelePulse source datasets.
"""

SMS_COLUMNS = [
    "datetime",
    "CellID",
    "countrycode",
    "smsin",
    "smsout",
    "callin",
    "callout",
    "internet",
]

PROVINCE_COLUMNS = [
    "datetime",
    "CellID",
    "provinceName",
    "cell2Province",
    "Province2cell",
]