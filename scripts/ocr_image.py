#!/usr/bin/env python3
"""
OCR image to text using PaddleOCR.

Designed for long-form Chinese investment research images (e.g., 洪灏's reports).
Automatically splits tall images into overlapping slices to avoid PaddleOCR's
max_side_limit, then merges results in reading order.

Usage:
    python scripts/ocr_image.py investment/洪灏/史诗级TACO.jpg
    python scripts/ocr_image.py investment/洪灏/利好.jpg -o /tmp/result.md

Naming convention:
    By default, output is saved as <image_name>_OCR.md in the same directory.
    e.g., 史诗级TACO.jpg → 史诗级TACO_OCR.md

Requirements:
    ~/ocr-env virtualenv with Python 3.12 (via pyenv) + paddlepaddle + paddleocr
"""

import argparse
import os
import sys
from pathlib import Path

# Suppress noisy PaddlePaddle logs
os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")
os.environ.setdefault("GLOG_minloglevel", "2")

MAX_HEIGHT = 3000  # PaddleOCR struggles above ~4000px; use 3000 for safety
OVERLAP = 200      # Overlap between slices to avoid cutting text lines


def split_image(img, max_h=MAX_HEIGHT, overlap=OVERLAP):
    """Split a tall image into overlapping horizontal slices."""
    from PIL import Image
    h = img.height
    if h <= max_h:
        return [img]

    slices = []
    y = 0
    while y < h:
        y_end = min(y + max_h, h)
        slices.append(img.crop((0, y, img.width, y_end)))
        if y_end == h:
            break
        y = y_end - overlap
    return slices


def ocr_image(image_path: Path) -> str:
    """Run PaddleOCR on an image (with auto-slicing for tall images)."""
    from PIL import Image
    from paddleocr import PaddleOCR

    ocr = PaddleOCR(lang="ch")
    img = Image.open(image_path)

    slices = split_image(img)
    if len(slices) > 1:
        print(f"Image {img.width}x{img.height} → split into {len(slices)} slices")

    all_lines = []
    for i, s in enumerate(slices):
        # Save slice to temp file (PaddleOCR needs a file path or numpy array)
        import numpy as np
        img_array = np.array(s)
        result = ocr.ocr(img_array)
        if not result or not result[0]:
            continue
        for word_info in result[0]:
            all_lines.append(word_info[1][0])

    return "\n".join(all_lines)


def main():
    parser = argparse.ArgumentParser(description="OCR image to Markdown text")
    parser.add_argument("image", type=Path, help="Path to the image file")
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="Output file path (default: <image>_OCR.md)")
    args = parser.parse_args()

    if not args.image.exists():
        print(f"Error: {args.image} not found", file=sys.stderr)
        sys.exit(1)

    output_path = args.output
    if output_path is None:
        output_path = args.image.with_name(args.image.stem + "_OCR.md")

    print(f"OCR: {args.image}")
    text = ocr_image(args.image)

    output_path.write_text(text, encoding="utf-8")
    print(f"Saved: {output_path} ({len(text)} chars)")


if __name__ == "__main__":
    main()
