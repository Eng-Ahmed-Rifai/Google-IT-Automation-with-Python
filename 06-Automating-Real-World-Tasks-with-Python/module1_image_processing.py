"""
Google IT Automation with Python - Course 6: Automating Real-World Tasks with Python
Module 1: Image Processing with Pillow (module1_image_processing.py)

Covers:
- Batch resizing of images to standardized dimensions (e.g., 128x128)
- Clockwise rotation (90 degrees / 270 degrees in counter-clockwise PIL coordinate space)
- Format conversion (TIFF, RGBA, PNG to standard JPEG / RGB)
- Directory scanning, error-tolerant batch execution, and output directory organization
"""

import os
import sys
from typing import List, Optional, Tuple
from PIL import Image


def process_single_image(
    input_path: str,
    output_path: str,
    target_size: Tuple[int, int] = (128, 128),
    rotate_clockwise_degrees: int = 90,
    target_format: str = "JPEG"
) -> bool:
    """
    Processes a single image:
    1. Opens the image.
    2. Converts color mode to RGB (handling RGBA, CMYK, P, etc. safely).
    3. Rotates by specified clockwise degrees (PIL rotates counter-clockwise, so clockwise 90 is -90 or 270).
    4. Resizes to target_size.
    5. Saves in target_format (e.g. JPEG).
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    try:
        with Image.open(input_path) as im:
            # 1. Convert to RGB mode if not already RGB (stripping alpha channel safely)
            if im.mode != "RGB":
                # If RGBA, create white background and paste to avoid black artifacts
                if im.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", im.size, (255, 255, 255))
                    alpha_channel = im.split()[-1]
                    background.paste(im, mask=alpha_channel)
                    im_rgb = background
                else:
                    im_rgb = im.convert("RGB")
            else:
                im_rgb = im.copy()

            # 2. Rotate clockwise
            # In PIL, positive degrees rotate counter-clockwise, so rotate clockwise = -degrees
            if rotate_clockwise_degrees % 360 != 0:
                pil_rotation = (-rotate_clockwise_degrees) % 360
                im_rotated = im_rgb.rotate(pil_rotation, expand=True)
            else:
                im_rotated = im_rgb

            # 3. Resize to target dimension
            im_resized = im_rotated.resize(target_size, Image.Resampling.LANCZOS)

            # Ensure parent output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            # 4. Save to target path
            im_resized.save(output_path, format=target_format)
            return True

    except Exception as exc:
        print(f"[ERROR] Failed to process image '{input_path}': {exc}", file=sys.stderr)
        return False


def batch_process_images(
    input_dir: str,
    output_dir: str,
    target_size: Tuple[int, int] = (128, 128),
    rotate_clockwise_degrees: int = 90,
    target_format: str = "JPEG",
    extension_filter: Optional[Tuple[str, ...]] = None
) -> List[str]:
    """
    Scans input_dir, filters valid image files, processes each, and saves to output_dir.
    Returns list of successfully processed output file paths.
    """
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    os.makedirs(output_dir, exist_ok=True)
    processed_files: List[str] = []

    for filename in sorted(os.listdir(input_dir)):
        input_file = os.path.join(input_dir, filename)

        # Ignore subdirectories or hidden files (e.g. .DS_Store, .git)
        if not os.path.isfile(input_file) or filename.startswith("."):
            continue

        if extension_filter:
            if not filename.lower().endswith(extension_filter):
                continue

        # In Coursera Lab 1, output filename strips old extension or appends .jpeg
        base_name, _ = os.path.splitext(filename)
        output_ext = f".{target_format.lower()}" if target_format.lower() != "jpeg" else ".jpg"
        output_file = os.path.join(output_dir, f"{base_name}{output_ext}")

        success = process_single_image(
            input_path=input_file,
            output_path=output_file,
            target_size=target_size,
            rotate_clockwise_degrees=rotate_clockwise_degrees,
            target_format=target_format
        )
        if success:
            processed_files.append(output_file)

    return processed_files


def test_module1() -> None:
    """
    Validation assertion test suite for Module 1.
    """
    import tempfile

    with tempfile.TemporaryDirectory() as tmp_dir:
        input_folder = os.path.join(tmp_dir, "input_images")
        output_folder = os.path.join(tmp_dir, "output_images")
        os.makedirs(input_folder, exist_ok=True)

        # Create sample test images:
        # Image 1: RGBA 200x100
        img1_path = os.path.join(input_folder, "test1_rgba.png")
        img1 = Image.new("RGBA", (200, 100), (255, 0, 0, 128))
        img1.save(img1_path)

        # Image 2: Grayscale 300x300
        img2_path = os.path.join(input_folder, "test2_gray.tiff")
        img2 = Image.new("L", (300, 300), 120)
        img2.save(img2_path)

        # Batch process
        processed = batch_process_images(
            input_dir=input_folder,
            output_dir=output_folder,
            target_size=(128, 128),
            rotate_clockwise_degrees=90,
            target_format="JPEG"
        )

        assert len(processed) == 2, f"Expected 2 processed images, got {len(processed)}"

        # Validate output attributes
        for out_path in processed:
            assert os.path.exists(out_path)
            with Image.open(out_path) as out_im:
                assert out_im.format == "JPEG"
                assert out_im.mode == "RGB"
                assert out_im.size == (128, 128)

        print("[PASS] Module 1 (Image Processing): All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module1()
