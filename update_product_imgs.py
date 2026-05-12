#!/usr/bin/env python3
"""Update product detail pages to use real images instead of SVG"""
import re, os

products_dir = "/Users/honghaifeng/Desktop/haifeng/2026/98/20260331/qiayun/website/products"

files_images = {
    "kyn28a-12.html": ("kyn28a-12.jpg", "KYN28A-12 MV Switchgear"),
    "ybm-12.html": ("ybm-12.jpg", "YBM-12 Prefab Substation"),
    "hxgn-12.html": ("hxgn-12.jpg", "HXGN-12 Ring Main Unit"),
    "gck.html": ("gck.jpg", "GCK LV Switchgear"),
    "svc.html": ("svc.jpg", "SVC Reactive Power Compensation"),
    "xgl.html": ("xgl.jpg", "XGL LV Power Cabinet"),
    "jxf.html": ("jxf.jpg", "JXF Distribution Box"),
}

for filename, (img, alt) in files_images.items():
    filepath = os.path.join(products_dir, filename)
    if not os.path.exists(filepath):
        print(f"Skip: {filename}")
        continue
    with open(filepath, 'r') as f:
        content = f.read()
    # Replace SVG in product-hero-img with img tag
    content = re.sub(
        r'<div class="product-hero-img">.*?</div>',
        f'<div class="product-hero-img"><img src="../images/{img}" alt="{alt}" style="max-width:100%;max-height:100%;border-radius:12px;object-fit:cover;"></div>',
        content,
        flags=re.DOTALL
    )
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated: {filename}")

print("Done!")
