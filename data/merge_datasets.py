from pathlib import Path
import pandas as pd
import glob

ROOT = Path(__file__).resolve().parent.parent

RAW = ROOT / "data" / "raw"
MERGED = ROOT / "data" / "merged"
MERGED.mkdir(parents=True, exist_ok=True)


# Merge SMS files
sms_files = sorted(glob.glob(str(RAW / "sms-call-internet-mi-2013-11-*.csv")))

print("SMS files found:")
for f in sms_files:
    print(Path(f).name)

sms_df = pd.concat([pd.read_csv(f) for f in sms_files], ignore_index=True)
sms_df.to_csv(MERGED / "sms_call_internet_all.csv", index=False)

print(f"SMS merged successfully! Rows: {len(sms_df)}")


# Merge Province files
province_files = sorted(glob.glob(str(RAW / "mi-to-provinces-2013-11-*.csv")))

print("\nProvince files found:")
for f in province_files:
    print(Path(f).name)

province_df = pd.concat([pd.read_csv(f) for f in province_files], ignore_index=True)
province_df.to_csv(MERGED / "mi_to_provinces_all.csv", index=False)

print(f"Province merged successfully! Rows: {len(province_df)}")