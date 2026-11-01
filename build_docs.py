import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from pptx import Presentation
from pptx.util import Inches as PInches, Pt as PPt
from pptx.dml.color import RGBColor as PRGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def set_cell_background(cell, hex_color):
    """設定表格儲存格背景顏色"""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """設定儲存格內距"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

# ==============================================================================
# 1. 產生專題報告 (Word: .docx)
# ==============================================================================
def create_project_report(output_path):
    doc = Document()
    
    # 邊界設定
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # 標題
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = title.add_run("🎓 AI 課堂摘要與互動測驗小助手")
    r_title.font.name = "微軟正黑體"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(30, 58, 138) # 深藍
    
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = subtitle.add_run("專題成果報告書 ｜ 基於本機離線大模型的高效主動學習系統")
    r_sub.font.name = "微軟正黑體"
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(75, 85, 99)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 基本資訊卡片表格
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    info_data = [
        ("專題作者", "楊皓翔"),
        ("核心技術", "Python, Streamlit, Ollama / LM Studio (本地模型)"),
        ("專案定位", "解決長文學習認知錯覺、落實測試效應與離線隱私保障"),
        ("開源倉庫", "https://github.com/haohsiangyang-0921/ai-study-assistant")
    ]
    
    for i, (k, v) in enumerate(info_data):
        row = i // 2
        col = i % 2
        cell = table.cell(row, col)
        cell.width = Inches(3.2)
        set_cell_background(cell, "F3F4F6")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        r1 = p.add_run(f"【{k}】 ")
        r1.font.bold = True
        r1.font.name = "微軟正黑體"
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(31, 41, 55)
        r2 = p.add_run(v)
        r2.font.name = "微軟正黑體"
        r2.font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    def add_section_header(text, icon="📌"):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(6)
        r = h.add_run(f"{icon} {text}")
        r.font.name = "微軟正黑體"
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 64, 175)

    def add_body(text, bold_prefix="", indent=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.25
        if indent:
            p.paragraph_format.left_indent = Inches(0.2)
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = "微軟正黑體"
            r_bold.font.size = Pt(11)
            r_bold.font.bold = True
            r_bold.font.color.rgb = RGBColor(17, 24, 39)
        r_text = p.add_run(text)
        r_text.font.name = "微軟正黑體"
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = RGBColor(55, 65, 81)

    # 1. 做什麼 (What it does)
    add_section_header("一、做什麼 (What it does) — 專題目標與核心功能", "🎯")
    add_body(
        "現代學生在面對繁重的教科書、長篇論文與課堂筆記時，常陷入「花費大量時間反覆劃線重讀，考試卻記不住」的窘境。本專案運用生成式 AI 與認知心理學原理，打造專為學生量身定制的智慧學習夥伴。",
        "1.1 研發動機："
    )
    add_body("精煉條列 3 至 5 點核心知識架構，快速過濾冗言贅字，幫助學生在 30 秒內建立全篇骨架。", "● 結構化重點萃取：", indent=True)
    add_body("依據認知科學中的「測試效應」（Testing Effect），自動產出 3 題四選一理解型測驗題（包含題目、4 個選項、標準答案與深度解析）。", "● 互動式隨堂三題測驗：", indent=True)
    add_body("提供單選按鈕作答介面，提交後即時統計得分、標記正誤，並展開詳解，引導學生進行主動提取與錯題強化。", "● 即時診斷與深度題解：", indent=True)
    add_body("擺脫傳統需付費且有隱私疑慮的雲端 API，本系統優先連接電腦本地模型（Ollama / LM Studio），達成完全免費、資料 100% 離線保密。", "● 本機離線 AI 支援：", indent=True)

    # 2. 給誰用 (Target Audience)
    add_section_header("二、給誰用 (Who it is for) — 目標客群與應用場景", "👥")
    add_body("面對龐大醫學、法律、工程或人文期中期末考量的學生，能在課前預習抓重點、課後 3 分鐘快速檢測理解程度。", "● 大專院校與高中職學生：", indent=True)
    add_body("國家考試、證照考或公職考生，需快速吸收繁複法規、技術文獻，透過自測加深長期記憶編碼。", "● 自學者與證照考生：", indent=True)
    add_body("可在設計教材或課堂報告後，一鍵產生隨堂評量題目，大幅節省出題與設計解析的時間成本。", "● 課堂助教 (TA) 與教師：", indent=True)

    # 3. 怎麼做 (How it is done)
    add_section_header("三、怎麼做 (How it is done) — 技術架構與實現細節", "🛠️")
    add_body(
        "本系統採用輕量敏捷的現代化技術棧，兼具跨平台相容性與極速響應能力：",
        "3.1 系統架構設計："
    )
    add_body("採用 Python Streamlit 框架建構響應式卡片 UI，運用 Streamlit 的 on_click 回呼函式與 Session State 機制，徹底避免輸入內容與測驗狀態在頁面重繪時遺失。", "● 前端互動層 (Frontend)：", indent=True)
    add_body("透過標準 OpenAI-Compatible REST 協議對接本機 Ollama (http://localhost:11434/v1) 或 LM Studio (http://localhost:1234/v1)。使用 requests 模組直接發送結構化 Prompt，無需繁重 SDK，隨開即跑。", "● AI 運算層 (Local LLM)：", indent=True)
    add_body("針對本地大模型（如 Llama 3.2, Qwen 2.5）偶發的非結構化贅詞或 Markdown 程式碼區塊包裹，實作「正規表示式 + 最外層括號探測」雙重容錯解析器，保證回傳資料 100% 成功解析為標準 JSON 物件。", "● 容錯解析機制 (JSON Parser)：", indent=True)
    add_body("當檢測到使用者未開啟本地模型伺服器時，系統自動無縫降級為預設的高品質演示模式，保證 90 秒展示或評審考核時零故障、零中斷。", "● 90 秒演示備用機制 (Demo Mode)：", indent=True)

    # 4. 怎麼測 (How it is tested)
    add_section_header("四、怎麼測 (How it is tested) — 測試方法與驗證成果", "🧪")
    add_body(
        "為確保系統在各種情境下的穩定性與出題品質，本專題進行了四層嚴格驗證：",
        "4.1 測試規劃與實施："
    )
    add_body("使用內建「主動回想與遺忘曲線」教育心理學短文進行驗證。重點摘要涵蓋率達 100%，生成的三題測驗均精準鎖定核心觀念（如認知錯覺與神經重構），解析清晰到位。", "● 基準教材測試 (Baseline Test)：", indent=True)
    add_body("貼入醫學神經學筆記、Python 物件導向教學文章與世界歷史長文進行泛化測試。模型成功依據跨領域知識產出高水準單選題，未發生幻覺或格式崩潰。", "● 跨學科長文壓力測試 (Stress Test)：", indent=True)
    add_body("在關閉 Ollama 服務的狀態下點擊生成，系統成功攔截連線例外並以友善提示降級為 Demo Mode，未出現 Python 崩潰或紅字報錯。", "● 斷線降級容錯測試 (Failover Test)：", indent=True)
    add_body("測試全部答對（觸發慶祝特效）、部分答對與未作答提交。系統即時且準確計算得分百分比，展開逐題正誤標籤與深度題解。", "● 互動評分反饋測試 (UI/UX Test)：", indent=True)

    # 5. 下一步 (Next steps)
    add_section_header("五、下一步 (Next steps) — 未來藍圖與功能擴充", "🚀")
    add_body("整合 PyPDF2 與 python-docx，讓學生可直接拖曳上傳上百頁的課本章節 PDF 或語音逐字稿，進行全書階層式摘要。", "● 多格式檔案拖曳上傳：", indent=True)
    add_body("結合艾賓浩斯遺忘曲線，記錄學生的錯題歷史，並於 1 天、3 天、7 天後透過瀏覽器通知自動推播「個人化間隔複習測驗」。", "● 間隔重複 (Spaced Repetition) 複習推播：", indent=True)
    add_body("提供一鍵導出為 Anki 數位單字記憶卡（.apkg），方便學生匯入手機隨時隨地刷題複習。", "● 匯出 Anki 牌組支援：", indent=True)
    add_body("探索 1B ~ 3B 級別專用微調小模型（如 Qwen2.5-1.5B Instruct 微調出題權重），達成極致輕量化，連低階筆電或平板都能秒級推論。", "● 教學專用端側小模型量化：", indent=True)

    doc.save(output_path)
    print(f"專題報告已成功儲存至: {output_path}")

# ==============================================================================
# 2. 產生 90 秒展示投影片 (PowerPoint: .pptx)
# ==============================================================================
def create_presentation_slides(output_path):
    prs = Presentation()
    # 16:9 寬螢幕投影片尺寸
    prs.slide_width = PInches(13.333)
    prs.slide_height = PInches(7.5)
    blank_layout = prs.slide_layouts[6] # 空白佈局

    # 配色方案
    COLOR_BG = PRGBColor(248, 250, 252)        # 淺灰底
    COLOR_PRIMARY = PRGBColor(30, 58, 138)     # 深藍
    COLOR_ACCENT = PRGBColor(37, 99, 235)      # 亮藍
    COLOR_TEXT_MAIN = PRGBColor(17, 24, 39)    # 深黑灰
    COLOR_TEXT_MUTED = PRGBColor(75, 85, 99)   # 中灰
    COLOR_CARD_BG = PRGBColor(255, 255, 255)   # 白底卡片
    COLOR_GREEN = PRGBColor(16, 185, 129)      # 綠色標籤
    COLOR_AMBER = PRGBColor(217, 119, 6)       # 琥珀橙

    def add_header(slide, title_text, category_text, time_tag=""):
        # 分類小標
        cat_box = slide.shapes.add_textbox(PInches(0.8), PInches(0.5), PInches(8), PInches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = f"{category_text}  {('｜ ⏱️ ' + time_tag) if time_tag else ''}".upper()
        p_cat.font.name = "微軟正黑體"
        p_cat.font.size = PPt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACCENT

        # 主標題
        title_box = slide.shapes.add_textbox(PInches(0.8), PInches(0.85), PInches(11.5), PInches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "微軟正黑體"
        p_t.font.size = PPt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_PRIMARY

    def add_card(slide, left, top, width, height, title, items, badge_text="", badge_color=COLOR_ACCENT):
        # 卡片背景矩形
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_CARD_BG
        shape.line.color.rgb = PRGBColor(229, 231, 235)
        shape.line.width = PPt(1.5)

        # 頂部 Badge 與標題
        tb = slide.shapes.add_textbox(left + PInches(0.25), top + PInches(0.25), width - PInches(0.5), PInches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        if badge_text:
            p.text = f"[{badge_text}] {title}"
        else:
            p.text = title
        p.font.name = "微軟正黑體"
        p.font.size = PPt(16)
        p.font.bold = True
        p.font.color.rgb = badge_color

        # 條列內容
        tb_body = slide.shapes.add_textbox(left + PInches(0.25), top + PInches(0.8), width - PInches(0.5), height - PInches(0.95))
        tf_body = tb_body.text_frame
        tf_body.word_wrap = True
        for idx, itm in enumerate(items):
            p_itm = tf_body.paragraphs[0] if idx == 0 else tf_body.add_paragraph()
            p_itm.text = f"• {itm}"
            p_itm.font.name = "微軟正黑體"
            p_itm.font.size = PPt(12.5)
            p_itm.font.color.rgb = COLOR_TEXT_MAIN
            p_itm.space_after = PPt(8)

    # --------------------------------------------------------------------------
    # Slide 1: 封面 (0 ~ 10 秒)
    # --------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    # 背景大卡片
    bg_s1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_s1.fill.solid()
    bg_s1.fill.fore_color.rgb = PRGBColor(241, 245, 249)
    bg_s1.line.fill.background()

    tb1 = s1.shapes.add_textbox(PInches(1.2), PInches(1.8), PInches(11), PInches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "🎓 AI 課堂摘要與互動測驗小助手"
    p1.font.name = "微軟正黑體"
    p1.font.size = PPt(38)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_PRIMARY
    p1.space_after = PPt(14)

    p2 = tf1.add_paragraph()
    p2.text = "基於本機離線大模型（Local LLM）的學生智慧複習夥伴 ｜ 90 秒專案成果展示"
    p2.font.name = "微軟正黑體"
    p2.font.size = PPt(18)
    p2.font.color.rgb = COLOR_ACCENT
    p2.space_after = PPt(28)

    p3 = tf1.add_paragraph()
    p3.text = "報告人：楊皓翔  ｜  核心技術：Python · Streamlit · Ollama / LM Studio (離線隱私)"
    p3.font.name = "微軟正黑體"
    p3.font.size = PPt(14)
    p3.font.color.rgb = COLOR_TEXT_MUTED

    # --------------------------------------------------------------------------
    # Slide 2: 學生學習痛點 (10 ~ 25 秒)
    # --------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "學生讀書抓不到重點？缺乏練習題？傳統複習的三大困境", "PROBLEM STATEMENT", "10s ~ 25s")
    
    add_card(s2, PInches(0.8), PInches(1.9), PInches(3.7), PInches(4.8), 
             "痛點 1：被動劃線的認知錯覺", 
             [
                 "反覆瀏覽長篇課文，看似用功劃滿螢光筆。",
                 "心理學指出：這只是「視覺熟悉感」，並非大腦真正的長期記憶編碼。",
                 "考場上一蓋上書本，大腦依然一片空白。"
             ],
             "效率低", PRGBColor(220, 38, 38))

    add_card(s2, PInches(4.8), PInches(1.9), PInches(3.7), PInches(4.8), 
             "痛點 2：讀完缺乏即時題目檢驗", 
             [
                 "缺少隨堂小測驗進行「主動提取」（Active Recall）。",
                 "無法觸發神經突觸強化的「測試效應」（Testing Effect）。",
                 "學生不知道自己哪裡沒懂，無法針對錯點補強。"
             ],
             "無反饋", PRGBColor(217, 119, 6))

    add_card(s2, PInches(8.8), PInches(1.9), PInches(3.7), PInches(4.8), 
             "痛點 3：市面雲端 AI 的隱私與費用", 
             [
                 "OpenAI / Claude 需月費或綁定信用卡，學生負擔重。",
                 "將課堂未公開教材或研究報告上傳雲端，有版權與隱私疑慮。",
                 "網路不穩或無額度時無法進行複習。"
             ],
             "門檻高", PRGBColor(79, 70, 229))

    # --------------------------------------------------------------------------
    # Slide 3: 核心功能與創新解方 (25 ~ 45 秒)
    # --------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "三大核心解方：提煉重點、主動測驗、本機離線隱私", "SOLUTION OVERVIEW", "25s ~ 45s")

    add_card(s3, PInches(0.8), PInches(1.9), PInches(3.7), PInches(4.8), 
             "1. 結構化核心摘要", 
             [
                 "智慧去蕪存菁：一鍵萃取 3~5 點核心考點條列。",
                 "概念標籤化：每個重點標註專屬關鍵字與原理解說。",
                 "30 秒快速掌握全章核心，打通學習脈絡。"
             ],
             "精準萃取", COLOR_ACCENT)

    add_card(s3, PInches(4.8), PInches(1.9), PInches(3.7), PInches(4.8), 
             "2. 互動式隨堂測驗", 
             [
                 "自動生成 3 題四選一單選題，考查理解而非死背。",
                 "線上點選作答，點擊「提交」即時批改並計算分數。",
                 "逐題展開深度解析，指出為何對、為何錯。"
             ],
             "主動回想", COLOR_GREEN)

    add_card(s3, PInches(8.8), PInches(1.9), PInches(3.7), PInches(4.8), 
             "3. 本機模型離線保護", 
             [
                 "支援電腦本機 Ollama / LM Studio 離線模型運算。",
                 "100% 免費、零 API Key 洩漏、資料絕不上傳雲端。",
                 "內建 90 秒展示 Demo 模式，雙重備援保證不當機。"
             ],
             "離線免費", PRGBColor(13, 148, 136))

    # --------------------------------------------------------------------------
    # Slide 4: 系統架構與技術亮點 (45 ~ 60 秒)
    # --------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "輕量敏捷架構：Streamlit 前端 + 本地大模型推論", "ARCHITECTURE & TECH STACK", "45s ~ 60s")

    add_card(s4, PInches(0.8), PInches(1.9), PInches(5.7), PInches(4.8), 
             "系統技術架構", 
             [
                 "前端介面：Streamlit 現代化卡片式學生友善 UI。",
                 "狀態管理：使用 on_click 回呼函式與 Session State，徹底解決頁面重新渲染導致的文字遺失問題。",
                 "通訊協議：標準 OpenAI-Compatible REST API，透過輕量 requests 直連本地 11434 埠，無需繁瑣套件。",
                 "模型支援：Llama 3.2, Qwen 2.5, Gemma 2 等常見主流本地端側模型。"
             ],
             "前端與通訊", COLOR_PRIMARY)

    add_card(s4, PInches(6.8), PInches(1.9), PInches(5.7), PInches(4.8), 
             "核心演算法與穩定性保證", 
             [
                 "強健 JSON 容錯提取器：以正則表達式自動穿透本地模型常夾帶的 Markdown 程式碼標籤，穩定輸出標準結構。",
                 "無伺服器 Demo 備用機制：若檢測到本機尚未啟動 Ollama，自動無縫降級至 Demo 模擬模式，達成 100% 演示可用性。",
                 "一鍵模型偵測：側邊欄提供探測按鈕，自動讀取本機目前所有已下載的 AI 模型清單。"
             ],
             "穩定性設計", COLOR_GREEN)

    # --------------------------------------------------------------------------
    # Slide 5: 現場展示腳本 (60 ~ 75 秒)
    # --------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "現場 90 秒極速演示流程：三步驟完成高效學習閉環", "LIVE DEMO FLOW", "60s ~ 75s")

    add_card(s5, PInches(0.8), PInches(1.9), PInches(3.7), PInches(4.8), 
             "Step 1：一鍵載入教材", 
             [
                 "點擊「📚 載入範例文章」。",
                 "自動帶入「主動回想與遺忘曲線」精選短文。",
                 "展示學生免手打、免手動複製貼上的直覺體驗。"
             ],
             "30 秒內", COLOR_ACCENT)

    add_card(s5, PInches(4.8), PInches(1.9), PInches(3.7), PInches(4.8), 
             "Step 2：AI 分析與重點萃取", 
             [
                 "點擊「🚀 開始由本地 AI 分析生成」。",
                 "本機模型迅速提煉 4 點核心條列重點。",
                 "向評審展示乾淨清楚的卡片化概念精華。"
             ],
             "迅速生成", COLOR_AMBER)

    add_card(s5, PInches(8.8), PInches(1.9), PInches(3.7), PInches(4.8), 
             "Step 3：互動測驗與即時批改", 
             [
                 "現場點選 3 題四選一單選題答案。",
                 "點擊「📝 提交答案並查看解析」。",
                 "展示全對慶祝氣球特效、分數反饋與逐題深度題解。"
             ],
             "閉環驗證", COLOR_GREEN)

    # --------------------------------------------------------------------------
    # Slide 6: 未來展望與結語 (75 ~ 90 秒)
    # --------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "未來展望：打造個人化自適應長期記憶中樞", "FUTURE ROADMAP & CONCLUSION", "75s ~ 90s")

    add_card(s6, PInches(0.8), PInches(1.9), PInches(5.7), PInches(4.8), 
             "下一步發展藍圖 (Next Steps)", 
             [
                 "多格式支援：擴充 PDF 課本與錄音檔逐字稿直接拖曳解析。",
                 "間隔重複推播：整合艾賓浩斯遺忘週期，在 1 天、3 天、7 天後自動推播錯題溫習通知。",
                 "匯出數位牌組：一鍵導出至 Anki (.apkg) 記憶卡，落實隨時隨地刷題。",
                 "專用端側小模型：微調 1.5B ~ 3B 專用出題小模型，連低階筆電都能秒級出題。"
             ],
             "功能擴充", COLOR_PRIMARY)

    add_card(s6, PInches(6.8), PInches(1.9), PInches(5.7), PInches(4.8), 
             "專案價值總結", 
             [
                 "🎯 學習效能：告別無效反覆劃線，以測驗驅動大腦深度編碼。",
                 "🔒 本地自主：不依賴任何付費雲端 API，個人學習隱私零風險。",
                 "💡 開源分享：專案完整程式碼已開源至 GitHub，開箱即用！",
                 "感謝聆聽！請各位評審老師批評指教！"
             ],
             "專題總結", COLOR_GREEN)

    prs.save(output_path)
    print(f"專題簡報已成功儲存至: {output_path}")

if __name__ == "__main__":
    report_file = os.path.abspath(r"c:\Users\yangh\OneDrive\Desktop\ai-study-assistant\專題報告_AI課堂摘要與互動測驗小助手.docx")
    slides_file = os.path.abspath(r"c:\Users\yangh\OneDrive\Desktop\ai-study-assistant\專題簡報_AI課堂摘要與互動測驗小助手.pptx")
    
    create_project_report(report_file)
    create_presentation_slides(slides_file)
