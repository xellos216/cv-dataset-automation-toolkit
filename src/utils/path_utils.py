from pathlib import Path

BASE_OUTPUT_DIR = Path("outputs")

LOG_DIR = BASE_OUTPUT_DIR / "logs"
REPORT_DIR = BASE_OUTPUT_DIR / "reports"
METADATA_DIR = BASE_OUTPUT_DIR / "metadata"
STATS_DIR = BASE_OUTPUT_DIR / "stats"


def ensure_output_dirs() -> None:
    """
    Create all standard output directories if they do not exist.
    """
    for directory in [LOG_DIR, REPORT_DIR, METADATA_DIR, STATS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
