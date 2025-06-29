import os
from pathlib import Path

PROJECT_ROOT_PATH: Path = Path(__file__).resolve().parents[1]
SRC_PATH: Path = PROJECT_ROOT_PATH / "src"
TEMPLATES_PATH: Path = SRC_PATH / "api" / "templates"

PERSISTENCE_MOUNTING_POINT: Path = PROJECT_ROOT_PATH / "persistence"
os.makedirs(PERSISTENCE_MOUNTING_POINT, exist_ok=True)

DB_PATH: Path = PERSISTENCE_MOUNTING_POINT / "requests.db"
CONFIG_PATH: Path = PERSISTENCE_MOUNTING_POINT / "config.yaml"

DATA_FOLDER: Path = PERSISTENCE_MOUNTING_POINT / "data"
OUT_FOLDER: Path = PERSISTENCE_MOUNTING_POINT / "out"

# NUL for windows, /dev/null for linux
NULL_PATH: Path = Path("NUL") if os.name == "nt" else Path("/dev/null")
PASSLOG_PATH: Path = OUT_FOLDER / "ffmpeg2pass"

ARCHIVE_FORMAT: str = "zip"
