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
