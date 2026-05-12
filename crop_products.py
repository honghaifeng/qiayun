#!/usr/bin/env python3
"""Crop product photos from full-page PDF images"""
from PIL import Image
import os

src_dir = "/Users/honghaifeng/Desktop/haifeng/2026/98/20260331/qiayun/website/images"
out_dir = src_dir

# Mapping: product -> source image and crop region (left, top, right, bottom) in ratio of full image
# Full image is 2482x3510
W, H = 2482, 3510

products = [
    # KYN28A-12: p2, product photo is bottom half
    ("kyn28a-12.jpg", "宜兴休元_p2_0.jpeg", (0, 0.42, 1.0, 1.0)),
    # YBM-12: p3, product photo is bottom half
    ("ybm-12.jpg", "宜兴休元_p3_0.jpeg", (0, 0.45, 1.0, 1.0)),
    # HXGN-12: p4, product photos bottom half
    ("hxgn-12.jpg", "宜兴休元_p4_0.jpeg", (0, 0.42, 1.0, 1.0)),
    # GCK: p5, product photo bottom half
    ("gck.jpg", "宜兴休元_p5_0.jpeg", (0, 0.42, 1.0, 1.0)),
    # SVC: p6, product photo in bottom portion
    ("svc.jpg", "宜兴休元_p6_0.jpeg", (0, 0.45, 1.0, 0.95)),
    # XGL: p7, product photo bottom half
    ("xgl.jpg", "宜兴休元_p7_0.jpeg", (0, 0.45, 1.0, 1.0)),
    # JXF: p8, product photo bottom half
    ("jxf.jpg", "宜兴休元_p8_0.jpeg", (0, 0.42, 1.0, 1.0)),
]

for out_name, src_name, crop_ratio in products:
    src_path = os.path.join(src_dir, src_name)
    img = Image.open(src_path)
    w, h = img.size

    left = int(w * crop_ratio[0])
    top = int(h * crop_ratio[1])
    right = int(w * crop_ratio[2])
    bottom = int(h * crop_ratio[3])

    cropped = img.crop((left, top, right, bottom))

    # Resize to reasonable web size (max 800px wide)
    max_w = 800
    if cropped.width > max_w:
        ratio = max_w / cropped.width
        new_h = int(cropped.height * ratio)
        cropped = cropped.resize((max_w, new_h), Image.LANCZOS)

    out_path = os.path.join(out_dir, out_name)
    cropped.save(out_path, "JPEG", quality=85)
    print(f"{out_name}: {cropped.size[0]}x{cropped.size[1]}")

print("\nDone! Product images cropped.")
