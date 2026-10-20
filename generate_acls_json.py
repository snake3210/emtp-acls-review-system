import os
import json
import sys
from collections import Counter

from build_part1 import ANNOTATIONS_PART1, IMAGE_IDS
from build_part2 import ANNOTATIONS_PART2

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(__file__)
ALL_QS_PATH = os.path.join(BASE_DIR, "all_emtp_108_114.json")
OUTPUT_JSON_PATH = os.path.join(BASE_DIR, "acls_questions.json")

# 補充高頻 5H5T (張力性氣胸針刺減壓、壓碎症候群/腫瘤溶解症候群致死性高血鉀、肺栓塞、EtCO2 與給藥途徑) 試題深度解析
ANNOTATIONS_PART3 = {
    "114-33": {
        "category": "心搏停止",
        "algorithm_path": [
            "專業人員執行 BLS / ACLS 心肺復甦術",
            "一般心因性猝死：採 C-A-B 順序 (先胸部按壓維持冠狀動脈與腦灌流)",
            "窒息性心搏停止 (Asphyxial cardiac arrest，如溺水與新生兒)：因缺氧為核心致死機轉，維持傳統 A-B-C 順序 (先暢通呼吸道並給予有效人工呼吸)"
        ],
        "key_triggers": ["基本救命術", "C-A-B 順序 vs A-B-C 順序", "溺水病人與新生兒"],
        "confusion_trap": "• 易混淆選項 (C) 藥物過量與 CO 中毒、或 (D) 雷擊與低體溫：雖然藥物過量（如鴉片類）與 CO 中毒也有缺氧問題，但在 AHA BLS 指引與台灣 EMT-P 標準教材中，明確規定**「溺水（Drowning）」与「新生兒急救（NRP）」**因屬於典型原發性窒息缺氧，仍建議優先執行 **A-B-C（先打開呼吸道並給予通氣）**！",
        "guideline_check": "• 符合 AHA 2020/2025 BLS & 溺水復甦指引：溺水患者因肺泡缺氧導致心搏停止，施救者一旦將患者移至安全處，應優先給予通氣（A-B-C），新生兒復甦亦以建立有效通氣為首要步驟。"
    },
    "114-71": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "腫瘤細胞快速崩解 (Tumor Lysis Syndrome, TLS) 或橫紋肌溶解症",
            "細胞內離子與代謝物大量釋入血液：鉀離子 (K+) 釋出 → 高血鉀症 (5H5T 致死性心律不整主因)；磷酸根 (PO4 3-) 釋出 → 高磷酸血症；核酸嘌呤代謝 → 高尿酸血症",
            "次發性電解質變化：高血磷與血液中游離鈣結合沉澱 (磷酸鈣) → 繼發性低血鈣症 (Hypocalcemia)"
        ],
        "key_triggers": ["腫瘤溶解症候群 (TLS)", "高尿酸血症", "高血鉀症 (5H5T)", "高磷酸血症", "低血鈣症"],
        "confusion_trap": "• 本題與壓碎症候群（113-44、109-29、108-62）完全共用同一個電解質記憶公式：\n• **「三高一低」：高鉀、高磷、高尿酸，唯有「血鈣是低的（低血鈣症）」**！\n• 考生最常在選項 (C) 中招，誤以為細胞破裂連鈣離子也一起變高——請切記：細胞內富含的是「鉀（K+）與磷（PO4 3-）」，當大量磷酸根釋出後，會把血液中的鈣離子抓走結合沉澱，反而造成嚴重的**低血鈣**（甚至延長 QT 波、誘發抽搐）！",
        "guideline_check": "• 符合 ACLS 5H5T（高血鉀 Hyperkalemia）與腫瘤急症照護準則：一旦出現高血鉀心電圖變化（高尖 T 波、QRS 變寬），首選應立即靜脈注射 Calcium chloride 或 Calcium gluconate 穩定心肌細胞膜（同時也能矯正低血鈣）。"
    },
    "113-11": {
        "category": "ROSC照護",
        "algorithm_path": [
            "潮氣末二氧化碳分壓 (EtCO2) 決定三要素：1. 細胞代謝產生 CO2 → 2. 心輸出量與肺血流運送 CO2 → 3. 肺泡通氣排出 CO2",
            "導致 EtCO2 下降的原因：代謝降低 (如低體溫)、肺灌流減少 (如休克、心搏停止、肺栓塞)、或過度換氣",
            "單純腦中風 (Stroke)：除非中風引發中樞性過度換氣，否則不會直接降低心輸出量或肺血流，故最不可能導致 EtCO2 下降"
        ],
        "key_triggers": ["潮氣末二氧化碳分壓值 (EtCO2) 下降", "體溫下降 (代謝減少)", "休克 / 肺栓塞 (肺灌流減少)", "中風最不可能"],
        "confusion_trap": "• 易混淆選項 (A) 體溫下降或 (D) 肺栓塞：\n• 1. **體溫下降（A）**：全身細胞新陳代謝率降低，產生的 CO2 減少，因此 EtCO2 會下降。\n• 2. **休克（B）與肺栓塞（D）**：右心室打去肺部的血流大幅減少（肺死腔增加、V/Q mismatch），CO2 無法交換到肺泡呼出，因此 EtCO2 會顯著下降！\n• 3. **腦中風（C）**：若呼吸變慢（腦幹受壓迫換氣不足）反而會使 EtCO2「上升」，因此中風最不可能直接造成 EtCO2 下降。",
        "guideline_check": "• 符合 AHA ACLS 生理監測觀念：當患者呼吸速率與潮氣量固定時，EtCO2 數值直接反映「心輸出量與肺部有效灌流（Cardiac Output & Pulmonary Perfusion）」。"
    },
    "113-37": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "高度懷疑張力性氣胸 (Tension Pneumothorax, 5H5T)",
            "院前針刺減壓 (Needle Decompression) 三大適應症：1. 嚴重呼吸窘迫或通氣困難 + 2. 單側呼吸音減弱或消失 + 3. 休克徵象 (SBP < 90 mmHg)",
            "解剖穿刺位置選擇：成人因前胸壁較厚，優先選擇患側「第五肋間、腋中線前緣 (或腋前線與腋中線之間)」；兒童仍維持「第二肋間鎖骨中線」"
        ],
        "key_triggers": ["針刺減壓", "成人較佳位置：患側第五肋間腋中線前側", "兒童仍為第二肋間鎖骨中線"],
        "confusion_trap": "• 四個選項全面考出 ATLS 第十版 / PHTLS 針刺減壓四大陷阱：\n• 1. 選項 (A) 陷阱：院前針刺減壓三大要件**「不包含」頸靜脈怒張與氣管偏移**（因為外傷病患常合併低血容積休克而看不到頸靜脈怒張，且氣管偏移是極晚期徵象，請對照 111-47）！\n• 2. 選項 (C) 陷阱：針刺減壓只是將張力性氣胸轉為單純氣胸的「暫時性救命處置」，**確切治療（Definitive treatment）是「胸管置入術（Chest tube thoracostomy）」**！\n• 3. 選項 (D) 陷阱：**兒童（小兒）**胸壁較薄，ATLS 第十版仍建議維持傳統的**「患側第二肋間鎖骨中線」**，僅成人改以第五肋間腋中線前側為優先！",
        "guideline_check": "• 完全符合 ATLS 10th Edition 與 AHA ACLS 5H5T（張力性氣胸）處置規範。"
    },
    "113-44": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "雙下肢壓砸傷 > 4 小時 → 高度風險發生壓碎症候群 (Crush Syndrome) 與再灌流致死性高血鉀 (5H5T)",
            "脫困前處置：立即建立靜脈管路，給予大量不含鉀之生理食鹽水 (成人 1,000~1,500 mL/hr)",
            "脫困瞬間再灌流風險：1. 血液湧入缺血擴張之患肢導致低血壓休克；2. 壞死肌肉釋出大量鉀、磷、肌紅蛋白與乳酸 → 代謝性酸中毒、高血鉀、高血磷、低血鈣"
        ],
        "key_triggers": ["瓦礫堆壓傷四小時 (壓碎症候群)", "脫困前給予大量生理食鹽水 (1000 mL/hr)", "再灌流導致高血鉀、高血磷、「低血鈣」"],
        "confusion_trap": "• 與 114-71、109-29、108-62 為同一高頻考題模板！\n• 選項 (C) 把「低血鈣」偷換成「高血鈣」——再灌流後大量磷酸根釋出會結合血液中的鈣離子，再加上缺血受損的肌肉細胞膜鈣離子通道失調使鈣離子流入受損肌肉細胞內，必定造成**「低血鈣（Hypocalcemia）」**！",
        "guideline_check": "• 符合災難醫學與 ACLS 5H5T（高血鉀與低血容積）預防指引：壓碎傷患者務必在「移開重物（脫困）之前」就開始大量輸注生理食鹽水（禁用含鉀之乳酸林格氏液 Lactated Ringer's），並密切監測心電圖防範高血鉀致死性心律不整。"
    },
    "113-53": {
        "category": "ACS與12導程",
        "algorithm_path": [
            "54 歲男性車禍胸痛、呼吸短促、冒冷汗、低血壓 (85/40 mmHg)",
            "外傷性休克與內科胸痛鑑別：e-FAST 超音波可快速床邊鑑別張力性氣胸 vs 大量血胸 vs 心包膜填塞",
            "用藥與判讀禁忌：正常 12 導程心電圖無法完全排除 AMI；且當血壓 85/40 mmHg (< 90 mmHg) 時絕對禁用 NTG"
        ],
        "key_triggers": ["車禍胸痛", "血壓 85/40mmHg", "e-FAST 協助鑑別診斷氣胸與血胸", "SBP < 90 mmHg 禁用 NTG"],
        "confusion_trap": "• 本題同時結合外傷 5H5T 與 ACS 12 導程兩大陷阱：\n• 1. 選項 (A) 陷阱：約有半數急性冠心症（如 NSTEMI 或超早期心肌梗塞）第一張 12 導程心電圖可能無特異性變化，因此**不能單憑一張 12 導程心電圖就完全排除 AMI**。\n• 2. 選項 (B) 雙重致命禁忌：第一，病人目前血壓僅 **85/40 mmHg（收縮壓 < 90 mmHg）**，為 NTG 絕對禁忌症；第二，Lead II, III, aVF ST 段上升代表「下壁心肌梗塞」，常合併右心室梗塞，未排除前亦禁用 NTG！\n• 3. 選項 (D) 陷阱：當外傷患者同時合併低血容積（出血）時，即使有嚴重張力性氣胸或心包膜填塞，也**可能不會出現頸靜脈怒張**！",
        "guideline_check": "• 符合 AHA ACLS 與 ATLS 指引：針對低血壓與胸痛患者，重點式超音波（e-FAST / POCUS）是快速鑑別氣胸（Lung sliding 消失）、血胸與心包膜填塞最有效工具。"
    },
    "112-35": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "開放性氣胸 (Open Pneumothorax / 吸吮性胸部傷口) 貼上三邊封閉敷料 (Three-sided occlusive dressing)",
            "送醫途中突發意識改變、呼吸急促 → 高度懷疑敷料被血塊黏住或失效，轉變為「張力性氣胸 (Tension Pneumothorax, 5H5T)」",
            "立即處置：先掀開/移除單邊敷料讓氣體排出減壓，若仍未改善則於患側第五肋間腋中線前側執行針刺減壓 (絕對不可用填塞止血敷料把胸壁洞口塞死)"
        ],
        "key_triggers": ["右胸中彈開放性傷口", "塑膠包裝貼三邊覆蓋後突發意識變化與呼吸急促", "轉變為張力性氣胸", "絕對不可改用填塞止血敷料"],
        "confusion_trap": "• 選項 (C) 為致命錯誤處置：胸部穿透傷貼上三邊敷料後若病情惡化，最常見原因是三邊敷料失效變成全封閉，導致空氣只進不出形成**「張力性氣胸」**！此時應立即「掀開敷料讓胸腔高壓氣體洩出」，若改用急救填塞止血敷料（Wound packing）把傷口塞死，不僅無法止住胸腔內出血，更會讓張力性氣胸瞬間惡化致死！",
        "guideline_check": "• 符合 PHTLS / ATLS 與 ACLS 5H5T 指引：軀幹（胸腔、腹腔）穿透傷嚴禁執行傷口內填塞止血（Wound packing 僅限用於四肢與交界處 Junctional 大出血）。"
    },
    "111-33": {
        "category": "核心藥物與5H5T",
        "is_disputed": True,
        "algorithm_path": [
            "胸部創傷與張力性氣胸 (5H5T) 解剖生理評估",
            "小兒胸壁特性：兒童肋骨軟骨比例高、彈性極佳，遭受鈍傷時外力直接傳導至肺實質造成肺挫傷，反而「較少」發生肋骨骨折 (一旦骨折代表承受極高能量)",
            "成人針刺減壓位置比較：第五肋間腋中線前緣 (胸壁較薄) vs 第二肋間鎖骨中線"
        ],
        "key_triggers": ["胸部創傷", "兒童肋骨彈性大較不易骨折", "張力性氣胸針刺減壓位置 (第五肋間 vs 第二肋間)"],
        "confusion_trap": "• 【官方多解爭議題（A 或 C 皆給分）】：\n• 1. **原命題正解 (A)**：兒童骨骼尚未完全鈣化、順應性（彈性）極高，遭遇胸部鈍傷時，**比成人「更不容易」發生肋骨骨折**（常表現為無肋骨骨折的嚴重肺挫傷），故 (A) 敘述明顯錯誤。\n• 2. **申訴爭點 (C)**：ATLS 第十版建議成人針刺減壓位置為「第五肋間、**腋中線稍前方（Anterior to the midaxillary line）**」，而選項 (C) 寫成「腋前線（Anterior axillary line）」，因字面上與部分教材翻譯略有出入，故官方最終判定 A 或 C 均給分。",
        "guideline_check": "• 符合 ATLS 10th Edition：成人針刺減壓因為前胸壁（第二肋間鎖骨中線）脂肪與胸大肌較厚，長針頭失敗率較高，故改以側胸壁「第五肋間、腋中線前緣（或第四/五肋間腋前線至腋中線間）」為首選。"
    },
    "111-44": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "右側張力性氣胸經針刺減壓與胸管置入後生命徵象改善",
            "5 分鐘後突發再度呼吸困難、血壓下降 (病情急性惡化)",
            "外傷與急救黃金準則：一旦患者生命徵象再次不穩定，應立即回到「初級評估 (Primary Survey: ABCDE)」從頭檢視呼吸道、呼吸音與管路是否滑脫/阻塞 (DOPE)"
        ],
        "key_triggers": ["張力性氣胸胸管置入後再度呼吸困難、血壓下降", "生命徵象不穩定應重新進行初級評估"],
        "confusion_trap": "• 本題在 **108-56、109-41、111-44** 三年一字不漏重複出現（連選項都幾乎一樣），是台灣 EMT-P 甄試最經典的「秒殺考古題」！\n• 誘答陷阱 (B)/(D)：考生看到氣胸病人胸管置入後又喘、血壓掉，很容易直覺選 (B) 再戳一針減壓或 (D) 再插第二根胸管；但急救核心邏輯是**「每當病人生命徵象發生改變或惡化時，永遠先退回初級評估（Primary Survey ABCDE）」**，更何況推去排電腦斷層（C）對不穩定休克病人更是大忌！",
        "guideline_check": "• 符合 ATLS / PHTLS 初級評估再評估（Re-evaluation）原則。"
    },
    "111-47": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "院前高度懷疑張力性氣胸 (Tension Pneumothorax)",
            "確認執行針刺減壓 (Needle Decompression) 之三大必要條件：",
            "要件 1：嚴重呼吸窘迫或通氣困難 (Bag-valve-mask 捏球阻力極大)",
            "要件 2：患側呼吸音明顯減弱或消失",
            "要件 3：代償失調之休克表現 (成人收縮壓 SBP < 90 mmHg)"
        ],
        "key_triggers": ["張力性氣胸", "針刺減壓的三個要件", "不包括：意識不清到對疼痛無反應"],
        "confusion_trap": "• 考生常將「意識狀態（AVPU 之 P/U）」誤認為針刺減壓的適應症條件之一。\n• 請牢記台灣《高級救護技術員救護處置指引》針刺減壓三大要件口訣：**「一喘（嚴重呼吸窘迫或通氣困難）、二無音（患側呼吸音變小或聽不到）、三休克（收縮壓 < 90 mmHg）」**！不需要等到病人昏迷對痛無反應（選項 A）才執行減壓！",
        "guideline_check": "• 完全符合我國衛福部與各縣市消防局《EMTP 預立醫療流程—張力性氣胸針刺減壓》三大適應症規範。"
    },
    "110-19": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "48 歲男性突發呼吸喘、竇性頻脈 (HR 120 bpm)、主訴腳腫",
            "懷疑急性肺動脈栓塞 (Pulmonary Embolism, PE — 5H5T 之 Thrombosis, pulmonary)",
            "尋找血栓來源：約 70%~80% 肺栓塞之血栓源自下肢深部靜脈栓塞 (DVT)",
            "DVT 典型視觸診徵象：單側下肢不對稱水腫、腫脹、膚色發紅且局部皮溫升高 (溫熱)、小腿壓痛"
        ],
        "key_triggers": ["腳腫、呼吸喘、心跳 120 下/分", "肺栓塞 (Pulmonary Embolism)", "深部靜脈栓塞 (DVT)：單側肢體腫脹、肢體溫熱"],
        "confusion_trap": "• 易混淆選項剖析：\n• 1. **選項 (A) 單側紅腫合併水泡、劇痛**：這是壞死性筋膜炎（Necrotizing fasciitis）或嚴重蜂窩性組織炎的表現。\n• 2. **選項 (B) 單側肢體腫脹、肢體溫熱**：這是標準的**下肢深部靜脈血栓（DVT）**表現！因單側靜脈回流受阻導致鬱血腫脹與發炎溫熱，血栓脫落順流回右心打入肺動脈即造成**急性肺栓塞（5H5T）**！\n• 3. **選項 (C)/(D) 脈搏消失、網狀青斑**：這是急性「動脈」阻塞（5P 徵象）或重度周邊循環衰竭的表現。",
        "guideline_check": "• 符合 ACLS 5H5T（肺栓塞）與 Wells Criteria 臨床評估準則：當呼吸困難或不明原因休克/PEA 患者合併「單側下肢腫脹（DVT 徵象）」與「頻脈（HR > 100 bpm）」時，應高度懷疑急性肺栓塞。"
    },
    "109-29": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "右下肢遭落石壓傷 > 5 小時 → 典型壓碎症候群 (Crush Syndrome)",
            "移開落石瞬間 (再灌流 Reperfusion)：長期缺血壞死之橫紋肌細胞大量釋出鉀離子 (K+)、肌紅蛋白、磷酸與乳酸進入全身循環",
            "致命機轉：高濃度鉀離子瞬間回流至心臟，可在「重物移除後的數分鐘內」引發致死性心律不整 (VF / VT / Asystole) 導致猝死 (Smiling death)"
        ],
        "key_triggers": ["壓傷右下肢持續五小時", "重物被移除的數分鐘內死亡 (再灌流高血鉀致死性心律不整)", "脫困前給輸液、碳酸氫鈉鹼化尿液"],
        "confusion_trap": "• 本題與 113-44、108-62 互為姊妹題，三個錯誤選項皆是經典陷阱：\n• 1. 選項 (B) 時機陷阱：大量輸液（生理食鹽水）必須在**「脫困前（重物移開前）」**就開始給予，等到脫困後才給已來不及阻止再灌流休克與高血鉀！\n• 2. 選項 (C) 電解質陷阱：再灌流會造成**「高血鉀、高血磷、低血鈣」**（選項 C 寫反成低血鉀、高血鈣）！\n• 3. 選項 (D) 酸鹼字眼陷阱：給予碳酸氫鈉（Sodium bicarbonate, NaHCO3）的目的是**「鹼化（Alkalinize）尿液」**（提高尿液 pH 值 > 6.5，防止肌紅蛋白在腎小管沉澱阻塞），選項 (D) 卻故意寫成「酸化尿液」！",
        "guideline_check": "• 符合災難醫學與 ACLS 5H5T（高血鉀與酸中毒）急救指引：救援現場稱為「微笑死亡（Smiling death）」——傷患剛被救出時還意識清楚對救難人員微笑，數分鐘後即因再灌流高血鉀引發 VF 猝死。"
    },
    "109-41": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "右側張力性氣胸經針刺減壓與胸管置入後血壓、血氧改善",
            "5 分鐘後突然再度呼吸困難、血壓下降",
            "處置決策：因生命徵象再次不穩定，應立即重新進行初級評估 (Primary Survey: ABCDE)"
        ],
        "key_triggers": ["張力性氣胸胸管置入後再度呼吸困難、血壓下降", "生命徵象不穩定應重新進行初級評估"],
        "confusion_trap": "• 與 **108-56、111-44** 完全相同的三連霸考古題！\n• 請注意選項 (B) 在 109 年寫的是「右鎖骨中線第二肋間」（舊版位置），到了 111-44 出題委員還特地把選項 (B) 改成「右腋中線第五肋間」（新版位置）來增加誘答力，但不論位置對不對，**只要病人已插胸管後再度生命徵象不穩，標準答案永遠是「重新進行初級評估（選項 A）」**！",
        "guideline_check": "• 符合 ATLS / PHTLS 外傷初級評估與再評估準則。"
    },
    "109-44": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "急救藥物給藥途徑與吸收動力學選擇",
            "心搏停止與休克：優先建立靜脈管路 (IV)，若 IV 建立困難或延誤，骨內注射 (IO) 吸收速度與藥效等同於中央/周邊靜脈注射",
            "特殊族群 IV 部位：孕婦因增大之子宮壓迫下腔靜脈，靜脈管路必須建立於「橫膈膜以上 (上肢)」",
            "過敏性休克 (Anaphylaxis)：Epinephrine 1:1000 (0.3~0.5 mg) 首選路徑為「大腿前外側肌肉注射 (IM)」，而非皮下注射 (SC)"
        ],
        "key_triggers": ["藥物給予與路徑", "孕婦 IV 建立於橫膈以上", "過敏性休克 Epinephrine 首選為大腿前外側肌肉注射 (IM)", "骨內注射 (IO) 相當於 IV"],
        "confusion_trap": "• 選項 (B) 為臨床極常考的給藥路徑陷阱：在**過敏性休克（Anaphylactic shock）**時，病患周邊皮膚血管收縮或微血管通透性改變，若採用「皮下注射（SC）」吸收極慢且不穩定！因此指引強制規定首選為**「大腿前外側（股外側肌）肌肉注射（IM）」**，可迅速達到最高血中藥物濃度！\n• 選項 (C) 記憶口訣：可經由氣管內管（ET tube）給藥的四大急救藥物口訣為 **`NAVEL`** —— **N**aloxone、**A**tropine、**V**asopressin、**E**pinephrine、**L**idocaine（劑量需為靜脈劑量的 2~2.5 倍並稀釋）。",
        "guideline_check": "• 完全符合 AHA 2020/2025 ACLS 給藥途徑（IV/IO 優先，過敏性休克 IM Epinephrine 首選）與孕婦復甦指引（橫膈膜以上建立靜脈管路）。"
    },
    "109-75": {
        "category": "ACS與12導程",
        "algorithm_path": [
            "急性冠心症 (ACS) / 急性心肌梗塞 (AMI) 冠狀動脈粥狀硬化主要危險因子評估",
            "經典不可逆危險因子：年齡、男性、早發性冠心病家族史",
            "經典可逆主要危險因子 (Major Risk Factors)：高血壓、糖尿病、高血脂、抽菸 (吸菸)",
            "次要或非主要直接因子：飲酒 (喝酒並非傳統四大主要危險因子)"
        ],
        "key_triggers": ["急性心肌梗塞 (AMI)", "主要危險因子：糖尿病、高血壓、抽菸", "喝酒不是主要危險因子"],
        "confusion_trap": "• 考生容易覺得「菸酒不分家」，誤以為喝酒也是心肌梗塞的四大主要危險因子之一。在心血管流行病學（如 Framingham Risk Score）與 EMT-P 教材中，冠狀動脈心臟病的**主要危險因子為「三高（高血壓、糖尿病、高血脂）+ 抽菸 + 家族史/年齡」**，喝酒並不列為主要危險因子（過量飲酒主要與擴張型心肌病變、心房顫動或出血性中風相關）。",
        "guideline_check": "• 符合 AHA 急性冠心症風險評估與病史詢問重點。"
    },
    "108-51": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "張力性氣胸 (Tension Pneumothorax, 5H5T) 臨床表徵與處置",
            "典型徵象：呼吸窘迫、低血壓休克、頸靜脈怒張、患側呼吸音減弱或消失、叩診鼓音、氣管偏向對側",
            "與心包膜填塞 (Cardiac Tamponade) 鑑別：心包膜填塞之 Beck's triad 為「低血壓、頸靜脈怒張、心音模糊遙遠 (Muffled heart sounds)」，呼吸音則雙側對稱清晰",
            "處置禁忌：未減壓前不可直接氣管內管插管給予正壓通氣 (否則會使張力性氣胸瞬間惡化致死)"
        ],
        "key_triggers": ["張力性氣胸", "不建議未減壓即插管正壓通氣", "ATLS 第十版成人針刺減壓位置：第五肋間腋中線前方", "休克 + 頸靜脈怒張 + 模糊心音 = 心包膜填塞 (Beck's triad)"],
        "confusion_trap": "• 選項 (D)「休克（低血壓）、頸靜脈怒張、模糊的心音」是 **心包膜填塞（Cardiac Tamponade）的貝克氏三病徵（Beck's triad）**，而非張力性氣胸的典型表現！\n• 選項 (A) 是極重要的臨床保命觀念：張力性氣胸患者若未先執行「針刺減壓」或「胸管置入」，**絕對不能先插氣管內管接正壓呼吸器（PPV）**，因為正壓打氣會把更多空氣灌進肋膜腔，使張力性氣胸瞬間轉為 PEA 心搏停止！",
        "guideline_check": "• 完全符合 ATLS 10th Edition 與 AHA ACLS 5H5T（張力性氣胸 vs 心包膜填塞）鑑別診斷要點。"
    },
    "108-56": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "50 歲騎士車禍右側張力性氣胸 → 經細針減壓與右側胸管置入後血壓 (90/70 mmHg) 與血氧 (94%) 改善",
            "5 分鐘後突然再度呼吸困難、血壓掉回 70/50 mmHg",
            "處置決策：因生命徵象不穩定，應立即重新進行初級評估 (Primary Survey: ABCDE)"
        ],
        "key_triggers": ["張力性氣胸胸管置入後再度呼吸困難、血壓下降", "生命徵象不穩定應重新進行初級評估"],
        "confusion_trap": "• 本題即為 **108-56、109-41、111-44** 三連霸考題的「始祖題」！\n• 注意在 108-56 正確答案放在選項 (C)，而 109-41 與 111-44 則移到選項 (A)，千萬不要死背選項代號，請記住核心原則：**「外傷或重症患者處置後生命徵象再次惡化 → 永遠先重新進行初級評估（Primary Survey）」**！",
        "guideline_check": "• 符合 ATLS / PHTLS 初級評估再評估原則。"
    },
    "108-62": {
        "category": "核心藥物與5H5T",
        "algorithm_path": [
            "40 歲男性左小腿巨石壓傷 > 5 小時 → 壓碎症候群 (Crush Syndrome)",
            "橫紋肌溶解與再灌流損傷：受壓肌肉釋放肌紅蛋白 (Myoglobin，導致深茶色/可樂色尿液與急性腎小管壞死腎衰竭) 及大量鉀離子、磷酸、乳酸",
            "血液生化特徵：代謝性酸中毒、高血鉀症 (5H5T)、高血磷症、低血鈣症"
        ],
        "key_triggers": ["壓傷左小腿超過五小時 (壓碎症候群)", "深色小便 (肌紅蛋白尿) 與急性腎衰竭", "代謝性酸中毒、高血鉀、低血鈣"],
        "confusion_trap": "• 與 **109-29、113-44、114-71** 完全相同的「三高一低」考點！\n• 選項 (D) 再次把「高血鉀、低血鈣」故意顛倒寫成「低血鉀、高血鈣」（請注意 108-62 的選項 D 文字與 109-29 的選項 C 文字一模一樣）！只要記住**「細胞破掉 → 鉀磷飆高、鈣變低」**，這四題就能百分之百全拿！",
        "guideline_check": "• 符合災難醫學與 ACLS 5H5T（高血鉀與酸中毒）處置準則。"
    },
}


