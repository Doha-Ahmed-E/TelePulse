"""
TelePulse incremental ingestion pipeline.
"""

from pathlib import Path

INCOMING_DIR = Path("/data/uploads/incoming")


def main():

    files = sorted(INCOMING_DIR.glob("*.csv"))

    print(f"Found {len(files)} file(s).")

    for file in files:
        print(file.name)


if __name__ == "__main__":
    main()