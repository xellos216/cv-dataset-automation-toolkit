import hashlib
import shutil
from pathlib import Path
from typing import List, Tuple

ALLOWED_IMAGE_EXTENSIONS: Tuple[str, ...] = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tiff",
    ".tif",
    ".webp",
)


def collect_files(input_dir: str, recursive: bool = False) -> List[Path]:
    """
    Collect files from the input directory.

    Args:
        input_dir: Directory path to scan.
        recursive: Whether to scan recursively.

    Returns:
        List of file paths.
    """
    root = Path(input_dir)

    if not root.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    if not root.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_dir}")

    pattern = "**/*" if recursive else "*"
    return [path for path in root.glob(pattern) if path.is_file()]


def is_allowed_image_file(file_path: Path) -> bool:
    """
    Check whether the file has an allowed image extension.
    """
    return file_path.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS


def compute_file_hash(file_path: Path, chunk_size: int = 8192) -> str:
    """
    Compute SHA256 hash for a file.
    """
    sha256 = hashlib.sha256()

    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def ensure_directory(path: Path) -> None:
    """
    Create directory if it does not exist.
    """
    path.mkdir(parents=True, exist_ok=True)


def move_file_to_directory(file_path: Path, target_dir: Path) -> Path:
    """
    Move a file into a target directory.
    If the filename already exists, append a numeric suffix.
    """
    ensure_directory(target_dir)

    destination = target_dir / file_path.name
    counter = 1

    while destination.exists():
        destination = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
        counter += 1

    shutil.move(str(file_path), str(destination))
    return destination
