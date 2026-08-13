from pathlib import Path

INCOMING_DIR = Path("/data/uploads/incoming")


def save_upload(file, filename: str) -> Path:
    """
    Save an uploaded file to the incoming directory.
    """
    INCOMING_DIR.mkdir(parents=True, exist_ok=True)

    destination = INCOMING_DIR / filename

    with destination.open("wb") as output:
        while chunk := file.file.read(1024 * 1024):
            output.write(chunk)

    return destination