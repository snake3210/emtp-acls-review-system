import re
import os
import sys
import urllib.parse
import urllib3
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TSEM (台灣急診醫學會) 108 ~ 114 年度 EMT-P 甄試筆試題目及答案公告頁面
EXAM_PAGES = {
    "114": "https://www.sem.org.tw/News/11/Details/1515",
    "113": "https://www.sem.org.tw/News/11/Details/1333",
    "112": "https://www.sem.org.tw/News/11/Details/1137",
    "111": "https://www.sem.org.tw/News/11/Details/945",
    "110": "https://www.sem.org.tw/News/11/Details/734",
    "109": "https://www.sem.org.tw/News/11/Details/485",
    "108": "https://www.sem.org.tw/News/11/Details/484",
}

BASE_URL = "https://www.sem.org.tw"
PDF_DIR = os.path.join(os.path.dirname(__file__), "pdfs")
os.makedirs(PDF_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for year, url in EXAM_PAGES.items():
    print(f"=== 正在解析 {year} 年度公告頁面: {url} ===")
    try:
        resp = requests.get(url, headers=headers, timeout=15, verify=False)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # 尋找所有附件或 PDF 連結
        links = soup.find_all("a", href=True)
        found = False
        for a in links:
            href = a["href"]
            text = a.get_text(strip=True)
            if ".pdf" in href.lower() or ".pdf" in text.lower() or "download" in href.lower() or "筆試" in text or "題目" in text or "答案" in text:
                full_url = urllib.parse.urljoin(BASE_URL, href)
                print(f"  找到連結: [{text}] -> {full_url}")
                found = True
                # 下載檔案
                safe_name = re.sub(r'[\\/*?:"<>|]', "_", text) or f"{year}_exam.pdf"
                if not safe_name.lower().endswith(".pdf"):
                    safe_name += ".pdf"
                out_path = os.path.join(PDF_DIR, f"{year}_{safe_name}")
                if not os.path.exists(out_path):
                    r_pdf = requests.get(full_url, headers=headers, timeout=30, verify=False)
                    if r_pdf.status_code == 200 and len(r_pdf.content) > 1000:
                        with open(out_path, "wb") as f:
                            f.write(r_pdf.content)
                        print(f"  -> 已儲存至: {out_path} ({len(r_pdf.content)} bytes)")
        if not found:
            for a in links:
                if "News" not in a["href"] and "Content" not in a["href"] and "Activity" not in a["href"]:
                    print("  其他連結:", a.get_text(strip=True), a["href"])
    except Exception as e:
        print(f"  錯誤: {e}")
