import os
import re
import sys
import json
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

PDF_DIR = os.path.join(os.path.dirname(__file__), "pdfs")

# ACLS 專項關鍵字篩選字典
ACLS_KEYWORDS = [
    # 核心與復甦
    "ACLS", "OHCA", "ROSC", "心肺復甦", "復甦後", "目標體溫", "TTM", "葉克膜", "ECMO",
    # 心律與傳導
    "心電圖", "ECG", "EKG", "導程", "導極", "QRS", "ST段", "ST-T", "STEMI", "NSTEMI",
    "心室顫動", "VF", "心室頻脈", "VT", "PEA", "無脈性", "Asystole",
    "心搏過緩", "心搏過速", "頻脈", "緩脈", "房室傳導阻滯", "AV block", "心房顫動", "心房撲動",
    "PSVT", "SVT", "Torsades", "多形性", "竇房結", "房室結", "傳導系統", "去極化", "右心室梗塞", "心肌缺氧",
    # 電擊與節律器
    "電擊", "去顫", "同步", "整律", "cardioversion", "defibrillation", "AED", "焦耳", "節律器", "TCP", "pacing",
    # 5H5T 與心因急症
    "5H5T", "心包填塞", "心包膜填塞", "tamponade", "張力性氣胸", "肺栓塞", "肺動脈栓塞",
    "高血鉀", "低血鉀", "高尖 T 波", "高尖T波", "低體溫", "冠狀動脈", "心肌梗塞", "心絞痛", "急性冠心症", "ACS",
    # 核心急救藥物
    "Epinephrine", "腎上腺素", "Amiodarone", "Adenosine", "Atropine", "阿托品", "Lidocaine",
    "Dopamine", "Norepinephrine", "NTG", "硝化甘油", "硝酸鹽", "阿斯匹靈", "Aspirin", "硫酸鎂", "Magnesium",
    "鈣離子", "Calcium", "碳酸氫鈉", "Sodium bicarbonate", "Bicarbonate"
]


import unicodedata


def clean_page_headers(text):
    text = unicodedata.normalize("NFKC", text)
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if re.match(r"^衛生福利部\s*\d+\s*年度高級救護技術員甄試筆試", s):
            continue
        if re.match(r"^第\s*\d+\s*頁\s*,\s*共\s*\d+\s*頁$", s) or re.match(r"^第\s*\d+\s*頁\s*，\s*共\s*\d+\s*頁$", s):
            continue
        if "准考證號碼" in s or "受訓單位" in s:
            continue
        if s.startswith("單選題") or s.startswith("※括號()內答案"):
            continue
        if s in ("答案 題號 題目", "答案 題號", "題目"):
            continue
        if "所有試題均已完成" in s:
            continue
        cleaned.append(s)
    return "\n".join(cleaned)


