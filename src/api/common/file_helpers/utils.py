from pathlib import Path


def get_adjusted_save_path(save_path: Path, filename: str) -> Path:
    file_suffix: str = Path(filename).suffix
    return save_path.with_suffix(file_suffix) if file_suffix else save_path
