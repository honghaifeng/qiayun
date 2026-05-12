#!/usr/bin/env python3
"""Extract product images from PDF brochures"""
import fitz  # PyMuPDF
import os

output_dir = "/Users/honghaifeng/Desktop/haifeng/2026/98/20260331/qiayun/website/images"
os.makedirs(output_dir, exist_ok=True)

pdfs = [
    "/Users/honghaifeng/Desktop/haifeng/2026/98/20260331/qiayun/宜兴休元.pdf",
    "/Users/honghaifeng/Desktop/haifeng/2026/98/20260331/qiayun/恰云电力服务图册.pdf",
]

for pdf_path in pdfs:
    doc = fitz.open(pdf_path)
    pdf_name = os.path.basename(pdf_path).replace(".pdf", "")
    print(f"\n=== {pdf_name} ({len(doc)} pages) ===")

    img_count = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)
        print(f"  Page {page_num+1}: {len(images)} images")

        for img_idx, img_info in enumerate(images):
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            if base_image:
                img_bytes = base_image["image"]
                ext = base_image["ext"]
                w = base_image["width"]
                h = base_image["height"]

                # Skip tiny images (icons, decorations)
                if w < 100 or h < 100:
                    continue

                img_count += 1
                filename = f"{pdf_name}_p{page_num+1}_{img_idx}.{ext}"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(img_bytes)
                print(f"    -> {filename} ({w}x{h}, {len(img_bytes)//1024}KB)")

    print(f"  Total extracted: {img_count} images")
    doc.close()

print(f"\nAll images saved to: {output_dir}")
