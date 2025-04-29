from pathlib import Path
import os

PROJECT_ROOT_PATH: Path = Path(__file__).resolve().parents[1]
SRC_PATH: Path = PROJECT_ROOT_PATH / "src"
TEMPLATES_PATH: Path = SRC_PATH / "api" / "templates"

DATA_FOLDER: Path = PROJECT_ROOT_PATH / "data"
OUT_FOLDER: Path = PROJECT_ROOT_PATH / "out"
# NUL for windows, /dev/null for linux
NULL_PATH: Path = Path("NUL") if os.name == "nt" else "/dev/null"
