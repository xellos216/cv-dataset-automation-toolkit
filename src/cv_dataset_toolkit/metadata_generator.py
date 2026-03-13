import argparse
import json
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from utils.file_utils import collect_files, is_allowed_image_file
from utils.image_utils import extract_image_metadata
from utils.logging_utils import setup_logger
from utils.path_utils import LOG_DIR, METADATA_DIR, ensure_output_dirs


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate image metadata for a computer vision dataset."
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
        "--output-csv",
        default=str(METADATA_DIR / "metadata.csv"),
        help="Path to save metadata CSV.",
    )
    parser.add_argument(
        "--output-json",
        default=None,
        help="Optional path to save metadata JSON.",
    )
    parser.add_argument(
        "--include-invalid",
        action="store_true",
        help="Include unreadable/invalid images in the output metadata.",
    )
    parser.add_argument(
        "--log-file",
        default=str(LOG_DIR / "metadata_generator.log"),
        help="Path to save the log file.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    ensure_output_dirs()

    output_csv_path = Path(args.output_csv)
    output_json_path = Path(args.output_json) if args.output_json else None
    log_file_path = Path(args.log_file)

    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    if output_json_path:
        output_json_path.parent.mkdir(parents=True, exist_ok=True)

    logger = setup_logger(name="metadata_generator", log_file=str(log_file_path))

    logger.info("Starting metadata generation")
    logger.info(f"Input directory: {args.input}")
    logger.info(f"Recursive scan: {args.recursive}")
    logger.info(f"Output CSV: {output_csv_path}")
    logger.info(f"Output JSON: {output_json_path}")

    try:
        files = collect_files(args.input, recursive=args.recursive)
    except Exception as exc:
        logger.error(str(exc))
        return

    image_files = [file_path for file_path in files if is_allowed_image_file(file_path)]
    logger.info(f"Total files found: {len(files)}")
    logger.info(f"Image files selected: {len(image_files)}")

    metadata_rows = []

    for file_path in tqdm(image_files, desc="Extracting metadata"):
        metadata = extract_image_metadata(file_path)

        if metadata["is_readable"]:
            metadata_rows.append(metadata)
            continue

        if args.include_invalid:
            metadata_rows.append(metadata)
        else:
            logger.warning(
                f"Skipping unreadable image: {file_path} | reason={metadata['error_reason']}"
            )

    df = pd.DataFrame(metadata_rows)

    if not df.empty:
        df = df.sort_values(by=["file_name"]).reset_index(drop=True)

    df.to_csv(output_csv_path, index=False)
    logger.info(f"Metadata CSV saved to: {output_csv_path.resolve()}")

    if output_json_path:
        records = df.to_dict(orient="records")
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        logger.info(f"Metadata JSON saved to: {output_json_path.resolve()}")

    readable_count = (
        int(df["is_readable"].sum())
        if not df.empty and "is_readable" in df.columns
        else 0
    )
    unreadable_count = len(df) - readable_count if not df.empty else 0

    print("\n=== Metadata Generator Summary ===")
    print(f"Total scanned files    : {len(files)}")
    print(f"Image files selected   : {len(image_files)}")
    print(f"Metadata rows written  : {len(df)}")
    print(f"Readable images        : {readable_count}")
    print(f"Unreadable images      : {unreadable_count}")
    print(f"CSV output             : {output_csv_path}")
    print(
        f"JSON output            : {output_json_path if output_json_path else 'Not requested'}"
    )
    print(f"Log file               : {log_file_path}")


if __name__ == "__main__":
    main()
