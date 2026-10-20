import os
import json
import base64
import sys
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(__file__)
INDEX_HTML_PATH = os.path.join(BASE_DIR, "index.html")
ACLS_JSON_PATH = os.path.join(BASE_DIR, "acls_questions.json")
TAILWIND_JS_PATH = os.path.join(BASE_DIR, "tailwind.min.js")
STANDALONE_OUTPUT_PATH = os.path.join(BASE_DIR, "EMTP_ACLS_終極單一獨立版.html")


def encode_image_optimized_base64(img_rel_path: str, quality: int = 76) -> str:
    """將心電圖/圖譜轉為高清晰度最佳化 Base64 Data URI，兼顧銳利格線與約 2MB 輕量秒開。"""
    abs_path = os.path.join(BASE_DIR, img_rel_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"找不到圖片: {abs_path}")

    pix = pymupdf.Pixmap(abs_path)
    # 若含有透明通道 (alpha)，先轉為白底 RGB
    if pix.alpha:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix, False)

    # 若寬度超過 1200px，使用高品質雙線性縮放至約 1150px 寬度（12 導程小格依然完全清晰）
    if pix.width > 1200:
        scale = 1150.0 / pix.width
        new_w = int(pix.width * scale)
        new_h = int(pix.height * scale)
        pix = pymupdf.Pixmap(pix, new_w, new_h)

    jpg_bytes = pix.tobytes("jpeg", jpg_quality=quality)
    b64_str = base64.b64encode(jpg_bytes).decode("ascii")
    return f"data:image/jpeg;base64,{b64_str}"


