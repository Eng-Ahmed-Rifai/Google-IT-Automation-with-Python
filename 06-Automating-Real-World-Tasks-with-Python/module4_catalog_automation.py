"""
Google IT Automation with Python - Course 6: Automating Real-World Tasks with Python
Module 4: Catalog Automation & Supplier Pipeline (module4_catalog_automation.py)

Covers:
- Processing supplier catalog images (600x400, RGB, JPEG format)
- Parsing fruit/product descriptions from plain text to normalized JSON
- Converting weight strings (e.g. '500 lbs') to integer values
- Associating corresponding image filenames with product entries
- Interacting with catalog web servers (REST endpoints & multipart/form-data upload)
- Full orchestration pipeline execution with reporting
"""

import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image
import requests


def process_catalog_image(
    input_path: str,
    output_path: str,
    target_size: Tuple[int, int] = (600, 400)
) -> bool:
    """
    Processes a supplier image:
    Converts to RGB, resizes to target_size (600x400), and saves as JPEG.
    """
    try:
        with Image.open(input_path) as im:
            if im.mode != "RGB":
                im_rgb = im.convert("RGB")
            else:
                im_rgb = im.copy()

            im_resized = im_rgb.resize(target_size, Image.Resampling.LANCZOS)

            out_dir = os.path.dirname(output_path)
            if out_dir and not os.path.exists(out_dir):
                os.makedirs(out_dir, exist_ok=True)

            im_resized.save(output_path, "JPEG")
            return True
    except Exception as exc:
        print(f"[ERROR] Failed to process image '{input_path}': {exc}", file=sys.stderr)
        return False


def batch_process_catalog_images(
    images_dir: str,
    output_dir: str,
    target_size: Tuple[int, int] = (600, 400)
) -> List[str]:
    """
    Processes all non-hidden image files in images_dir, saving them as .jpeg in output_dir.
    """
    if not os.path.exists(images_dir):
        raise FileNotFoundError(f"Directory not found: {images_dir}")

    os.makedirs(output_dir, exist_ok=True)
    processed: List[str] = []

    for filename in sorted(os.listdir(images_dir)):
        if filename.startswith(".") or not os.path.isfile(os.path.join(images_dir, filename)):
            continue

        base_name, ext = os.path.splitext(filename)
        # Skip if already a .jpeg in the source directory unless different output dir
        input_file = os.path.join(images_dir, filename)
        output_file = os.path.join(output_dir, f"{base_name}.jpeg")

        if process_catalog_image(input_file, output_file, target_size):
            processed.append(output_file)

    return processed


