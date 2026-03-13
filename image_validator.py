import argparse
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from utils.file_utils import collect_files, is_allowed_image_file
from utils.image_utils import validate_image
from utils.logging_utils import setup_logger
from utils.path_utils import LOG_DIR, REPORT_DIR, ensure_output_dirs


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate image files in a dataset directory."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input image directory.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan directories recursively.",
    )
    parser.add_argument(
        "--min-width",
        type=int,
        default=1,
        help="Minimum allowed image width.",
    )
    parser.add_argument(
        "--min-height",
        type=int,
        default=1,
        help="Minimum allowed image height.",
    )
    parser.add_argument(
        "--report",
        default=str(REPORT_DIR / "validation_report.csv"),
        help="Path to save the CSV validation report.",
    )
    parser.add_argument(
        "--log-file",
        default=str(LOG_DIR / "validation.log"),
        help="Path to save the log file.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    ensure_output_dirs()

    report_path = Path(args.report)
    log_file_path = Path(args.log_file)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    logger = setup_logger(log_file=str(log_file_path))

    logger.info("Starting image validation")
    logger.info(f"Input directory: {args.input}")
    logger.info(f"Recursive scan: {args.recursive}")
    logger.info(f"Minimum resolution: {args.min_width}x{args.min_height}")

    try:
        files = collect_files(args.input, recursive=args.recursive)
    except Exception as exc:
        logger.error(str(exc))
        return

    logger.info(f"Total files found: {len(files)}")

    results = []

    for file_path in tqdm(files, desc="Validating files"):
        if not is_allowed_image_file(file_path):
            results.append(
                {
                    "file_path": str(file_path),
                    "file_name": file_path.name,
                    "is_valid": False,
                    "error_reason": "Unsupported file extension",
                    "width": None,
                    "height": None,
                    "channels": None,
                }
            )
            continue

        validation_result = validate_image(
            file_path=file_path,
            min_width=args.min_width,
            min_height=args.min_height,
        )
        results.append(validation_result)

    df = pd.DataFrame(results)
    df.to_csv(report_path, index=False)

    valid_count = int(df["is_valid"].sum()) if not df.empty else 0
    invalid_count = len(df) - valid_count
    corrupted_count = (
        int((df["error_reason"] == "Unreadable or corrupted image").sum())
        if not df.empty
        else 0
    )
    low_resolution_count = (
        int(
            df["error_reason"]
            .fillna("")
            .str.contains("Resolution below threshold")
            .sum()
        )
        if not df.empty
        else 0
    )
    unsupported_count = (
        int((df["error_reason"] == "Unsupported file extension").sum())
        if not df.empty
        else 0
    )

    logger.info("Validation complete")
    logger.info(f"Valid images: {valid_count}")
    logger.info(f"Invalid files: {invalid_count}")
    logger.info(f"Corrupted images: {corrupted_count}")
    logger.info(f"Low resolution images: {low_resolution_count}")
    logger.info(f"Unsupported files: {unsupported_count}")
    logger.info(f"Report saved to: {report_path.resolve()}")

    print("\n=== Validation Summary ===")
    print(f"Total scanned files   : {len(files)}")
    print(f"Valid images          : {valid_count}")
    print(f"Invalid files         : {invalid_count}")
    print(f"Corrupted images      : {corrupted_count}")
    print(f"Low resolution images : {low_resolution_count}")
    print(f"Unsupported files     : {unsupported_count}")
    print(f"CSV report            : {report_path}")
    print(f"Log file              : {log_file_path}")


if __name__ == "__main__":
    main()
