import os
import sys
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

PDF_DIR = os.path.join(os.path.dirname(__file__), "pdfs")
IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMG_DIR, exist_ok=True)

pdf_files = {f.split("_")[0]: os.path.join(PDF_DIR, f) for f in os.listdir(PDF_DIR) if f.endswith(".pdf")}

# 定義每題對應的 (年度, 頁碼(1-indexed), 裁切區域或圖片索引)
# 使用 page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=rect) 進行 300% 高解析度無損裁切，
# 這樣像 112-58 (含圖1~圖4標籤)、111-15 (含A~D四張EtCO2圖)、109-9 (含A~D四張EtCO2圖) 都能把選項文字與波形完整裁切在一張高清圖內！
CROP_SPECS = {
    "114-55": ("114", 11, (90, 140, 560, 455)),
    "113-54": ("113", 11, (90, 103, 570, 276)),
    "113-56": ("113", 12, (90, 117, 566, 316)),
    "112-9":  ("112", 2,  (88, 655, 560, 770)),
    "112-56": ("112", 12, (88, 189, 508, 272)),
    "112-57": ("112", 12, (88, 383, 508, 547)),
    "112-58": ("112", 12, (88, 638, 562, 725)),
    "111-15": ("111", 3,  (86, 298, 555, 585)),
    "111-61": ("111", 11, (86, 97,  450, 300)),
    "110-24": ("110", 4,  (90, 660, 378, 736)),
    "110-35": ("110", 6,  (90, 588, 332, 681)),
    "110-39": ("110", 7,  (90, 389, 350, 465)),
    "110-59": ("110", 11, (90, 425, 428, 608)),
    "109-9":  ("109", 2,  (88, 288, 540, 504)),
    "109-14": ("109", 3,  (86, 331, 316, 405)),
    "109-45": ("109", 8,  (88, 600, 500, 705)),
    "109-55": ("109", 10, (88, 206, 495, 467)),
    "109-64": ("109", 12, (88, 205, 512, 414)),
    "109-68": ("109", 13, (88, 129, 460, 236)),
    "108-26": ("108", 5,  (86, 110, 564, 237)),
    "108-36": ("108", 7,  (86, 150, 564, 251)),
    "108-37": ("108", 7,  (86, 360, 565, 582)),
    "108-74": ("108", 15, (86, 95,  564, 271)),
}

for qid, (year, pno, bbox) in CROP_SPECS.items():
    doc = pymupdf.open(pdf_files[year])
    page = doc[pno - 1]
    clip_rect = pymupdf.Rect(*bbox)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(3.0, 3.0), clip=clip_rect, alpha=False)
    out_file = os.path.join(IMG_DIR, f"{qid}.png")
    pix.save(out_file)
    print(f"已裁切匯出: {out_file} ({pix.width}x{pix.height})")