def parse_catalog_description(
    file_path: str,
    image_extension: str = ".jpeg"
) -> Dict[str, Any]:
    """
    Parses a single product description text file:
    - Line 1: Fruit Name
    - Line 2: Weight (e.g. '500 lbs') -> converted to integer (500)
    - Line 3+: Description paragraph
    Associates image_name based on filename stem + image_extension.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Description file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        lines = [line.strip() for line in f.readlines()]

    if len(lines) < 3:
        raise ValueError(
            f"Invalid description format in '{file_path}': expected at least 3 lines, got {len(lines)}"
        )

    name = lines[0]

    # Extract integer weight from line 2 (e.g. '500 lbs' -> 500)
    weight_match = re.search(r"(\d+)", lines[1])
    if not weight_match:
        raise ValueError(f"Could not parse numeric weight from '{lines[1]}' in '{file_path}'")
    weight = int(weight_match.group(1))

    description = " ".join([l for l in lines[2:] if l])

    base_stem, _ = os.path.splitext(os.path.basename(file_path))
    image_name = f"{base_stem}{image_extension}"

    return {
        "name": name,
        "weight": weight,
        "description": description,
        "image_name": image_name
    }


def parse_all_catalog_descriptions(descriptions_dir: str) -> List[Dict[str, Any]]:
    """
    Parses all .txt description files in the directory.
    """
    if not os.path.exists(descriptions_dir):
        raise FileNotFoundError(f"Descriptions directory not found: {descriptions_dir}")

    items: List[Dict[str, Any]] = []
    for filename in sorted(os.listdir(descriptions_dir)):
        if filename.endswith(".txt") and not filename.startswith("."):
            full_path = os.path.join(descriptions_dir, filename)
            try:
                item = parse_catalog_description(full_path)
                items.append(item)
            except Exception as exc:
                print(f"[WARNING] Skipping '{filename}': {exc}", file=sys.stderr)

    return items


def upload_catalog_item(
    url: str,
    item_dict: Dict[str, Any],
    session: Optional[requests.Session] = None
) -> Tuple[bool, int, str]:
    """
    Posts catalog item dictionary as JSON to fruits endpoint.
    """
    requester = session or requests
    try:
        response = requester.post(url, json=item_dict, timeout=5.0)
        return (response.status_code in (200, 201)), response.status_code, response.text
    except Exception as exc:
        return False, 0, str(exc)


def upload_catalog_image(
    url: str,
    image_path: str,
    session: Optional[requests.Session] = None
) -> Tuple[bool, int, str]:
    """
    Uploads an image file to the image upload endpoint via multipart/form-data.
    """
    requester = session or requests
    if not os.path.exists(image_path):
        return False, 0, f"File not found: {image_path}"

    try:
        with open(image_path, "rb") as img_file:
            response = requester.post(url, files={"file": img_file}, timeout=10.0)
            return (response.status_code in (200, 201)), response.status_code, response.text
    except Exception as exc:
        return False, 0, str(exc)


def generate_catalog_summary(descriptions: List[Dict[str, Any]]) -> str:
    """
    Generates formatted summary text used in PDF reports:
    name: Apple<br/>weight: 500 lbs<br/><br/>
    """
    paragraphs = []
    for item in descriptions:
        paragraphs.append(f"name: {item['name']}<br/>weight: {item['weight']} lbs")
    return "<br/><br/>".join(paragraphs)


def test_module4() -> None:
    """
    Validation assertion test suite for Module 4.
    """
    import tempfile
    from unittest.mock import MagicMock, patch

    with tempfile.TemporaryDirectory() as tmp_dir:
        img_in = os.path.join(tmp_dir, "001.tiff")
        img_out = os.path.join(tmp_dir, "001.jpeg")

        # Create dummy source image
        im = Image.new("RGBA", (800, 600), (0, 255, 0, 255))
        im.save(img_in, "TIFF")

        # Test image processing
        ok = process_catalog_image(img_in, img_out, target_size=(600, 400))
        assert ok is True
        assert os.path.exists(img_out)
        with Image.open(img_out) as verified_im:
            assert verified_im.size == (600, 400)
            assert verified_im.format == "JPEG"

        # Create description text file
        desc_file = os.path.join(tmp_dir, "001.txt")
        with open(desc_file, "w", encoding="utf-8") as f:
            f.write("Apple\n")
            f.write("500 lbs\n")
            f.write("Crisp and delicious red apples freshly harvested.\n")

        # Test description parsing
        item = parse_catalog_description(desc_file)
        assert item["name"] == "Apple"
        assert item["weight"] == 500
        assert isinstance(item["weight"], int)
        assert item["image_name"] == "001.jpeg"
        assert "Crisp and delicious" in item["description"]

        # Test summary generation
        summary = generate_catalog_summary([item])
        assert "name: Apple" in summary
        assert "weight: 500 lbs" in summary

        # Test upload mocks
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.text = '{"status": "success"}'

        with patch("requests.post", return_value=mock_resp):
            up_ok, code, _ = upload_catalog_item("http://localhost/fruits", item)
            assert up_ok is True
            assert code == 201

            up_img_ok, img_code, _ = upload_catalog_image("http://localhost/upload", img_out)
            assert up_img_ok is True
            assert img_code == 201

    print("[PASS] Module 4 (Catalog Automation): All assertions passed with 100.00% precision.")


if __name__ == "__main__":
    test_module4()