def build_mobile_optimized_index_html() -> str:
    """讀取 index.html 並強化手機/平板觸控體驗（底部懸浮快速切換列 + 心電圖雙指縮放 + 觸控熱區）。"""
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. 移除 viewport 限制以確保平板/手機支援原生雙指縮放 (Pinch-to-Zoom)，並加入 touch-manipulation 消除 300ms 點擊延遲
    html = html.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0" />',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes" />'
    )

    # 2. 在 <style> 內加入手機觸控與底部懸浮安全距離優化樣式
    mobile_css = """
    button, label, select, input, textarea {
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }
    /* 心電圖燈箱支援雙指縮放與平移 */
    .pinch-zoom-container {
      touch-action: pan-x pan-y pinch-zoom;
      -webkit-overflow-scrolling: touch;
    }
    @media (max-width: 1023px) {
      body {
        padding-bottom: 76px;
      }
    }
  </style>"""
    if "pinch-zoom-container" not in html:
        html = html.replace("  </style>", mobile_css)

    # 3. 強化 Lightbox 全螢幕放大檢視器：加入手機/平板「雙指縮放」與「點擊切換 1x / 2x 放大」按鈕
    old_lightbox = """    <div class="max-w-6xl w-full flex items-center justify-between mb-3 px-2">
      <div class="flex items-center gap-2">
        <span id="lightbox-title" class="text-sm font-mono font-bold text-cyan-300 bg-slate-900 px-3 py-1 rounded-lg border border-cyan-500/30">
          114-55 心電圖檢視
        </span>
        <span class="text-xs text-slate-400 hidden sm:inline">（點擊背景或按 ESC 關閉）</span>
      </div>
      <button onclick="closeLightbox()" class="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-rose-600 text-white text-xs font-bold transition">
        ✕ 關閉放大檢視 (ESC)
      </button>
    </div>
    <div onclick="closeLightbox()" class="w-full flex-1 flex items-center justify-center overflow-auto cursor-zoom-out">
      <img
        id="lightbox-img"
        src=""
        alt="放大心電圖"
        onclick="event.stopPropagation()"
        class="max-w-full max-h-[85vh] object-contain bg-white p-3 rounded-2xl shadow-2xl border-2 border-cyan-500/40 cursor-default"
      />
    </div>"""

    new_lightbox = """    <div class="max-w-6xl w-full flex flex-wrap items-center justify-between gap-2 mb-3 px-2">
      <div class="flex items-center gap-2">
        <span id="lightbox-title" class="text-xs sm:text-sm font-mono font-bold text-cyan-300 bg-slate-900 px-3 py-1 rounded-lg border border-cyan-500/30">
          114-55 心電圖檢視
        </span>
        <span class="text-xs text-emerald-300 bg-emerald-950/60 border border-emerald-500/30 px-2 py-0.5 rounded">
          👌 支援雙指縮放或點擊倍率切換
        </span>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="toggleLightboxZoom()" id="btn-lightbox-zoom" class="px-3 py-1.5 rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-200 border border-cyan-500/40 text-xs font-bold transition">
          🔍 切換 200% 放大
        </button>
        <button onclick="closeLightbox()" class="px-3.5 py-1.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold transition shadow-lg">
          ✕ 關閉 (ESC)
        </button>
      </div>
    </div>
    <div id="lightbox-scroll-area" onclick="closeLightbox()" class="pinch-zoom-container w-full flex-1 flex items-center justify-center overflow-auto cursor-zoom-out">
      <img
        id="lightbox-img"
        src=""
        alt="放大心電圖"
        onclick="event.stopPropagation(); toggleLightboxZoom();"
        class="max-w-full max-h-[85vh] object-contain bg-white p-2 sm:p-3 rounded-2xl shadow-2xl border-2 border-cyan-500/40 cursor-zoom-in transition-all duration-200"
      />
    </div>"""

    if old_lightbox in html:
        html = html.replace(old_lightbox, new_lightbox)

    # 4. 在 </body> 前加入手機/平板專屬「底部懸浮快速切換列 (Mobile Sticky Action Bar)」
    mobile_bottom_bar = """
  <!-- ==================== 手機/平板專屬：底部懸浮快速切換列 (Mobile/Tablet Sticky Bottom Bar) ==================== -->
  <nav class="lg:hidden fixed bottom-0 inset-x-0 z-40 bg-[#070d19]/95 backdrop-blur-md border-t border-slate-800 px-3 py-2.5 shadow-2xl">
    <div class="max-w-xl mx-auto grid grid-cols-4 gap-2 items-center">
      <button
        onclick="prevQuestion()"
        id="btn-mobile-prev"
        class="py-2.5 px-2 rounded-xl text-xs font-bold bg-slate-800 active:bg-slate-700 text-slate-200 border border-slate-700 flex items-center justify-center gap-1 disabled:opacity-40"
      >
        <span>←</span> <span>上一題</span>
      </button>
      <button
        onclick="toggleStarCurrent()"
        id="btn-mobile-star"
        class="py-2.5 px-2 rounded-xl text-xs font-bold bg-slate-800 active:bg-slate-700 text-amber-300 border border-slate-700 flex items-center justify-center gap-1"
      >
        <span id="mobile-star-icon">☆</span> <span>收藏</span>
      </button>
      <button
        onclick="scrollToOrRevealAnalysis()"
        id="btn-mobile-analysis"
        class="py-2.5 px-2 rounded-xl text-xs font-bold bg-emerald-500/20 active:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 flex items-center justify-center gap-1"
      >
        <span>🧠</span> <span>看解析</span>
      </button>
      <button
        onclick="nextQuestion()"
        id="btn-mobile-next"
        class="py-2.5 px-2 rounded-xl text-xs font-bold bg-cyan-500 active:bg-cyan-400 text-slate-950 shadow-md shadow-cyan-500/20 flex items-center justify-center gap-1 disabled:opacity-40"
      >
        <span>下一題</span> <span>→</span>
      </button>
    </div>
  </nav>
"""

    if "btn-mobile-prev" not in html:
        html = html.replace(
            "  <!-- 引入 104 題結構化題庫資料檔 (免開 Server 零 CORS 阻擋) -->",
            mobile_bottom_bar + "\n  <!-- 引入 104 題結構化題庫資料檔 (免開 Server 零 CORS 阻擋) -->"
        )

    # 5. 在 JS 中補上同步更新手機底部按鈕狀態、點擊「看解析」自動平滑捲動至解析區、以及心電圖 200% 倍率切換函式
    old_nav_enable = """      // 8. 上下題按鈕啟用狀態
      document.getElementById('btn-prev-q').disabled = currentIndex <= 0;
      document.getElementById('btn-next-q').disabled = currentIndex >= filteredQuestions.length - 1;
      document.getElementById('btn-reveal-analysis').classList.toggle('hidden', isRevealed);"""

    new_nav_enable = """      // 8. 上下題按鈕啟用狀態（同步桌機與手機底部懸浮列）
      const atFirst = currentIndex <= 0;
      const atLast = currentIndex >= filteredQuestions.length - 1;
      document.getElementById('btn-prev-q').disabled = atFirst;
      document.getElementById('btn-next-q').disabled = atLast;
      document.getElementById('btn-reveal-analysis').classList.toggle('hidden', isRevealed);
      const mobPrev = document.getElementById('btn-mobile-prev');
      const mobNext = document.getElementById('btn-mobile-next');
      const mobStarIcon = document.getElementById('mobile-star-icon');
      if (mobPrev) mobPrev.disabled = atFirst;
      if (mobNext) mobNext.disabled = atLast;
      if (mobStarIcon) mobStarIcon.textContent = isStarred ? '⭐' : '☆';"""

    if old_nav_enable in html:
        html = html.replace(old_nav_enable, new_nav_enable)

    extra_mobile_js = """
    let isLightboxZoomed = false;
    function toggleLightboxZoom() {
      const img = document.getElementById('lightbox-img');
      const btn = document.getElementById('btn-lightbox-zoom');
      const scrollArea = document.getElementById('lightbox-scroll-area');
      isLightboxZoomed = !isLightboxZoomed;
      if (isLightboxZoomed) {
        img.className = 'w-[180vw] sm:w-[150vw] max-w-none max-h-none object-contain bg-white p-2 sm:p-3 rounded-2xl shadow-2xl border-2 border-cyan-500/40 cursor-zoom-out transition-all duration-200';
        scrollArea.classList.remove('items-center', 'justify-center');
        scrollArea.classList.add('items-start', 'justify-start');
        if (btn) btn.textContent = '🔍 恢復 100% 適應大小';
      } else {
        img.className = 'max-w-full max-h-[85vh] object-contain bg-white p-2 sm:p-3 rounded-2xl shadow-2xl border-2 border-cyan-500/40 cursor-zoom-in transition-all duration-200';
        scrollArea.classList.add('items-center', 'justify-center');
        scrollArea.classList.remove('items-start', 'justify-start');
        if (btn) btn.textContent = '🔍 切換 200% 放大';
      }
    }

    function scrollToOrRevealAnalysis() {
      const q = filteredQuestions[currentIndex];
      if (!q) return;
      manualRevealMap[q.id] = true;
      renderCurrentQuestion();
      setTimeout(() => {
        const unlockedEl = document.getElementById('analysis-unlocked-container');
        if (unlockedEl) {
          unlockedEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 60);
    }
"""

    if "function toggleLightboxZoom()" not in html:
        html = html.replace(
            "    function closeLightbox() {",
            extra_mobile_js + "\n    function closeLightbox() {\n      if (isLightboxZoomed) toggleLightboxZoom();"
        )

    return html