def extract_all_questions_from_pdf(pdf_path, year):
    doc = pymupdf.open(pdf_path)
    full_text = ""
    for page in doc:
        page_text = page.get_text("text")
        full_text += "\n" + clean_page_headers(page_text)

    questions = []
    lines = [line.strip() for line in full_text.split("\n") if line.strip()]

    # 將多行答案合併，例如 "C" + "(送" + "分)" 或 "D(A、" + "B、C)"
    merged_lines = []
    i = 0
    while i < len(lines):
        cur = lines[i]
        # 情況1: cur 是單一字母 A-D，下一行以 '(' 開頭且短於 8 字元
        if re.match(r"^[A-D]$", cur) and i + 1 < len(lines) and lines[i + 1].startswith("(") and not re.match(r"^\([A-D]\)", lines[i + 1]):
            acc = cur
            i += 1
            while i < len(lines):
                acc += lines[i]
                if ")" in lines[i]:
                    i += 1
                    break
                i += 1
            merged_lines.append(acc)
        # 情況2: cur 含有 '(' 但還沒遇到 ')'，且為短答案行
        elif "(" in cur and ")" not in cur and len(cur) <= 10 and not re.match(r"^\([A-D]\)", cur):
            acc = cur
            i += 1
            while i < len(lines):
                acc += lines[i]
                if ")" in lines[i]:
                    i += 1
                    break
                i += 1
            merged_lines.append(acc)
        else:
            merged_lines.append(cur)
            i += 1

    ans_pattern = re.compile(r"^([A-D]+(?:\([^\)]+\))?|送分|一律給分)$")

    q_positions = {}
    search_idx = 0
    for qnum in range(1, 101):
        # 尋找題號 qnum
        q_regex_dot_or_space = re.compile(rf"^{qnum}(?:\.|\s+)(.*)$")
        q_regex_exact = re.compile(rf"^{qnum}\.?$")
        found_idx = -1
        for idx in range(search_idx, len(merged_lines)):
            line = merged_lines[idx]
            # 檢查前一行是否為答案
            prev_is_ans = (idx > 0 and bool(ans_pattern.match(merged_lines[idx - 1])))
            # 或者同一行包含 "答案 題號"
            same_line_m = re.match(rf"^([A-D]+(?:\([^\)]+\))?)\s+{qnum}(?:\.|\s+)?(.*)$", line)
            if same_line_m:
                found_idx = idx
                q_positions[qnum] = {
                    "ans_idx": idx,
                    "q_idx": idx,
                    "ans": same_line_m.group(1),
                    "first_line_rest": same_line_m.group(2).strip()
                }
                search_idx = idx + 1
                break
            elif prev_is_ans and (q_regex_exact.match(line) or q_regex_dot_or_space.match(line)):
                m_rest = q_regex_dot_or_space.match(line)
                rest = m_rest.group(1).strip() if m_rest else ""
                found_idx = idx
                q_positions[qnum] = {
                    "ans_idx": idx - 1,
                    "q_idx": idx,
                    "ans": merged_lines[idx - 1],
                    "first_line_rest": rest
                }
                search_idx = idx + 1
                break
        if found_idx == -1:
            print(f"  [警告] {year} 年度找不到第 {qnum} 題！(search_idx={search_idx})")

    for qnum in range(1, 101):
        if qnum not in q_positions:
            continue
        info = q_positions[qnum]
        start_line = info["q_idx"] + 1
        if qnum + 1 in q_positions:
            end_line = q_positions[qnum + 1]["ans_idx"]
        else:
            end_line = len(merged_lines)

        body_lines = []
        if info["first_line_rest"]:
            body_lines.append(info["first_line_rest"])
        body_lines.extend(merged_lines[start_line:end_line])
        raw_q_text = "\n".join(body_lines)
        stem, opts = parse_question_and_options(raw_q_text)
        questions.append({
            "id": f"{year}-{qnum}",
            "year": int(year),
            "qnum": qnum,
            "answer": info["ans"],
            "question": stem,
            "options": opts
        })
    return questions


def parse_question_and_options(raw_text):
    text = re.sub(r"\r\n?", "\n", raw_text)
    m_a = re.search(r"[\(（]A[\)）]", text)
    if not m_a:
        return text.replace("\n", ""), []
    q_stem = text[:m_a.start()].replace("\n", "").strip()
    opt_part = text[m_a.start():]
    parts = re.split(r"[\(（]([A-D])[\)）]", opt_part)
    options = []
    for i in range(1, len(parts) - 1, 2):
        label = parts[i]
        val = parts[i + 1].replace("\n", "").strip()
        options.append(f"({label}) {val}")
    return q_stem, options


def main():
    all_questions = []
    all_acls_candidates = []
    for fname in sorted(os.listdir(PDF_DIR), reverse=True):
        if not fname.endswith(".pdf"):
            continue
        year = fname.split("_")[0]
        pdf_path = os.path.join(PDF_DIR, fname)
        qs = extract_all_questions_from_pdf(pdf_path, year)
        print(f"[{year}年度] 成功擷取題數: {len(qs)} / 100")
        for q in qs:
            full_str = q["question"] + " " + " ".join(q["options"])
            matched_kw = [kw for kw in ACLS_KEYWORDS if kw.lower() in full_str.lower()]
            if matched_kw:
                q["matched_keywords"] = matched_kw
                all_acls_candidates.append(q)
        all_questions.extend(qs)

    print(f"\n7個年度總擷取題數: {len(all_questions)} / 700")
    print(f"符合 ACLS 關鍵字之候選題數: {len(all_acls_candidates)}")

    out_all = os.path.join(os.path.dirname(__file__), "all_emtp_108_114.json")
    with open(out_all, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

    out_acls = os.path.join(os.path.dirname(__file__), "raw_acls_candidates.json")
    with open(out_acls, "w", encoding="utf-8") as f:
        json.dump(all_acls_candidates, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
