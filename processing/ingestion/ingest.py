"""
Incrementally ingest one uploaded TelePulse dataset.
"""

from pathlib import Path
import argparse
import subprocess

from processing.common.constants import (
    INGESTION_APP_NAME,
    RAW_ROOT,
    PROCESSED_ROOT,
    REJECTED_ROOT,
    LOCAL_PROCESSED_ROOT,
    LOCAL_REJECTED_ROOT,
    SMS_TABLE,
    PROVINCE_TABLE,
)

from processing.common.schema import (
    SMS_COLUMNS,
    PROVINCE_COLUMNS,
)

from processing.common.hive import append_table
from processing.common.transform import transform_dataframe
from processing.common.utils import create_spark_session, read_csv
from processing.common.validate import validate_dataframe


def resolve_dataset(file_path: Path) -> tuple[list[str], str, str]:
    """Resolve the schema, dataset label, and Hive table for an uploaded file."""

    filename = file_path.name

    if filename.startswith("sms-call-internet-"):
        return SMS_COLUMNS, "SMS", SMS_TABLE

    if filename.startswith("mi-to-provinces-"):
        return PROVINCE_COLUMNS, "Province", PROVINCE_TABLE

    raise ValueError(
        f"Unsupported TelePulse dataset: {filename}. "
        "Expected an SMS/call/internet or province dataset."
    )


def upload_to_hdfs(file_path: Path) -> str:
    """Upload the local file to the HDFS raw zone."""

    hdfs_path = f"{RAW_ROOT}/{file_path.name}"

    print(f"Uploading to HDFS: {file_path.name}")

    subprocess.run(
        [
            "hdfs",
            "dfs",
            "-put",
            "-f",
            str(file_path),
            hdfs_path,
        ],
        check=True,
    )

    print(f"Uploaded: {hdfs_path}")

    return hdfs_path


def build_hdfs_path(root: str, filename: str) -> str:
    """Build an absolute HDFS path for a file."""

    return f"{root}/{filename}"


def move_hdfs_file(source: str, destination: str) -> None:
    """Move a file within HDFS."""

    subprocess.run(
        [
            "hdfs",
            "dfs",
            "-mv",
            source,
            destination,
        ],
        check=True,
    )


def move_local_file(file_path: Path, directory: str) -> None:
    """Move a local file to the specified directory."""

    destination = Path(directory) / file_path.name

    subprocess.run(
        [
            "mv",
            str(file_path),
            str(destination),
        ],
        check=True,
    )


def ingest(file_path: Path) -> None:
    """Ingest one uploaded file into the TelePulse warehouse."""

    expected_columns, dataset_label, table_name = resolve_dataset(
        file_path
    )

    hdfs_raw_path = upload_to_hdfs(file_path)

    spark = create_spark_session(INGESTION_APP_NAME)

    try:
        print(
            f"Reading {dataset_label} dataset from HDFS: "
            f"{hdfs_raw_path}"
        )

        df = read_csv(
            spark,
            hdfs_raw_path,
        )

        validate_dataframe(
            df,
            expected_columns,
            dataset_label,
        )

        df = transform_dataframe(df)

        append_table(
            df,
            table_name,
        )

        # Hive append succeeded.
        # The file can now safely be marked as processed.
        processed_hdfs_path = build_hdfs_path(
            PROCESSED_ROOT,
            file_path.name,
        )

        move_hdfs_file(
            hdfs_raw_path,
            processed_hdfs_path,
        )

        move_local_file(
            file_path,
            LOCAL_PROCESSED_ROOT,
        )

        print(
            f"{dataset_label} ingestion completed successfully."
        )

    except Exception:
        print(
            f"{dataset_label} ingestion failed. "
            "Moving file to rejected."
        )

        rejected_hdfs_path = build_hdfs_path(
            REJECTED_ROOT,
            file_path.name,
        )

        try:
            move_hdfs_file(
                hdfs_raw_path,
                rejected_hdfs_path,
            )
        except Exception as move_error:
            print(
                "Failed to move HDFS file to rejected: "
                f"{move_error}"
            )

        try:
            move_local_file(
                file_path,
                LOCAL_REJECTED_ROOT,
            )
        except Exception as move_error:
            print(
                "Failed to move local file to rejected: "
                f"{move_error}"
            )

        raise

    finally:
        spark.stop()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)

    args = parser.parse_args()

    ingest(args.file)


if __name__ == "__main__":
    main()