def main():
    # 先同步更新標準版 index.html 的手機/平板觸控體驗
    updated_index_html = build_mobile_optimized_index_html()
    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(updated_index_html)
    print("1. 已更新 index.html 加入手機/平板底部懸浮導覽列與心電圖雙指/倍率縮放功能。")

    # 讀取 104 題 JSON，將所有 23 張圖片轉為最佳化 Base64 Data URI
    with open(ACLS_JSON_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    encoded_img_count = 0
    for q in questions:
        if "image" in q and q["image"]:
            q["image"] = encode_image_optimized_base64(q["image"], quality=76)
            encoded_img_count += 1

    print(f"2. 已將 {encoded_img_count} 張心電圖與生理圖譜轉為高解析度 Base64 內嵌格式。")

    # 讀取本地 tailwind.min.js
    with open(TAILWIND_JS_PATH, "r", encoding="utf-8") as f:
        tailwind_js = f.read()

    # 將外部 <script src="tailwind.min.js"></script> 與 <script src="acls_data.js"></script> 替換為內嵌 <script>
    standalone_html = updated_index_html.replace(
        '<script src="tailwind.min.js"></script>',
        f"<script>\n/* Inlined Tailwind CSS Engine */\n{tailwind_js}\n</script>"
    )

    inline_data_script = (
        "<script>\n"
        "// Inlined 104 ACLS Questions + 23 Base64 ECG Images\n"
        "window.ACLS_QUESTIONS = "
        + json.dumps(questions, ensure_ascii=False)
        + ";\n</script>"
    )

    standalone_html = standalone_html.replace(
        '<script src="acls_data.js"></script>',
        inline_data_script
    )

    with open(STANDALONE_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(standalone_html)

    size_mb = os.path.getsize(STANDALONE_OUTPUT_PATH) / (1024 * 1024)
    print(f"3. 成功打包終極單一獨立版：{STANDALONE_OUTPUT_PATH}")
    print(f"   檔案總大小：{size_mb:.2f} MB（單一檔案，100% 離線免外部圖檔）")


if __name__ == "__main__":
    main()
