import os
import sys
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

PDF_DIR = os.path.join(os.path.dirname(__file__), "pdfs")
IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMG_DIR, exist_ok=True)

# 檢查特定含圖題目所在的頁碼與圖片 bbox
TARGET_IMG_QUESTIONS = [
    ("114", 55),
    ("113", 54),
    ("113", 56),
    ("112", 9),
    ("112", 56),
    ("112", 57),
    ("112", 58),
    ("111", 15),
    ("111", 61),
    ("110", 24),
    ("110", 35),
    ("110", 39),
    ("110", 59),
    ("109", 9),
    ("109", 14),
    ("109", 45),
    ("109", 55),
    ("109", 64),
    ("109", 68),
    ("108", 26),
    ("108", 36),
    ("108", 37),
    ("108", 74),
]

pdf_files = {f.split("_")[0]: os.path.join(PDF_DIR, f) for f in os.listdir(PDF_DIR) if f.endswith(".pdf")}

for year, qnum in TARGET_IMG_QUESTIONS:
    doc = pymupdf.open(pdf_files[year])
    for pidx, page in enumerate(doc):
        txt = page.get_text("text")
        # 找題號與題幹關鍵字
        if f"{qnum}" in txt:
            img_info = page.get_image_info(xrefs=True)
            if img_info:
                print(f"[{year}-{qnum}] Page {pidx+1}: {len(img_info)} images -> {[ (round(x['bbox'][0]), round(x['bbox'][1]), round(x['bbox'][2]), round(x['bbox'][3])) for x in img_info ]}")
