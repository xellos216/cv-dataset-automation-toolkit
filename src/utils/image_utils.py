from pathlib import Path
from typing import Any, Dict

import cv2


def validate_image(
    file_path: Path, min_width: int = 1, min_height: int = 1
) -> Dict[str, Any]:
    """
    Validate an image file using OpenCV.

    Returns:
        A dictionary containing validation results and metadata.
    """
    result = {
        "file_path": str(file_path),
        "file_name": file_path.name,
        "is_valid": False,
        "error_reason": "",
        "width": None,
        "height": None,
        "channels": None,
    }

    try:
        image = cv2.imread(str(file_path), cv2.IMREAD_UNCHANGED)

        if image is None:
            result["error_reason"] = "Unreadable or corrupted image"
            return result

        height, width = image.shape[:2]
        channels = 1 if len(image.shape) == 2 else image.shape[2]

        result["width"] = int(width)
        result["height"] = int(height)
        result["channels"] = int(channels)

        if width < min_width or height < min_height:
            result["error_reason"] = (
                f"Resolution below threshold ({width}x{height} < {min_width}x{min_height})"
            )
            return result

        result["is_valid"] = True
        return result

    except Exception as exc:
        result["error_reason"] = f"Exception during validation: {exc}"
        return result


def extract_image_metadata(file_path: Path) -> Dict[str, Any]:
    """
    Extract image metadata using OpenCV.

    Returns:
        A dictionary containing metadata for a single image.
    """
    result = {
        "file_path": str(file_path),
        "file_name": file_path.name,
        "extension": file_path.suffix.lower(),
        "width": None,
        "height": None,
        "channels": None,
        "color_mode": None,
        "file_size_bytes": None,
        "aspect_ratio": None,
        "is_readable": False,
        "error_reason": "",
    }

    try:
        image = cv2.imread(str(file_path), cv2.IMREAD_UNCHANGED)

        if image is None:
            result["error_reason"] = "Unreadable or corrupted image"
            return result

        height, width = image.shape[:2]
        channels = 1 if len(image.shape) == 2 else image.shape[2]

        if channels == 1:
            color_mode = "grayscale"
        elif channels == 3:
            color_mode = "rgb_or_bgr"
        elif channels == 4:
            color_mode = "rgba_or_bgra"
        else:
            color_mode = f"{channels}_channels"

        aspect_ratio = round(width / height, 4) if height else None
        file_size_bytes = file_path.stat().st_size

        result.update(
            {
                "width": int(width),
                "height": int(height),
                "channels": int(channels),
                "color_mode": color_mode,
                "file_size_bytes": int(file_size_bytes),
                "aspect_ratio": aspect_ratio,
                "is_readable": True,
            }
        )
        return result

    except Exception as exc:
        result["error_reason"] = f"Exception during metadata extraction: {exc}"
        return result