def main():
    with open(ALL_QS_PATH, "r", encoding="utf-8") as f:
        raw_list = json.load(f)
    raw_map = {q["id"]: q for q in raw_list}

    # 合併三個 Part 的深度解析字典
    all_annotations = {}
    all_annotations.update(ANNOTATIONS_PART1)
    all_annotations.update(ANNOTATIONS_PART2)
    all_annotations.update(ANNOTATIONS_PART3)

    # 依照年度 (114 -> 108) 與題號 (1 -> 100) 排序
    def sort_key(qid):
        yr, no = qid.split("-")
        return (-int(yr), int(no))

    sorted_ids = sorted(all_annotations.keys(), key=sort_key)

    allowed_categories = {
        "心搏停止",
        "心搏過緩",
        "心搏過速",
        "ACS與12導程",
        "ROSC照護",
        "核心藥物與5H5T",
    }

    output_questions = []

    for qid in sorted_ids:
        if qid not in raw_map:
            raise ValueError(f"找不到原始題目 ID: {qid}")
        raw_q = raw_map[qid]
        ann = all_annotations[qid]

        cat = ann["category"]
        if cat not in allowed_categories:
            raise ValueError(f"題目 {qid} 的分類不在允許清單內: {cat}")

        question_text = raw_q["question"].strip()
        options_list = [opt.strip() for opt in raw_q["options"]]

        # 修正 112-58 選項 (D) 尾端連帶擷取到的圖號文字 "圖1圖2圖3圖4"
        if qid == "112-58":
            options_list = [
                opt.replace("圖1圖2圖3圖4", "").strip() for opt in options_list
            ]

        # 處理官方答案與爭議題/送分題標記
        raw_ans = raw_q["answer"].strip()
        is_disputed = bool(ann.get("is_disputed", False)) or (
            len(raw_ans) > 1 or "送分" in raw_ans or "(" in raw_ans
        )

        # 設定乾淨的 answer 欄位（若有預設覆寫則用覆寫，否則解析官方答案）
        if "answer_override" in ann:
            clean_answer = ann["answer_override"]
        elif "送分" in raw_ans:
            # 例如 "B(送分)" -> 取原公布主答案 "B"，並標記 is_disputed: true
            clean_answer = raw_ans.split("(")[0].strip()
        elif "(" in raw_ans:
            # 例如 "A(D)" 或 "A(C)" -> 轉為多解陣列 ["A", "D"]
            main_a = raw_ans.split("(")[0].strip()
            sub_a = raw_ans.split("(")[1].replace(")", "").replace("、", ",").strip()
            extra = [x.strip() for x in sub_a.split(",") if x.strip()]
            clean_answer = [main_a] + extra
        elif len(raw_ans) > 1 and all(c in "ABCD" for c in raw_ans):
            # 例如 "BD", "AB", "AD" -> 轉為陣列 ["B", "D"]
            clean_answer = list(raw_ans)
        else:
            clean_answer = raw_ans

        item = {
            "id": qid,
            "question": question_text,
            "options": options_list,
            "answer": clean_answer,
            "category": cat,
            "algorithm_path": ann["algorithm_path"],
            "key_triggers": ann["key_triggers"],
            "confusion_trap": ann["confusion_trap"],
            "guideline_check": ann["guideline_check"],
        }

        # 若為圖片題，加入 image 欄位並驗證圖檔存在
        if qid in IMAGE_IDS or "image" in ann:
            img_rel_path = ann.get("image", f"images/{qid}.png")
            img_abs_path = os.path.join(BASE_DIR, img_rel_path)
            if not os.path.exists(img_abs_path):
                raise FileNotFoundError(f"找不到圖片檔案: {img_abs_path}")
            item["image"] = img_rel_path

        # 若為爭議題或送分題，加入 is_disputed 與 official_answer 備註
        if is_disputed:
            item["is_disputed"] = True
            item["official_answer"] = raw_ans

        output_questions.append(item)

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output_questions, f, ensure_ascii=False, indent=2)

    output_js_path = os.path.join(BASE_DIR, "acls_data.js")
    with open(output_js_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated from acls_questions.json (108-114 TSEM EMT-P ACLS Questions)\n")
        f.write("window.ACLS_QUESTIONS = ")
        json.dump(output_questions, f, ensure_ascii=False, indent=2)
        f.write(";\n")

    print(f"成功生成 {OUTPUT_JSON_PATH} 與 {output_js_path}！")
    print(f"總題數：{len(output_questions)} 題")

    cat_counts = Counter(q["category"] for q in output_questions)
    print("\n【各分類題數統計】")
    for c in [
        "心搏停止",
        "心搏過緩",
        "心搏過速",
        "ACS與12導程",
        "ROSC照護",
        "核心藥物與5H5T",
    ]:
        print(f"  - {c}: {cat_counts[c]} 題")

    year_counts = Counter(q["id"].split("-")[0] for q in output_questions)
    print("\n【各年度題數統計】")
    for yr in ["114", "113", "112", "111", "110", "109", "108"]:
        print(f"  - {yr} 年度: {year_counts[yr]} 題")

    img_count = sum(1 for q in output_questions if "image" in q)
    disputed_list = [
        f"{q['id']} ({q['official_answer']})"
        for q in output_questions
        if q.get("is_disputed")
    ]
    print(f"\n【心電圖/生理圖譜裁切題數】：{img_count} 題")
    print(f"【歷年送分/多解爭議題數】：{len(disputed_list)} 題 -> {', '.join(disputed_list)}")


if __name__ == "__main__":
    main()
