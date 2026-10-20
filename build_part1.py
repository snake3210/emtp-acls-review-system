import os
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(__file__)
ALL_QS_PATH = os.path.join(BASE_DIR, "all_emtp_108_114.json")

with open(ALL_QS_PATH, "r", encoding="utf-8") as f:
    raw_map = {q["id"]: q for q in json.load(f)}

# 圖片題清單
IMAGE_IDS = {
    "114-55", "113-54", "113-56", "112-9", "112-56", "112-57", "112-58",
    "111-15", "111-61", "110-24", "110-35", "110-39", "110-59",
    "109-9", "109-14", "109-45", "109-55", "109-64", "109-68",
    "108-26", "108-36", "108-37", "108-74"
}

# 114 ~ 112 年度深度解析資料庫
ANNOTATIONS_PART1 = {
    # ==================== 114 年度 ====================
    "114-3": {
        "category": "心搏停止",
        "algorithm_path": [
            "OHCA 頑固性心室顫動 (Refractory VF：經 ≥ 3 次去顫電擊與 Amiodarone/Lidocaine 仍持續 VF)",
            "考慮進階體外心肺復甦術 (ECPR / V-A ECMO)",
            "實證醫學外推性評估 (External Validity)：檢視本地 EMS 反應時間、醫院 ECMO 團隊啟動速度與病人收案條件是否與 RCT 相似"
        ],
        "key_triggers": ["頑固性心室顫動 (refractory VF)", "院前葉克膜 (ECMO)", "ARREST Trial vs INCEPTION Trial", "EMS 系統環境相似性"],
        "confusion_trap": "• 易混淆選項 (A)/(B)：誤以為只要是隨機控制試驗 (RCT) 且 P < 0.05 具統計顯著性，就能直接套用於所有 EMS 系統。\n• 臨床與研究陷阱：2020《Lancet》ARREST Trial 為單一高量能醫學中心（明尼蘇達大學），從啟動到上機極快，存活率顯著提升；但 2023《NEJM》INCEPTION Trial 為多中心真實世界研究，因各院上機時間較長導致無顯著差異。因此導入 ECPR 前必須優先評估「研究族群與本地 EMS 系統環境是否相似（外推性）」！",
        "guideline_check": "• AHA 2020/2025 ACLS 指引：針對常規 CPR 無效之特定可逆病因心搏停止病人，若醫療體系具備熟練且能快速部署之團隊，可考慮使用 ECPR（Class 2a, LOE B-R）。\n• 關鍵決策門檻：從心搏停止到完成 V-A ECMO 轉流（Low-flow time）最好控制在 60 分鐘內。"
    },
    "114-12": {
        "category": "心搏過速",
        "algorithm_path": [
            "心臟正常節律起搏點：竇房結 (SA node, 60-100 bpm)",
            "經心房內傳導路徑傳至房室結 (AV node, 40-60 bpm) 延遲約 0.1 秒",
            "經希氏束 (Bundle of His)、左右束支至普金吉氏纖維 (Purkinje fibers, 20-40 bpm) 引發心室去極化 (QRS 波)",
            "若存在額外傳導路徑 (Accessory pathway，如 WPW 症候群 Bundle of Kent) 易形成迴旋 (Re-entry) 導致陣發性心搏過速 (PSVT)"
        ],
        "key_triggers": ["心臟傳導系統", "心搏過速", "額外的傳導路徑", "P 波代表心房去極化"],
        "confusion_trap": "• 選項 (A)/(B) 陷阱：正常心臟電氣傳導始於「竇房結 (SA node)」並由其主導最高心跳速率，而非房室結或普金吉氏纖維。\n• 選項 (D) 陷阱：心電圖中的「P 波」代表心房去極化，「QRS 複合波」才代表心室去極化，「T 波」則代表心室再極化。",
        "guideline_check": "• 符合基礎心電圖生理與 ACLS 頻脈機轉：絕大多數規律窄 QRS 波頻脈（PSVT）源於房室結內雙路徑（AVNRT）或存在房室間額外副傳導路徑（AVRT）引發的再迴旋（Re-entry）機轉。"
    },
    "114-20": {
        "category": "ACS與12導程",
        "algorithm_path": [
            "疑似急性冠心症 (ACS) 胸痛評估",
            "給予舌下硝化甘油 (NTG 0.4 mg SL) 擴張冠狀動脈與周邊靜脈 (降低前負荷)",
            "藥理副作用監測：硝酸鹽類釋放一氧化氮 (NO) 平滑肌舒張 → 腦膜與顱內血管擴張引發「搏動性劇烈頭痛」+ 周邊靜脈擴張回心血量減少引發「低血壓」"
        ],
        "key_triggers": ["胸悶痛", "NTG 舌下含片", "劇烈頭痛與血壓下降", "硝酸鹽藥物導致顱內血管擴張"],
        "confusion_trap": "• 易誤選 (A) 過敏反應或 (C) 顱內壓下降：看到給藥後血壓下降很容易聯想到過敏性休克，但「劇烈頭痛 + 低血壓」是 NTG 最典型的藥理血管擴張作用！\n• 選項 (C) 相反陷阱：NTG 使顱內血管擴張、腦血流量增加，會導致「顱內壓上升（ICP 微升）」與血管性頭痛，而非顱內壓下降。",
        "guideline_check": "• 符合 AHA ACLS ACS 用藥安全規範：給予 NTG 前務必確認「收縮壓 SBP ≥ 90 mmHg（或未較基準值下降 > 30 mmHg）」、「無心搏過緩 (< 50 bpm) 或嚴重頻脈 (> 100 bpm)」、「無右心室梗塞」，且「24~48 小時內未服用磷酸二酯酶抑制劑（Sildenafil 24h / Tadalafil 48h）」。"
    },
    "114-24": {
        "category": "ACS與12導程",
        "algorithm_path": [
            "急性胸痛鑑別診斷 (ACS vs 心包膜炎 vs 主動脈剝離 vs 肺栓塞)",
            "評估疼痛加劇與緩解因子 (OPQRST 之 Provocation/Palliation)",
            "平躺或深吸氣時因心包膜摩擦牽扯而劇痛、身體坐起前傾 (Leaning forward) 時緩解 → 典型急性心包膜炎 (Acute Pericarditis)"
        ],
        "key_triggers": ["心包膜炎 (pericarditis)", "躺臥時加劇胸痛", "身體前傾或坐姿時可緩解"],
        "confusion_trap": "• 選項 (A)/(C) 是典型心絞痛 (Angina pectoris)：常在運動、寒冷或情緒激動時誘發，且休息或使用 NTG 舌下含片後可緩解（心包膜炎含服 NTG 無效）。\n• 選項 (B) 雖可見於肋膜性胸痛或心包膜炎，但最能精準區別心包膜炎與其他胸痛的特異性姿勢徵象為「平躺加劇、坐起身體前傾緩解（選項 D）」。",
        "guideline_check": "• 符合 ACLS 急性胸痛鑑別診斷要點：急性心包膜炎的 12 導程心電圖常呈現「廣泛性（多導程）凹向上（Concave）之 ST 段上升」合併 PR 段壓低（PR depression），不可誤判為 STEMI 而錯誤啟動血栓溶解劑治療！"
    },
    "114-32": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "65 歲男性突發昏厥、冒冷汗、低血壓 (80/40mmHg) 伴隨兩側肺部濕囉音與下肢水腫 (急性左心衰竭/心因性休克表現)",
            "轉送途中突發抽搐並轉為心室顫動 (VF) OHCA",
            "回溯 5H5T 可逆病因：典型缺血性心因性休克惡化為致死性心律不整 → 冠狀動脈血栓 (Thrombosis, coronary / 急性心肌梗塞)"
        ],
        "key_triggers": ["昏厥冒冷汗", "濕囉音 (crackles)", "血壓 80/40mmHg", "VF 心律", "5H5T：冠狀動脈血栓"],
        "confusion_trap": "• 易混淆選項 (A) 低血容積與 (B) 張力性氣胸：低血容積休克肺音應清晰且頸靜脈扁平，不會出現雙側肺水腫濕囉音與下肢水腫；張力性氣胸則是「單側呼吸音減弱或消失、叩診鼓音」，而非濕囉音。\n• 破題關鍵：成人突發性 VF 最常見的 5H5T 原因即為急性冠狀動脈血栓（AMI）引發心肌缺血電氣不穩及急性心因性肺水腫。",
        "guideline_check": "• 符合 AHA ACLS 5H5T 病因學：當 OHCA 初始心律為可電擊心律（VF/pVT），且病史有冒冷汗、急性肺水腫（濕囉音）時，5H5T 首要考慮「冠狀動脈血栓（Thrombosis, coronary）」，ROSC 後應立即執行 12 導程心電圖並評估緊急心導管（PCI）。"
    },
    "114-34": {
        "category": "ROSC照護",
        "algorithm_path": [
            "OHCA 病人經復甦後恢復自發性循環 (ROSC)",
            "評估神經學意識狀態：對語言指令無反應 (Comatose)",
            "啟動目標體溫管理 (TTM / Temperature Control)：每降低 1°C 體溫可減少約 6%~10% 大腦代謝率，抑制自由基、興奮性胺基酸釋放與細胞凋亡，減輕缺血再灌流腦損傷"
        ],
        "key_triggers": ["復甦後照護", "目標體溫管理 (TTM)", "減少大腦代謝與缺血再灌流傷害"],
        "confusion_trap": "• 選項 (B) 陷阱：ROSC 後必須維持正常或偏高之平均動脈壓（MAP ≥ 65 mmHg、SBP ≥ 90 mmHg）以確保腦部灌流，絕對不能「降低血壓」。\n• 選項 (D) 陷阱：低溫會「減慢（降低）」全身酵素活性與藥物代謝速度（例如鎮靜劑與肌肉鬆弛劑清除變慢），而非增加藥物代謝速度。",
        "guideline_check": "• 符合 AHA 2020/2025 復甦後照護指引：所有在 ROSC 後仍無法遵從指令（昏迷）的成人患者，皆建議執行目標體溫管理（TTM），核心目的為神經保護（降低腦代謝率與減緩缺血再灌流傷害）。"
    },
    "114-35": {
        "category": "ROSC照護",
        "algorithm_path": [
            "恢復自發性循環 (ROSC)",
            "呼吸與氧合優化：調整 FiO2 維持 SpO2 92%~98% (避免低血氧與高血氧)，維持 PaCO2 35~45 mmHg (EtCO2 30~40 mmHg)",
            "血行動力學穩定：給予輸液或升壓藥，維持收縮壓 SBP ≥ 90 mmHg 及平均動脈壓 MAP ≥ 65 mmHg",
            "評估意識狀態：若無法遵從指令，啟動目標體溫管理 (TTM 32°C~36°C 維持至少 24 小時，並積極預防發燒 > 37.7°C)"
        ],
        "key_triggers": ["復甦後照護", "目標體溫管理 (TTM)", "復甦後的血氧濃度：92~98%"],
        "confusion_trap": "• 選項 (A) 雙重數字陷阱：TTM 目標溫度範圍在 2015/2020 指引為「32~36ºC」（而非舊版 32~34ºC），且維持目標體溫時間為「至少 24 小時」（而非 48 小時）。\n• 選項 (B) 二氧化碳陷阱：復甦後應維持「正常碳酸血症（PaCO2 35~45 mmHg）」，高碳酸血症會使腦血管擴張、顱內壓升高。\n• 選項 (D) 血壓陷阱：平均動脈壓 MAP ≥ 65 mmHg 正確，但收縮壓標準為「SBP ≥ 90 mmHg」（而非 120 mmHg 以上）。",
        "guideline_check": "• 血氧目標演進：2015 版為 94~99%，2020 版起修正為「92~98%」。\n• 體溫控制演進：2020 版為「32~36ºC 至少 24 小時」；2023/2025 AHA Focused Update 整合 TTM-2 Trial 後改稱「體溫控制 (Temperature Control)」，建議維持體溫於「32ºC 至 37.5ºC 之間」並積極預防發燒。台灣 EMT-P 筆試仍以 2020 版數據（32~36ºC、至少 24 小時、SpO2 92~98%、SBP ≥ 90 / MAP ≥ 65 mmHg、PaCO2 35~45 mmHg）為命題基準。"
    },
    "114-52": {
        "category": "ACS與12導程",
        "algorithm_path": [
            "12 導程心電圖連續兩個以上解剖相關導極出現 ST-T 波變化",
            "解剖位置定位：V1-V2 = 中隔區 (Septal)；V3-V4 = 前壁 (Anterior)；V5-V6, I, aVL = 側壁 (Lateral)；II, III, aVF = 下壁 (Inferior)",
            "對應冠狀動脈：中隔/前壁 → 左前降支 (LAD)；側壁 → 左迴旋支 (LCx)；下壁 → 右冠狀動脈 (RCA，約佔 85%)"
        ],
        "key_triggers": ["12 導程心電圖", "ST-T 波變化", "心臟解剖位置配對", "下壁為導極 II, III, aVF"],
        "confusion_trap": "• 選項 (A)(B)(C) 將胸前導極全部故意錯位平移：V1, V2 才是「中隔區（Septal）」（非側壁）；V3, V4 才是「前壁（Anterior）」（非中隔區）；V5, V6（連同 I, aVL）才是「側壁（Lateral）」（非前壁）。\n• 必背口訣：1、2 中隔（Septal），3、4 前壁（Anterior），5、6 加 I、aVL 側壁（Lateral），II、III、aVF 下壁（Inferior）。",
        "guideline_check": "• 符合 AHA ACLS 12 導程心電圖定位標準。臨床上若發現下壁導極（II, III, aVF）ST 段上升，務必加做右側胸前導極（尤其 V4R）以確認是否合併右心室心肌梗塞。"
    },
    "114-53": {
        "category": "心搏停止",
        "algorithm_path": [
            "病患無意識、無呼吸或僅有瀕死喘息、無脈搏 (OHCA)",
            "心電圖節律判讀：完全無正常 P 波、QRS 波或 T 波，基線呈現混亂、無規則、大小振幅與寬窄皆不一致的顫動波 → 心室顫動 (VF)",
            "屬於可電擊心律 (Shockable rhythm) → 立即執行去顫電擊 (Defibrillation) 並接續 2 分鐘高品質 CPR"
        ],
        "key_triggers": ["心室顫動 (Ventricular Fibrillation, VF)", "無規則節律", "大小、寬窄不一"],
        "confusion_trap": "• 選項 (A) 是「單形性心室頻脈 (Monomorphic VT)」的特徵：連續快速、規律一致、寬 QRS 波且無 P 波。\n• 選項 (C) 常見於「心室撲動 (Ventricular flutter，正弦波型)」或超急性 T 波伴規則頻脈。\n• 選項 (D) 為正常竇性心律或竇性頻脈的特徵。",
        "guideline_check": "• 符合 AHA ACLS 可電擊心律判讀規範：心室顫動（VF）與無脈性心室頻脈（pVT）皆為可電擊心律，一旦確認應立即給予非同步去顫電擊（雙相波依製造商建議 120~200J，單相波 360J）。"
    },
    "114-54": {
        "category": "ACS與12導程",
        "algorithm_path": [
            "急性致命性胸痛鑑別診斷",
            "症狀特徵：突發性（瞬間達到最痛）、「撕裂樣 / 刀割樣 (Tearing/Ripping)」劇烈胸痛，並放射至背後肩胛骨間",
            "理學檢查關鍵徵象：雙側上肢收縮壓差 > 20 mmHg (或單側橈動脈脈搏減弱/消失) → 高度懷疑急性主動脈剝離 (Acute Aortic Dissection)"
        ],
        "key_triggers": ["撕裂樣胸痛", "放射至背部", "雙側上肢血壓差異大於 20 mmHg", "主動脈剝離"],
        "confusion_trap": "• 與選項 (A) 急性心肌梗塞的關鍵鑑別：心肌梗塞典型為胸骨後「壓迫感、緊縮感」，疼痛通常在數分鐘內逐漸加劇，且雙手血壓對稱；而主動脈剝離則是「一發作第 1 秒就痛到極點」的撕裂痛，若剝離假腔壓迫鎖骨下動脈開口，就會出現雙手收縮壓差 > 20 mmHg。\n• 臨床致命陷阱：若主動脈剝離往近端延伸侵犯右冠狀動脈開口，心電圖可能同時出現下壁 STEMI，若未量雙手血壓而誤給抗血小板/抗凝血劑或血栓溶解劑，將導致大出血死亡！",
        "guideline_check": "• 符合 AHA ACLS 與急診胸痛評估指引：到院前對所有非創傷性胸痛患者，除執行 12 導程心電圖外，應常規評估疼痛性質（是否為撕裂痛放射至背部）與兩側上肢脈搏/血壓對稱性，以排除主動脈剝離。"
    },
    "114-55": {
        "category": "ACS與12導程",
        "image": "images/114-55.png",
        "algorithm_path": [
            "缺血性胸悶評估 (BP 84/52mmHg 低血壓、HR 54 bpm 緩脈、SpO2 96%)",
            "判讀題附 12 導程心電圖：Lead II, III, aVF 出現顯著 ST 段上升，且 Lead I, aVL 出現鏡像 ST 段壓低 → 確診為下壁 STEMI",
            "下壁 STEMI 合併低血壓 (84/52mmHg) 與緩脈 → 高度懷疑合併右心室梗塞 (RV Infarction)",
            "處置決策：絕對禁用硝化甘油 (NTG)，建立靜脈管路給予生理食鹽水輸液以維持右心室前負荷 (Preload)"
        ],
        "key_triggers": ["血壓 84/52mmHg (低血壓)", "脈搏 54 次/min (緩脈)", "血氧 96%", "12 導程心電圖：II, III, aVF ST 段上升 (下壁 STEMI)", "避免硝化甘油並維持靜脈輸液"],
        "confusion_trap": "• 陷阱一（MONA 反射性給藥錯誤）：看到胸悶加 STEMI 就想選給 NTG（選項 A、D），忽略了「下壁 STEMI 常合併右心室梗塞」且病人收縮壓僅 84 mmHg（< 90 mmHg），給予 NTG 或半坐臥姿勢會使靜脈回心血量驟降，引發致命性休克！\n• 陷阱二（常規高流量給氧錯誤）：病人血氧飽和度為 96%（≥ 90%），依最新指引不需給予高流量氧氣（選項 A 錯誤）。",
        "guideline_check": "• 完全符合 AHA 2020/2025 ACS 指引：\n• 1. 僅在 SpO2 < 90%（或台灣部分預立醫囑 < 94%）或有呼吸窘迫時才給予氧氣。\n• 2. 下壁 STEMI 應加做右側心電圖（V4R），在排除右心室梗塞前或 SBP < 90 mmHg 時，絕對禁用硝酸鹽類藥物（NTG），應給予生理食鹽水（Normal Saline）輸液。"
    },
    "114-56": {
        "category": "心搏過速",
        "algorithm_path": [
            "有脈搏之頻脈 (HR ≥ 150 bpm)",
            "評估血行動力學：不穩定 (休克、低血壓、急性心衰竭、缺血性胸痛、意識改變)",
            "QRS 波寬度與節律分析：寬 QRS (≥ 0.12 秒) 且規則 (單形性 VT)",
            "立即執行同步心臟整律 (Synchronized Cardioversion) 初始劑量 100J"
        ],
        "key_triggers": ["頻脈", "血行動力學不穩定", "同步心臟整律 (synchronized cardioversion)", "寬波且規則：同步整律 100J"],
        "confusion_trap": "• 選項 (A) 與 (B) 能量數值故意對調：「窄波且規則（PSVT / Atrial flutter）」所需能量最小，初始應為 50~100J；「窄波且不規則（Atrial fibrillation）」才需要雙相波 120~200J（或單相波 200J）。\n• 選項 (D) 致命臨床陷阱：「寬波且不規則（Polymorphic VT / Torsades de pointes）」因 R 波形態不斷改變，無法穩定同步，嚴禁同步整律，必須改用「非同步去顫電擊（Defibrillation dose）」。",
        "guideline_check": "• 符合 AHA 2020/2025 ACLS 指引：2020 年起 AHA 強調優先依各廠牌雙相波電擊器建議之有效能量給予；若考題測驗傳統四大分類通則（窄規則 50-100J、窄不規則雙相 120-200J/單相 200J、寬規則 100J、寬不規則非同步去顫），台灣 EMT-P 甄試仍以此配對為標準答案。"
    },
    "114-57": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "5H5T 可逆病因評估：心包膜填塞 (Cardiac Tamponade)",
            "病理機轉：心包膜腔積液急遽增加 → 腔內壓力上升先壓迫壁最薄、壓力最低的「右心房與右心室」 → 舒張期無法充盈導致回心血量與心輸出量驟降",
            "院前處置：於執行心包膜穿刺術 (Pericardiocentesis) 前，給予靜脈晶體輸液補充前負荷以暫時維持心輸出量"
        ],
        "key_triggers": ["心包膜填塞 (cardiac tamponade)", "頸靜脈怒張", "血流動力學不穩定可給予靜脈輸液"],
        "confusion_trap": "• 選項 (B) 腔室陷阱：心包膜腔積液過多時，最先壓迫的是壓力較低的「右心房與右心室（造成右心室舒張期塌陷）」，而非壁厚壓高的左心室！\n• 選項 (C) 週期陷阱：心包膜填塞是限制心臟在「舒張期（Diastole）」的擴張充盈而影響回心血流，而非收縮期。\n• 選項 (D) 盛行率陷阱：典型貝克氏三徵象（Beck's triad：低血壓、頸靜脈怒張、心音模糊遙遠）在臨床上僅約 10%~40% 的急性心包膜填塞病人會同時完整出現，並非大多數皆可見。",
        "guideline_check": "• 符合 AHA ACLS 與 ATLS 指引：心包膜填塞屬於阻塞性休克（Obstructive shock），院前無法立即執行心包膜穿刺引流時，應給予靜脈輸液（Volume resuscitation）提高右心充盈壓，爭取後送時間。"
    },
    "114-58": {
        "category": "ACS與12導程",
        "algorithm_path": [
            "急性冠心症 (ACS) 12 導程心電圖分類：無 ST 段上升 (NSTE-ACS)",
            "抽血檢驗心肌旋轉蛋白 (Troponin I / T)",
            "Troponin 上升 → 非 ST 段上升心肌梗塞 (NSTEMI，已有部分心肌細胞缺血壞死)；Troponin 正常 → 不穩定心絞痛 (Unstable Angina，心肌缺血但尚未壞死)"
        ],
        "key_triggers": ["非 ST 段上升心肌梗塞 (NSTEMI)", "不穩定心絞痛 (Unstable Angina)", "心肌壞死、血中心肌酵素上升"],
        "confusion_trap": "• 選項 (A) 陷阱：NSTEMI 與不穩定心絞痛在 12 導程心電圖上表現相同（皆可能出現 ST 段壓低、T 波倒置或無明顯變化），兩者唯一的核心區別就是「NSTEMI 有心肌細胞壞死導致血中心肌酵素（Troponin）上升」。\n• 選項 (B) 陷阱：病理性 Q 波通常出現在穿透性心肌梗塞（STEMI）數小時至數天後，不穩定心絞痛不會產生新 Q 波。\n• 選項 (C) 陷阱：到院 90 分鐘內完成心導管（Door-to-balloon / Door-to-device ≤ 90 min）是「STEMI」的黃金指標，而非所有 NSTEMI 與 UA。",
        "guideline_check": "• 符合 AHA ACS 指引：到院前僅憑 12 導程心電圖無法區分 NSTEMI 與不穩定心絞痛（UA），必須到院檢驗高敏感度心肌旋轉蛋白（hs-cTn）才能確診。"
    },
    "114-60": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "OHCA 心搏停止",
            "心電圖有波形但無脈搏 → 判定為無脈性電氣活動 (PEA，不可電擊心律)",
            "立即高品質 CPR + 儘速給予 Epinephrine 1 mg IV/IO",
            "同步搜尋並矯正可逆原因 (5H5T) + 重點式超音波 (POCUS) 評估",
            "超音波顯示右心室明顯擴大 (RV dilation / D-shape LV) → 鎖定肺動脈栓塞 (Thrombosis, pulmonary)"
        ],
        "key_triggers": ["心電圖有波形但脈搏摸不到 (PEA)", "重點式心臟超音波 (POCUS)", "右心室明顯擴大", "肺動脈栓塞 (pulmonary embolism)"],
        "confusion_trap": "• 選項 (A) 心包膜填塞 vs (D) 肺動脈栓塞超音波表現極易搞混：\n• 1.「肺動脈栓塞（PE）」因肺動脈主幹被血栓堵住，右心室後負荷暴增，超音波下呈現「右心室明顯擴大（RV > LV）、心室中膈壓向左側呈 D-shape」。\n• 2.「心包膜填塞」則是心包膜腔出現黑色無回音積液包圍心臟，因外部擠壓導致「右心房與右心室舒張期塌陷（變扁而非擴大）」。\n• 3.「張力性氣胸」在胸腔超音波下則為肺滑動消失（Absent lung sliding）與條碼徵象（Barcode sign）。",
        "guideline_check": "• 符合 AHA 2020/2025 ACLS 指引：\n• 1. 重點式超音波（POCUS）可輔助識別 PEA 之可逆原因（如肺栓塞、心包填塞）。\n• 2. 嚴格警示：執行超音波檢查時，絕對不可延長中斷胸外按壓的時間（不得超過 10 秒），且不可單獨以心臟超音波無收縮作為終止復甦的唯一依據。"
    },
    "114-61": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "急性呼吸困難合併阻塞性休克/PEA 風險評估 (5H5T：Tension pneumothorax)",
            "理學檢查三核心：患側單側呼吸音減弱或消失 + 叩診鼓音 (Hyperresonance) + 休克低血壓/頸靜脈怒張/氣管偏向健側",
            "確診張力性氣胸 → 立即執行針刺減壓術 (Needle Decompression)"
        ],
        "key_triggers": ["張力性氣胸", "單側呼吸音減弱", "氣管偏移合併低血壓"],
        "confusion_trap": "• 選項 (A)「叩診實音（Dullness）」是大量血胸或胸腔積液的特徵，張力性氣胸叩診應為「鼓音（Hyperresonance）」，且多為單側。\n• 選項 (C)「雙側哮鳴音 + 粉紅色泡沫痰」是急性心因性肺水腫（Cardiac asthma）的典型表現。\n• 選項 (D)「心音極小聲（Muffled heart sounds）+ 頸靜脈怒張 + 低血壓」是心包膜填塞的貝克氏三徵象（Beck's triad），其雙側呼吸音通常清晰對稱。",
        "guideline_check": "• 符合 ATLS 第 10 版與 ACLS 5H5T 指引：成人張力性氣胸針刺減壓首選位置已更新為「患側第五肋間、腋前線至腋中線前緣」（兒童仍維持第二肋間鎖骨中線）。"
    },
    "114-74": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "末期腎病變 (ESRD) 洗腎患者週末未洗腎 + 進食高鉀飲食 (火鍋湯底、水果)",
            "出現呼吸困難、肺部濕囉音與下肢水腫 (體液過量) + 口周麻木、肌肉顫抖與緩脈 (HR 52 bpm)",
            "心電圖出現高尖 T 波 (Tall peaked T wave)、PR 間隔延長 → 典型高血鉀症 (Hyperkalemia, 5H5T 之 H)",
            "急救藥物：1. 穩定心肌膜電位 (Calcium gluconate / Calcium chloride) → 2. 促使鉀離子移入細胞內 (Sodium bicarbonate, Insulin + Glucose, Beta-2 agonist)"
        ],
        "key_triggers": ["規律血液透析", "火鍋與水果", "心率 52 次/min (緩脈)", "高尖 T 波、PR 間隔延長", "高血鉀合併體液過量"],
        "confusion_trap": "• 易誤選 (A) 單純體液過量導致低氧性心搏過緩：患者雖有肺水腫體液過量，但其 SpO2 為 95%（並非嚴重低血氧），且心電圖出現「高尖 T 波（Tenting T wave）與 PR 延長」是高血鉀症最具特異性的電氣指標！\n• 高血鉀心電圖惡化時序必背：高尖狹窄 T 波 → PR 間隔延長、P 波變平消失 → QRS 波變寬 → 正弦波（Sine wave）→ VF / Asystole。",
        "guideline_check": "• 符合 AHA ACLS 嚴重高血鉀急救指引：當高血鉀出現心電圖變化（高尖 T 波、寬 QRS）或嚴重緩脈時，第一線護心藥物為「靜脈注射鈣離子（Calcium chloride 10% 5-10 mL 或 Calcium gluconate 10% 15-30 mL IV slow push）」，注意鈣離子僅能穩定心肌細胞膜電位，並不會降低血鉀濃度！"
    },
    "114-80": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "高山搜救環境評估與重度低體溫 (中心體溫 30°C，5H5T 之 Hypothermia)",
            "病患尚有生命徵象時：移除濕冷衣物、採取被動與主動體外回溫，所有搬運與處置動作務必「極度輕柔」，避免機械刺激誘發心室顫動 (VF)",
            "若發生 OHCA：確認脈搏可延長至 30~45 秒；若為 VF 可先去顫電擊 1 次，在中心體溫 < 30°C 時暫緩給予 Epinephrine 等急救藥物，待回溫至 ≥ 30°C 後再延長給藥間隔 (每 6~10 分鐘) 給予"
        ],
        "key_triggers": ["中心體溫為攝氏 30 度 (低體溫)", "被動回溫、減少熱散失", "動作應保持輕柔，避免誘發 Vf"],
        "confusion_trap": "• 選項 (B) 陷阱：重度低體溫（< 30°C）伴隨 VF 時，心肌對去顫電擊反應極差，電擊 1 次無效後應專注於高品質 CPR 與積極回溫，待體溫回升至 ≥ 30°C 後再行電擊，而非在低溫下無限制反覆電擊。\n• 選項 (C) 劑量間隔陷阱：中度低體溫（30~34°C）因藥物代謝極慢，為避免回溫後產生藥物累積毒性，Epinephrine 給藥間隔應「加倍延長為每 6~10 分鐘一次」，而非標準的每 3 分鐘一次！\n• 選項 (D) 緩脈陷阱：低體溫病患的「生理性竇性心搏過緩」是身體降低代謝的保護機制，回溫後即會自然恢復，不應使用經皮心臟節律器（TCP），以免誘發 VF！",
        "guideline_check": "• 符合 AHA ACLS 特殊情境（低體溫）指引：\n• 1. 體溫 < 30°C：暫緩 IV 急救藥物，去顫電擊以 1 次為限，優先回溫。\n• 2. 體溫 30~34°C：急救藥物給藥間隔延長為 2 倍（每 6~10 分鐘給一次 Epinephrine）。\n• 3. 體溫 ≥ 35°C：恢復標準 ACLS 給藥流程。"
    },

    # ==================== 113 年度 ====================
    "113-8": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "急救核心藥物給藥途徑與禁忌症檢核",
            "Amiodarone 於有脈搏寬 QRS 頻脈：150 mg 稀釋後靜脈慢速滴注 10 分鐘 (不可快速推注以免嚴重低血壓)",
            "Adenosine 於規則窄波頻脈 (PSVT)：6 mg 經近心端大靜脈「極快速推注 (IV rapid push)」並立即以 20 mL N/S 快速沖管",
            "毛地黃 (Digoxin) 中毒伴隨高血鉀：忌用鈣離子 (Calcium)，以免誘發不可逆之「石頭心 (Stone heart)」心室攣縮"
        ],
        "key_triggers": ["急救藥物使用時機", "Amiodarone", "Adenosine", "氯化鈣 (Calcium chloride)", "Midazolam 肌肉注射"],
        "confusion_trap": "• 選項 (A) 陷阱：Amiodarone 只有在「無脈搏（VF/pVT OHCA）」時才是 300 mg 快速靜脈推注（IV push）；若為「有脈搏的寬 QRS 波頻脈」，必須以 150 mg 靜脈滴注（IV drip over 10 mins），快速推注會造成嚴重低血壓與心搏過緩！\n• 選項 (B) 陷阱：Adenosine 半衰期小於 10 秒，若用「靜脈滴注（IV drip）」在抵達心臟前就會被紅血球與血管內皮代謝光，必須採用「閃電般快速靜脈推注（Rapid IV bolus）」！\n• 選項 (C) 經典毒理陷阱：一般高血鉀首選鈣離子護心，但「毛地黃（Digoxin）中毒引起的高血鉀」傳統上視為給予鈣離子的禁忌症（恐引發細胞內鈣超載與心室強直收縮），應使用 Digoxin immune Fab 解毒劑。",
        "guideline_check": "• 符合 AHA ACLS 藥理學規範：Midazolam 具有水溶性佳、肌肉吸收快的特性，在癲癇重積狀態尚未建立靜脈管路時，肌肉注射（IM 10 mg 或 0.2 mg/kg）為第一線實證首選途徑（RAMPART Trial）。"
    },
    "113-9": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "升壓藥/強心藥輸液滴速計算 (Epinephrine 1 mg in 250 mL D5W → 濃度 = 1000 μg / 250 mL = 4 μg/mL)",
            "計算每分鐘所需劑量：體重 60 kg × 0.5 μg/kg/min = 30 μg/min",
            "換算每分鐘所需毫升數：30 μg/min ÷ 4 μg/mL = 7.5 mL/min",
            "換算標準輸液套管 (Macro-drip 1 mL = 20 滴 gtt)：7.5 mL/min × 20 gtt/mL = 150 滴/每分鐘"
        ],
        "key_triggers": ["60 公斤", "Epinephrine 1mg in 250 ml D5W (濃度 4 μg/ml)", "0.5 μg/kg/min", "標準輸液套管 (20 滴/mL) = 150 滴/分"],
        "confusion_trap": "• 醫囑滴速計算三大易錯點：\n• 1. 單位換算錯誤：1 mg = 1,000 μg（微克），泡在 250 mL 中代表每 1 mL 含 4 μg。\n• 2. 輸液套管係數混淆：台灣 EMT-P 國考稱「標準輸液套管（普通套管 IV set）」預設為 **1 mL = 20 滴（gtt）**；若題目寫「精密輸液套管（Micro-drip / Buretrol）」才是 **1 mL = 60 滴**。本題 7.5 mL/min × 20 gtt/mL = 150 滴/分。",
        "guideline_check": "• 補充臨床提醒：ACLS 針對心搏過緩或復甦後低血壓之成人 Epinephrine 泡法常為 2~10 μg/min（或 0.1~0.5 μg/kg/min），考場遇到計算題務必依題幹給定的目標劑量逐步驗算。"
    },
    "113-10": {
        "category": "核心藥物與5H5T",
        "is_disputed": True,
        "algorithm_path": [
            "危急或 OHCA 病人無法立即建立周邊靜脈管路 (IV)",
            "建立骨內注射管路 (IO：成人常用脛骨近端、肱骨近端、脛骨遠端)",
            "給藥前衝管關鍵：完成穿刺回抽確認後，必須先以 5~10 mL (成人) 生理食鹽水快速推注 (Flush) 撐開骨髓腔纖維網，才能確保後續輸液與急救藥物順暢進入中央循環"
        ],
        "key_triggers": ["成人骨內注射 (IO)", "腎上腺素、阿托品及碳酸氫鈉", "沖洗留置針需 5~10 mL (1~2 mL 不足)"],
        "confusion_trap": "• 本題官方公告「A 或 D 皆給分」之爭議題解析：\n• 1. 為何 (A) 不正確？在「成人」骨內注射中，股骨遠端（Distal femur）因成人大腿肌肉與軟組織極厚、骨皮質堅硬，僅適用於「嬰幼兒與兒童」，不建議作為成人 IO 注射點。\n• 2. 為何 (D) 也不正確？IO 穿刺針置入骨髓腔後，必須先以「5~10 mL 生理食鹽水」強力快速推注沖開骨髓腔（No flush = No flow），對清醒病人還需先打 2% Lidocaine 止痛；選項 (D) 寫「僅給 1~2 mL」在成人骨髓腔內完全不足以撐開通道！",
        "guideline_check": "• 符合 AHA 2020/2025 ACLS 給藥途徑指引：所有能從 IV 給予的 ACLS 急救藥物（Epinephrine、Amiodarone、Lidocaine、Atropine、Sodium bicarbonate）皆可以相同劑量由 IO 給予；惟最新 AHA 指引強調「優先嘗試建立 IV，若 IV 嘗試失敗或不可行時再立即使用 IO（Class 2a）」。"
    },
    "113-14": {
        "category": "心搏過速",
        "is_disputed": True,
        "algorithm_path": [
            "快速心律不整之電生理機轉分類",
            "自律性增加 (Enhanced automaticity) / 觸發活動 (Triggered activity) vs 再迴旋機轉 (Re-entry)",
            "心臟存在額外傳導路徑 (Accessory pathway，如 AVRT) 或房室結雙路徑 (AVNRT) → 典型陣發性上心室頻脈 (PSVT)"
        ],
        "key_triggers": ["額外的傳導路徑", "再迴旋異常 (Re-entrant)", "陣發性上心室頻脈 (PSVT)"],
        "confusion_trap": "• 本題當年度因題幹文字結合兩個概念而開放「B、C、D 皆給分」：\n• 1. 原命題標準答案為 (B) PSVT：因為題幹明確寫出「由於心臟存在『額外的傳導路徑（Accessory pathway）』導致再迴旋」，這是 WPW 症候群引發 PSVT（AVRT）最標準的定義。\n• 2. 為何申訴後 (C) 心房顫動與 (D) 心室顫動也給分？因為在廣義心電生理學中，AF 與 VF 的維持機轉同樣涉及心房或心室肌內部的「多發性微小再迴旋波（Multiple wavelet re-entry）」，但唯有 (A) 多發性心房心搏過速（MAT，常見於嚴重 COPD）純粹是由心房內多個異位點「自律性增高（Automaticity）」所致，絕非再迴旋。",
        "guideline_check": "• 符合 ACLS 電生理機轉：因為 PSVT 屬於房室結參與之「再迴旋（Re-entry）」心律，所以使用迷走神經刺激術或 Adenosine 暫時阻斷房室結傳導，就能一舉打斷迴旋圈而終止 PSVT！"
    },
    "113-22": {
        "category": "ROSC照護",
        "algorithm_path": [
            "30 歲男性運動中目擊倒地 (可電擊心律 OHCA) → 經 CPR、2 次去顫電擊、Epinephrine、Amiodarone 後達成 ROSC",
            "ROSC 復甦後照護：1. 病人昏迷 (瞳孔對光無反應) 啟動目標體溫管理 (TTM) 保護腦部 → 2. 追查年輕人猝死原因 (急性心肌炎、肥厚性心肌病變、AMI) → 3. 若持續心因性休克或再發停止需上 ECMO，必須選擇同時支持心肺循環的「V-A ECMO」"
        ],
        "key_triggers": ["ROSC", "目標體溫管理 (TTM)", "葉克膜 (ECMO)", "V-V ECMO vs V-A ECMO"],
        "confusion_trap": "• 選項 (D) 為必考 ECMO 模式陷阱：\n• 1. **V-V ECMO（靜脈-靜脈）**：抽靜脈血氧合後打回靜脈，**僅能取代肺臟氣體交換功能，完全沒有支撐心臟輸出與血壓的作用**，僅適用於嚴重 ARDS / 呼吸衰竭且心功能正常者。\n• 2. **V-A ECMO（靜脈-動脈）**：抽靜脈血氧合後直接打入動脈系統，能**同時取代心臟泵血與肺臟氧合功能**，因此在心搏停止（ECPR）、心因性休克或復甦後心衰竭時，**絕對首選 V-A ECMO**！",
        "guideline_check": "• 符合 AHA 2020/2025 復甦後照護與 ECPR 指引：ECPR 定義即為採用 V-A ECMO 進行體外心肺復甦。"
    },
    "113-23": {
        "category": "心搏停止",
        "is_disputed": True,
        "algorithm_path": [
            "評估 OHCA 病患是否符合啟動葉克膜復甦 (ECPR) 收案條件",
            "典型高存活效益條件：年齡較輕 (< 65~70 歲)、目擊倒地 (Witnessed arrest)、有旁觀者立即 CPR (Bystander CPR)、初始心律為可電擊心律 (VF/pVT)、頑固性心搏停止無法達成持續 ROSC"
        ],
        "key_triggers": ["葉克膜復甦 (ECPR)", "目擊倒下", "可電擊心律", "旁觀者 CPR", "自發性血循恢復 (ROSC)"],
        "confusion_trap": "• 為何原答案為 (D) 且最終送分？\n• 1. 原命題邏輯：如果病人在到院前已經順利達成「持續性自發性血循恢復（Sustained ROSC）」且血行動力學穩定，就不需要執行「ECPR（在心肺停止壓胸狀態下緊急置放葉克膜）」。\n• 2. 申訴送分原因：在臨床真實世界與台灣 ECPR 資料庫分析中，「到院前曾出現『短暫/間歇性 ROSC（Intermittent ROSC）』隨後又再度心跳停止」的病人，代表其心肌與腦部曾獲得灌流、尚未完全壞死，反而常是臨床醫師積極啟動 ECPR 且預後較佳的族群！題幹未區分「持續穩定 ROSC」或「短暫間歇 ROSC」故予以送分。",
        "guideline_check": "• 符合 AHA ACLS ECPR 實證共識：ECPR 的黃金適應症為「目擊倒地 + 旁觀者 CPR + 初始可電擊心律（VF/pVT）+ 傳統 ACLS 急救 10~20 分鐘仍無法維持穩定 ROSC 之可逆病因患者」。"
    },
    "113-54": {
        "category": "ACS與12導程",
        "image": "images/113-54.png",
        "algorithm_path": [
            "判讀題附 12 導程心電圖：Lead II, III, aVF 出現明顯 ST 段上升 (且 Lead III 上升幅度 > Lead II)，Lead I, aVL 出現鏡像 ST 段壓低 → 典型下壁 STEMI (右冠狀動脈 RCA 阻塞)",
            "高度懷疑合併右心室心肌梗塞 (RVMI) → 應加做右側胸前導程 (V4R ST 段上升 ≥ 1 mm 具高度特異性)",
            "到院前處置禁忌：在排除右心室梗塞前，嚴禁給予舌下硝化甘油 (NTG) 以免引發嚴重低血壓"
        ],
        "key_triggers": ["12 導程心電圖判讀：II, III, aVF ST 段上升 (下壁 STEMI)", "V4R 的 ST 節段上升表示右心室心肌梗塞", "禁用 NTG"],
        "confusion_trap": "• 選項 (A) 致命陷阱：從心電圖可見標準的下壁 STEMI（II, III, aVF ST 段上升），且 Lead III ST 上升大於 Lead II、伴隨 V1 ST 微升，強烈暗示右冠狀動脈近端阻塞合併「右心室心肌梗塞」，此時給予舌下 NTG 會導致前負荷崩潰與嚴重休克！\n• 選項 (B) 為正確診斷關鍵：加做右側心電圖時，「V4R 導程 ST 段上升」是診斷右心室心肌梗塞最敏感且特異的指標。\n• 選項 (C) 陷阱：轉送過程隨時可能爆發致命性 VF/VT，必須全程連接心電圖監視器與去顫器。\n• 選項 (D) 陷阱：懷孕屬於使用血栓溶解劑（tPA）的「相對禁忌症」而非絕對禁忌症。",
        "guideline_check": "• 符合 AHA 2020/2025 ACS 指引：所有下壁 STEMI 病患皆應評估是否合併右心室梗塞（加做 V4R），並避免使用硝酸鹽類（NTG）、嗎啡及利尿劑等會降低前負荷之藥物。"
    },
    "113-55": {
        "category": "心搏停止",
        "algorithm_path": [
            "ACLS 四大核心情境綜合檢核",
            "情境 A (骨折術後突發無脈搏 + 監視器呈現窄波頻脈 = 肺栓塞引發 PEA) → 立即 CPR + 儘速給予 Epinephrine 1 mg IVP",
            "情境 B (目擊心室顫動 VF) → 應立即去顫電擊 (Defibrillation)，電擊 3 次無效後才給予 Amiodarone 300 mg IVP",
            "情境 C (完全房室傳導阻滯 Complete AVB 合併休克 78/42mmHg) → 準備經皮心臟節律器 (TCP)",
            "情境 D (洗腎病患高血鉀致寬 QRS 嚴重緩脈休克) → 給予 Atropine 1 mg + Calcium gluconate 穩定心肌 + Sodium bicarbonate"
        ],
        "key_triggers": ["ACLS 急救流程", "心室顫動 (VF)", "Amiodarone 300 mg 給藥時機", "去顫電擊優先順序"],
        "confusion_trap": "• 選項 (B) 犯了 ACLS 可電擊心律最嚴重的順序錯誤：\n• 1. 當監視器確認為心室顫動（VF）時，若電擊器已在旁，首要救命處置是「立即去顫電擊（雙相波 120~200J）」，絕不可延遲電擊！\n• 2. **Amiodarone 300 mg IVP 的給藥時機是在「第 3 次去顫電擊之後」**（第 1 次電擊 → 2 分鐘 CPR → 第 2 次電擊 → 2 分鐘 CPR + Epinephrine 1 mg → 第 3 次電擊 → 2 分鐘 CPR + Amiodarone 300 mg），絕對不會在第一次電擊前就先推 Amiodarone！",
        "guideline_check": "• 符合 AHA 2020/2025 ACLS 心搏停止演算法：\n• 1. 可電擊心律（VF/pVT）：電擊第 1 次 → CPR 2 min → 電擊第 2 次 → CPR 2 min + **Epinephrine 1 mg** → 電擊第 3 次 → CPR 2 min + **Amiodarone 300 mg（或 Lidocaine 1~1.5 mg/kg）**。\n• 2. 不可電擊心律（PEA/Asystole）：立即 CPR + **儘速給予 Epinephrine 1 mg**。"
    },
    "113-56": {
        "category": "ACS與12導程",
        "image": "images/113-56.png",
        "algorithm_path": [
            "60 歲男性典型缺血性胸痛冒冷汗",
            "判讀題附 12 導程心電圖：Lead I, aVL 出現明顯 ST 段上升 (High lateral)，且 Lead II, III, aVF 出現鏡像 ST 段壓低",
            "解剖定位：Lead I, aVL (以及 V5, V6) 代表左心室側壁 → 診斷為側壁心肌梗塞 (Lateral wall STEMI)"
        ],
        "key_triggers": ["胸痛及冒汗", "12 導程心電圖：Lead I, aVL ST 段上升，II, III, aVF 鏡像壓低", "側壁心肌梗塞 (Lateral STEMI)"],
        "confusion_trap": "• 看圖判讀最常見的「鏡像變化誤判」：許多考生第一眼看到下壁導程（III, aVF）波形有很大變化，沒看清楚它是「ST 段往下壓低（Reciprocal depression）」，而真正「ST 段往上升高」的是左上角的 **Lead I 與 aVL**！\n• 導程配對複習：I, aVL 為高側壁（High lateral，常由左迴旋支 LCx 或左前降支對角支 Diagonal branch 供應）；II, III, aVF 才是下壁；V1, V2 為中隔區；V3, V4 為前壁。",
        "guideline_check": "• 符合 AHA ACLS 12 導程心電圖 STEMI 判讀準則：在讀 12 導程心電圖時，若看到下壁（II, III, aVF）ST 段壓低，務必立刻抬頭看高側壁（I, aVL）是否有 ST 段上升；反之亦然。"
    },
    "113-100": {
        "category": "心搏過緩",
        "is_disputed": True,
        "algorithm_path": [
            "有症狀之心搏過緩 (HR < 50 bpm 且 BP 60/40mmHg 不穩定)",
            "ACLS 緩脈流程第一線雖為 Atropine 1 mg IVP (2020 更新劑量)",
            "特殊解剖定位例外：Mobitz type II 二度二型或三度 AV block (病灶位於希氏束以下 Infranodal)",
            "Atropine 作用於房室結 (AV node) 迷走神經，對 Infranodal block 通常無效，應優先使用 TCP 或 β-adrenergic 升壓藥物 (Dopamine / Epinephrine)"
        ],
        "key_triggers": ["Mobitz type II AV block", "下壁 STEMI (II, III, aVF)", "Atropine 1mg IVP", "寬且規則 QRS 穩定頻脈考慮 Adenosine"],
        "confusion_trap": "• 本題為「高階指引細節 vs 流程圖表面直覺」之經典爭議題（官方公告送分）：\n• 1. 原命題選 (B) 最不適當之理由：「Mobitz Type II AV block」阻滯位置在房室結以下（希氏束-普金氏系統），Atropine 難以發揮效果，不應依賴 Atropine 而延誤 TCP 或升壓藥。\n• 2. 考生申訴送分之理由：(1) 下壁心肌梗塞（RCA 阻塞）引起的房室傳導阻滯多數位於 AV node 層級（對 Atropine 有反應）；(2) ACLS 緩脈流程圖仍將 Atropine 1mg 列為所有症狀性緩脈的第一線嘗試（只要不延誤 TCP）。\n• 3. 強烈誘答選項 (D)：「寬且規則的穩定頻脈」給 Adenosine？注意！AHA 指引明確記載，若為「寬且規則（Regular monomorphic wide-complex tachycardia）」且血行動力學穩定，懷疑為 SVT 伴隨差異性傳導時，可考慮給予 Adenosine 6mg IVP 作鑑別與治療（若為不規則寬波則絕對禁用 Adenosine！）。",
        "guideline_check": "• AHA 2020/2025 ACLS 指引重點：\n• 1. 心搏過緩 Atropine 初始劑量自 2020 年起由舊版 0.5 mg 調升為「1 mg IVP」，每 3~5 分鐘可重複，最大總劑量 3 mg。\n• 2. 二度二型（Mobitz II）與三度 AV block 切勿過度依賴 Atropine，應立即準備經皮心臟節律器（TCP）或給予 Epinephrine（2~10 mcg/min）/ Dopamine（5~20 mcg/kg/min）。"
    },

    # ==================== 112 年度 ====================
    "112-9": {
        "category": "ROSC照護",
        "image": "images/112-9.png",
        "algorithm_path": [
            "氣管內管插管後持續監測波形定量潮氣末二氧化碳 (Waveform Capnography, EtCO2) 與超音波",
            "狀況排查 (DOPE 口訣)：Displacement (管路滑脫/入食道)、Obstruction (阻塞)、Pneumothorax (氣胸)、Equipment (氣囊破漏/設備故障)",
            "超音波氣道確認：正常氣管內插管僅見單一氣管影；若出現「雙氣管徵象 (Double tract / Double trachea sign)」代表管路誤入食道！"
        ],
        "key_triggers": ["插管後評估照護", "EtCO2 波形圖儀", "Double trachea sign (雙氣管徵象 = 誤入食道)", "DOPE 口訣"],
        "confusion_trap": "• 選項 (B) 是黑白顛倒的致命陷阱：在頸部氣道超音波橫切面下，食道位於氣管後外側，平時塌陷看不見；一旦氣管內管「誤入食道」，充滿空氣的管路會在原本氣管旁邊形成第二個高回音圓弧影與殘響假影，稱為 **Double trachea sign（雙氣管徵象）**，代表**插管位置錯誤（在食道內）**，必須立即拔除重插！\n• 選項 (A) 圖一可見原本正常的箱型波突然驟降趨近於 0，代表管路滑脫或呼吸器管路脫落。\n• 選項 (D) 圖二可見吐氣高原期無法維持、呈現鋸齒狀或提前下滑，代表氣管內管氣囊（Cuff）破損漏氣。",
        "guideline_check": "• 符合 AHA ACLS 進階呼吸道確認指引：確認氣管內管位置最準確的黃金標準為「連續波形潮氣末二氧化碳監測（Continuous waveform capnography）」，若具備經驗亦可輔以重點式超音波（Airway ultrasound）確認。"
    },
    "112-12": {
        "category": "ROSC照護",
        "algorithm_path": [
            "定量潮氣末二氧化碳 (EtCO2) 臨床監測",
            "正常生理數值範圍：35~45 mmHg",
            "CPR 期間應用：1. 確認氣管內管位置 → 2. 監測壓胸品質 (目標 ≥ 10~20 mmHg) → 3. 偵測 ROSC (EtCO2 瞬間驟升至 ≥ 40 mmHg)",
            "代謝與循環影響：低體溫/休克/肺栓塞時 CO2 產生或回流減少 → EtCO2 偏低；換氣不足時 → EtCO2 偏高"
        ],
        "key_triggers": ["潮氣末二氧化碳分壓值 (EtCO2)", "正常值為 35~45 mmHg", "評估 CPR 按壓品質與確認 ROSC"],
        "confusion_trap": "• 選項 (A) 數字陷阱：正常人的 EtCO2（以及動脈血 PaCO2）標準範圍是 **35~45 mmHg**；選項寫成「45~50 mmHg」已經屬於輕度高碳酸血症（Hypercapnia / 換氣不足）！\n• 選項 (C) 機轉理解：嚴重低體溫病人因全身新陳代謝率大幅降低、CO2 產量減少，因此測得的 EtCO2 會偏低。",
        "guideline_check": "• 符合 AHA 2020/2025 ACLS 指引：ROSC 後應調整通氣速率（約每 6 秒 1 次，即 10 次/分）以維持 PaCO2 35~45 mmHg 或 EtCO2 30~40 mmHg。"
    },
    "112-22": {
        "category": "心搏停止",
        "algorithm_path": [
            "目擊成人 OHCA (初始心律為 VF / 無脈性 VT)",
            "生命之鏈：立即求救 + 旁觀者立即施行高品質 CPR + 儘速使用 AED 去顫電擊",
            "存活率時間曲線：若無旁觀者 CPR，每延遲 1 分鐘去顫存活率下降 7%~10%；若有旁觀者 CPR，每延遲 1 分鐘去顫存活率僅下降 3%~4%"
        ],
        "key_triggers": ["心室顫動或無脈性心室頻脈", "目擊者施行 CPR", "存活率每分鐘下降 3~4%"],
        "confusion_trap": "• 四個選項全部在考經典復甦數據的精準度：\n• 1. 選項 (A) 錯在數字誇大：未做 CPR 時，每延遲 1 分鐘去顫，存活率下降為 **7%~10%**（而非 17~20%）。\n• 2. 選項 (B) 正確：若目擊者立即實施 CPR，可將每分鐘存活率下降幅度減緩一半以上，降至每分鐘 **3%~4%**。\n• 3. 選項 (C) 錯在壓胸佔比（CCF, Chest Compression Fraction）：高品質 CPR 要求減少中斷，胸部按壓時間佔比必須達 **60% 以上（理想目標 > 80%）**，而非 50%！\n• 4. 選項 (D) 錯在腦缺氧時間：心跳停止後 **4~6 分鐘**腦細胞就會開始受到不可逆的缺氧損傷，10 分鐘後則幾乎造成嚴重腦死。",
        "guideline_check": "• 符合 AHA 2020/2025 BLS/ACLS 核心指標：高品質 CPR 五大要素為「用力壓（5~6 公分）、快快壓（100~120 次/分）、胸回彈、莫中斷（中斷 < 10 秒，CCF > 60%~80%）、避免過度通氣」。"
    },
    "112-23": {
        "category": "心搏停止",
        "algorithm_path": [
            "體外膜氧合維生系統 (ECMO) 生理機轉與適應症評估",
            "V-V ECMO：靜脈引流 → 氧合器 → 靜脈回輸 (僅提供氣體交換，適用純呼吸衰竭)",
            "V-A ECMO：靜脈引流 → 氧合器 → 動脈回輸 (提供全身循環灌流與氣體交換，適用心因性休克與 ECPR)"
        ],
        "key_triggers": ["葉克膜 (ECMO)", "V-V ECMO vs V-A ECMO", "禁忌症：顱內出血 72 小時內、不可逆腦損傷"],
        "confusion_trap": "• 選項 (A) 是非常細膩的生理機制陷阱：V-A ECMO 是藉由體外幫浦將血液逆行打入主動脈，藉此**「取代/分擔」衰竭心臟的泵血工作以維持全身器官組織灌流**，但它並不會直接「改善心臟本身的收縮功能（甚至因打入主動脈而增加左心室後負荷 Afterload）」！心臟本身收縮功能的恢復仍需靠治療根本病因（如 PCI 打通冠狀動脈）或心肌自然修復。",
        "guideline_check": "• 符合 ELSO 與 AHA ECPR 指引：ECMO 執行期間需使用 Heparin 抗凝血，因此近期（72 小時內）顱內出血、無法控制的活動性大出血、或已出現不可逆嚴重腦損傷者均為禁忌症。"
    },
    "112-34": {
        "category": "心搏停止",
        "algorithm_path": [
            "鈍性胸部撞擊（如棒球、曲棍球直接擊中左前胸心前區）",
            "撞擊瞬間恰巧落在心電圖心室再極化「T 波上升支頂峰前 10~30 毫秒」之脆弱期 (Vulnerable period, R-on-T 概念)",
            "瞬間誘發心室顫動 (VF) 導致心搏停止 → 心臟震盪 (Commotio cordis)",
            "急救關鍵：立即 CPR 與儘速 AED 去顫電擊"
        ],
        "key_triggers": ["心臟震盪 (commotio cordis)", "最常見的心律是心室顫動 (VF)"],
        "confusion_trap": "• 選項 (A) 陷阱：創傷性主動脈剝離/破裂（減速傷）最常好發於「主動脈峽部（Aortic isthmus，即左鎖骨下動脈開口遠端、動脈韌帶附著處之降主動脈近端）」，而非升主動脈。\n• 選項 (B) 陷阱：鈍性氣管支氣管破裂最常發生於「隆突（Carina）周圍 2 公分內的主支氣管」，而非肺內細支氣管。\n• 選項 (D) 陷阱：創傷性窒息（Traumatic asphyxia）因上腔靜脈瞬間受壓逆流，是造成「壓迫位置以上（頭頸部、上胸、結膜）」呈現藍紫色發紺與出血點，而非壓迫位置以下。",
        "guideline_check": "• 符合 AHA BLS/ACLS 運動場猝死指引：心臟震盪（Commotio cordis）好發於青少年運動員，心臟本身無結構性病變，最常見致死心律為心室顫動（VF），3 分鐘內給予 AED 去顫可大幅提升存活率。"
    },
    "112-50": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "5H5T 可逆病因：肺動脈栓塞 (Pulmonary Embolism, PE)",
            "病理機轉：骨盆或下肢深部靜脈血栓 (DVT) 脫落 → 經下腔靜脈、右心房、右心室打入「肺動脈系統」造成阻塞 → V/Q 值暴增 (死腔通氣) 與急性右心衰竭",
            "心電圖表現：最常見為「竇性頻脈 (Sinus tachycardia)」，典型 S1Q3T3 僅見於少數嚴重右心負荷患者"
        ],
        "key_triggers": ["肺栓塞", "骨盆以及下肢靜脈系統為最常形成血栓的部位", "S1Q3T3 vs 竇性頻脈"],
        "confusion_trap": "• 選項 (A) 血管名稱陷阱：下肢靜脈血栓順著血流回右心後，堵住的是「肺動脈系統（Pulmonary artery）」，而非肺靜脈！\n• 選項 (C) 國考萬年陷阱（109-47 與 112-50 連考兩次）：肺栓塞病人心電圖**最常見的表現是「竇性頻脈（Sinus tachycardia）」**！雖然教科書常強調 `S1Q3T3`（Lead I 深 S 波、Lead III 病理 Q 波與 T 波倒置），但 `S1Q3T3` 特異性高卻不常見（僅佔約 10%~20%），絕非「最常見」表現！\n• 選項 (D) 藥物機轉陷阱：靜脈血栓（紅血栓，富含纖維蛋白）必須使用「抗凝血劑（Heparin / NOAC）或血栓溶解劑」，到院前給予抗血小板藥物（如 Aspirin）對肺栓塞並非標準治療。",
        "guideline_check": "• 符合急診醫學與 ACLS 肺栓塞診治共識：評估不明原因呼吸困難或 PEA 時，務必檢查雙下肢是否有不對稱腫脹（DVT 線索）及詢問近期手術/長期臥床病史。"
    },
    "112-56": {
        "category": "心搏過速",
        "image": "images/112-56.png",
        "algorithm_path": [
            "55 歲女性主訴心悸，無其他不適",
            "評估血行動力學：GCS 15 分、BP 121/70 mmHg → 血行動力學「穩定」",
            "判讀題附心電圖：規則、窄 QRS 波 (< 0.12 秒)、心率約 160~180 bpm、無明顯正常 P 波 → 陣發性心室上頻脈 (PSVT)",
            "穩定規則窄波頻脈處置步驟：1. 首選嘗試迷走神經刺激術 (Vagal maneuvers，如改良式 Valsalva maneuver) → 2. 若無效，給予 Adenosine 6 mg IV 快速推注 (Rapid IV push)"
        ],
        "key_triggers": ["血壓 121/70mmHg (穩定)", "心電圖：規則窄 QRS 波頻脈 (PSVT)", "迷走神經刺激術 (vagal maneuvers)", "Adenosine 必須快速推注"],
        "confusion_trap": "• 選項 (A) 給藥方式陷阱：看到 PSVT 就想選 Adenosine 6 mg，但仔細看選項 (A) 寫的是「緩慢推注」！Adenosine 半衰期極短（< 10 秒），緩慢推注完全無效，必須「極快速靜脈推注（1~3 秒內推完）並立即以 20 mL 生理食鹽水快速沖管」！\n• 選項 (B) 心律判讀錯誤：圖中 R-R 間距非常規則，並非不規則的心房顫動（Af）。\n• 選項 (D) 藥物選擇錯誤：穩定 PSVT 第一線為迷走神經刺激術與 Adenosine / 鈣離子通道阻斷劑（Verapamil/Diltiazem）/ 乙型阻斷劑，而非快速推注 Amiodarone。",
        "guideline_check": "• 符合 AHA 2020/2025 ACLS 有脈搏頻脈流程：穩定型規則窄 QRS 頻脈（PSVT）第一動永遠是「迷走神經刺激術（Class 1）」，臨床實證顯示「改良式伐氏操作（Modified Valsalva maneuver：吹氣用力後立即平躺並抬高雙腿 45 度 15 秒）」成功率最高。"
    },
    "112-57": {
        "category": "ACS與12導程",
        "image": "images/112-57.png",
        "algorithm_path": [
            "判讀題附 12 導程心電圖",
            "觀察各導程 ST 段變化：Lead I, aVL 出現明顯 ST 段上升，Lead III, aVF 出現鏡像 ST 段壓低，且胸前導極 V2~V4 為深 S 波 (可能合併 LBBB 或左心室肥厚，但肢體導程顯示高側壁 I, aVL 顯著 ST 上升)",
            "解剖位置對應：Lead I, aVL 對應左心室「側壁 (Lateral wall)」"
        ],
        "key_triggers": ["12 導程心電圖判讀", "Lead I, aVL ST 段上升，III, aVF 鏡像壓低", "側壁 (Lateral wall) 心肌梗塞"],
        "confusion_trap": "• 本題與 113-56 考完全相同的核心觀念（高側壁 STEMI）：\n• 許多考生看到 V1~V4 有明顯波形及 ST 段微揚（實為深 S 波之 Discordant ST change）就誤選 (A) 前壁；但關鍵在於肢體導程 **Lead I 與 aVL 有非常典型的拱背向上（Convex）ST 段上升，且下壁（III, aVF）出現明顯的鏡像 ST 段壓低**，這是標準的「高側壁心肌梗塞（High lateral MI，歸類於側壁 Lateral wall）」。",
        "guideline_check": "• 符合 AHA ACLS 12 導程心電圖判讀準則：Lead I 與 aVL 反應左心室高側壁（High lateral wall），常由左迴旋支（LCx）或左前降支的第一對角支（D1）阻塞所致。"
    },
    "112-58": {
        "category": "ACS與12導程",
        "image": "images/112-58.png",
        "algorithm_path": [
            "急性心肌梗塞 (STEMI) 心電圖隨缺血時間演進之四階段變化",
            "1. 超急性期 (數分鐘~數小時，圖 2)：T 波高聳對稱 (Hyperacute T wave)",
            "2. 急性期 (數小時，圖 3)：ST 段顯著上升 (ST elevation，與高尖 T 波融合呈墓碑狀)",
            "3. 亞急性期/近期 (數小時~數天，圖 1)：出現病理性 Q 波、ST 段仍上升但 T 波開始倒置 (T wave inversion)",
            "4. 陳舊期 (數週~數月後，圖 4)：ST 段回到基線、T 波恢復正向，但永久殘留深而寬的病理性 Q 波 (Old MI)"
        ],
        "key_triggers": ["心肌梗塞不同時期心電圖變化時序", "超急性 T 波 (圖2) → ST 段上升 (圖3) → Q 波出現與 T 波倒置 (圖1) → ST 回基線留 Q 波 (圖4)"],
        "confusion_trap": "• 易混淆點在於「圖 1」與「圖 3」的先後順序：\n• 圖 3 還沒有深的病理性 Q 波且 T 波仍為正向（急性損傷期）；圖 1 則已經長出明顯向下的 Q 波且 T 波已轉為倒置（壞死與亞急性演進期），因此必然是 **圖 2（超急性 T 波）→ 圖 3（ST 上升）→ 圖 1（Q 波 + T 波倒置）→ 圖 4（ST 回基線、留永久 Q 波）**，正確答案為 (D)。",
        "guideline_check": "• 符合 AHA ACS 心電圖演進學理：在心肌梗塞發作最初幾分鐘至 2 小時內，可能僅見「超急性高尖 T 波（Hyperacute T）」而尚未出現明顯 ST 段上升，此時應每隔 15~30 分鐘序列追蹤（Serial ECGs）！"
    },
    "112-59": {
        "category": "ACS與12導程",
        "algorithm_path": [
            "正常 12 導程心電圖波形與異常判讀基準",
            "P 波：右心房擴大 → P 波高尖 (> 2.5 mm, P pulmonale)；左心房擴大 → P 波寬大雙峰 (> 0.12 s, P mitrale)",
            "胸前導極正常 R 波遞增 (R-wave progression)：從 V1 到 V5/V6，R 波應逐漸變大、S 波應逐漸變小"
        ],
        "key_triggers": ["心電圖判讀", "胸前導極 R 波遞增 (R-wave progression)", "T 波反轉", "P pulmonale vs P mitrale"],
        "confusion_trap": "• 選項 (D) 將正常胸前導極的 **R 波遞增現象（Normal R-wave progression）** 完全寫反了！\n• 正常心室去極化電力向量是由右後上往「左前下」傳導，因此貼在右胸骨緣的 V1 主波向下（rS 型，R 波極小、S 波深），隨著導極往左心室側移動（V1 → V2 → V3 → V4 → V5），**R 波應該逐漸變大、S 波則逐漸變小**（通常在 V3~V4 轉換區 R/S 比約等於 1）。若 V1~V4 R 波沒有變大，稱為 R 波遞增不良（Poor R-wave progression，常見於前壁陳舊性心肌梗塞）。",
        "guideline_check": "• 符合標準 12 導程心電圖判讀原則。"
    },
    "112-77": {
        "category": "心搏停止",
        "algorithm_path": [
            "兒童與嬰兒院外心跳停止 (Pediatric OHCA)",
            "病因特性：多數源於漸進性呼吸衰竭或休克導致缺氧性心搏停止 (Asystole/PEA 居多，但約 5%~15% 仍為 VF/pVT)",
            "BLS/PALS 核心處置：雙人按壓通氣比 15:2、按壓深度為胸廓前後徑 1/3 (嬰兒約 4 cm、兒童約 5 cm)、儘速使用 AED (優先選用兒科衰減貼片，若無則用成人貼片)"
        ],
        "key_triggers": ["兒童與嬰兒 OHCA", "AED 使用原則", "雙人按壓通氣比 15:2", "按壓深度 5 公分"],
        "confusion_trap": "• 選項 (A) 是絕對錯誤的致命觀念：雖然嬰幼兒 OHCA 以呼吸性原因為主，但仍有一定比例為原發性心因性（如先天性心臟病、心肌炎、長 QT 症候群）或次發性 VF！**嬰兒與兒童發生 OHCA 時「絕對必須使用 AED 或去顫器分析心律」**（優先使用兒科能量衰減貼片；若現場僅有成人貼片，亦應直接使用成人貼片，切勿不貼）！",
        "guideline_check": "• 符合 AHA 2020/2025 PALS/BLS 指引：\n• 1. 嬰兒（< 1 歲）首選手動去顫器（2~4 J/kg）；若無手動去顫器，次選具備兒科能量衰減器之 AED；若皆無，則使用一般成人 AED（貼片不可互相接觸，可採前-後貼法 Anterior-Posterior）。\n• 2. 2020 PALS 更新提醒：兒童與嬰兒已建立進階呼吸道後，通氣速率已由舊版調升為「每 2~3 秒吹氣 1 次（每分鐘 20~30 次）」。"
    },
    "112-78": {
        "category": "核心藥物與5H5T",
        "is_disputed": True,
        "algorithm_path": [
            "嬰兒 OHCA 急救藥物劑量計算 (體重 2 kg)",
            "PALS Epinephrine 靜脈/骨內 (IV/IO) 標準劑量：0.01 mg/kg (使用 1:10,000 稀釋液，即 0.1 mL/kg)",
            "PALS Epinephrine 氣管內管 (ET) 標準劑量：0.1 mg/kg (使用 1:1,000 原液，即 0.1 mL/kg)"
        ],
        "key_triggers": ["嬰兒 (2 公斤) OHCA", "Epinephrine 劑量計算", "單人 vs 雙人壓胸通氣比"],
        "confusion_trap": "• 為何本題原答案為 (C) 最終卻公告「送分」？因為四個選項在嚴格兒科急救指引下全部都有瑕疵！\n• 1. 選項 (A) 錯在「單人」急救時，無論成人、兒童或嬰兒，按壓通氣比一律是 **30:2**（「雙人」施救兒童/嬰兒才是 15:2）。\n• 2. 選項 (B) 錯在 2 公斤嬰兒氣管內管置入深度（公式：體重 kg + 6 cm = 2 + 6 = **8 cm**，或內徑 × 3 = **9 cm**），12 cm 太深會單側插管！\n• 3. 選項 (C) 與 (D) 發生小數點計算錯誤：2 公斤嬰兒給予 IV/IO Epinephrine 劑量應為 `0.01 mg/kg × 2 kg = 0.02 mg`（相當於 1:10,000 抽 **0.2 mL**），出題老師把 **0.2 mL** 誤寫成 **0.2 mg**（足足超量 10 倍）！因此考生申訴後全題送分。",
        "guideline_check": "• 兒科/新生兒 Epinephrine 劑量必背防呆公式：\n• **IV / IO 途徑**：`0.01 mg/kg` = 抽 **1:10,000** 稀釋液 `0.1 mL/kg`。\n• **ET（氣管內管）途徑**：`0.1 mg/kg` = 抽 **1:1,000** 原液 `0.1 mL/kg`。"
    },
}

print(f"Part 1 定義完成，共 {len(ANNOTATIONS_PART1)} 題。")
