from pathlib import Path
import subprocess
import time

INCOMING_DIR = Path("/home/jupyter/telepulse/data/uploads/incoming")
PROJECT_ROOT = Path("/home/jupyter/telepulse")
INGEST_SCRIPT = PROJECT_ROOT / "processing/ingestion/ingest.py"


def ingest_file(file_path: Path):
    print(f"[watcher] Ingesting: {file_path.name}")

    subprocess.run(
        [
            "spark-submit",
            "--master",
            "spark://master:7077",
            str(INGEST_SCRIPT),
            str(file_path),
        ],
        cwd=PROJECT_ROOT,
        env={
            **__import__("os").environ,
            "PYTHONPATH": str(PROJECT_ROOT),
        },
        check=True,
    )


def main():
    print(f"[watcher] Watching: {INCOMING_DIR}")

    seen = set()

    while True:
        for file_path in INCOMING_DIR.iterdir():

            # Ignore gitkeep and anything that isn't a CSV
            if not file_path.is_file() or file_path.name == ".gitkeep":
                continue

            if file_path.suffix.lower() != ".csv":
                continue

            if file_path in seen:
                continue

            seen.add(file_path)

            print(f"[watcher] New file detected: {file_path.name}")

            try:
                ingest_file(file_path)
                print(f"[watcher] Ingestion completed: {file_path.name}")

            except subprocess.CalledProcessError as e:
                print(
                    f"[watcher] Ingestion failed for {file_path.name}: {e}"
                )
                seen.discard(file_path)

        time.sleep(5)


if __name__ == "__main__":
    main()