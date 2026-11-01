import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_styled_report(docx_path, html_path):
    doc = Document()
    
    # 邊距設定 (標準 A4 邊界: 上下左右各 1 英吋)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # 1. 主標題
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("AI 課堂摘要與互動測驗小助手")
    r_title.font.name = "微軟正黑體"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(30, 58, 138) # 深藍色

    # 2. 作者資訊
    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.space_after = Pt(22)
    r_author = p_author.add_run("411587035 教行一 楊皓翔")
    r_author.font.name = "微軟正黑體"
    r_author.font.size = Pt(13)
    r_author.font.bold = True
    r_author.font.color.rgb = RGBColor(55, 65, 81) # 深灰

    # 定義章節標題樣式
    def add_heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.font.name = "微軟正黑體"
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = RGBColor(37, 99, 235) # 主題藍色
        return p

    # 定義一般段落樣式
    def add_paragraph(text, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.3
        r = p.add_run(text)
        r.font.name = "微軟正黑體"
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(31, 41, 55)
        return p

    # 定義條列式清單樣式
    def add_bullet(text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.3
        
        # 實心圓點
        r_bullet = p.add_run("● ")
        r_bullet.font.name = "微軟正黑體"
        r_bullet.font.size = Pt(9.5)
        r_bullet.font.color.rgb = RGBColor(37, 99, 235)
        
        r_text = p.add_run(text)
        r_text.font.name = "微軟正黑體"
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = RGBColor(31, 41, 55)
        return p

    # 一、做什麼
    add_heading("一、做什麼")
    add_paragraph("動機：現在學生在面對厚重的教科書和課堂筆記時，會出現花很多時間一直重讀，考試卻記不住的困難，所以利用這次機會做一個可以快速複習的工具。")
    add_bullet("條列 3-5 點核心知識，快速過濾冗言贅字，在 30 秒內建立最基礎的認識。")
    add_bullet("生成 3 題四選一理解型測驗題（包含題目、4 個選項、標準答案與解析）。")
    add_bullet("提供單選按鈕作答介面，提交後即時統計得分、標記正誤，並展開詳解，引導學生進行主動提取與錯題強化。")

    # 二、給誰用
    add_heading("二、給誰用")
    add_bullet("大學和高中職學生：面對醫學、法律、工程或人文期中期末考量的學生，能在課前預習抓重點、課後 3 分鐘快速檢測理解程度。")
    add_bullet("自學與證照考生：國家考試、證照考或公職考生，快速吸收繁複法規、技術文獻，透過自測加深記憶。")

    # 三、怎麼做
    add_heading("三、怎麼做")
    add_bullet("畫面好操作，即使不小心按到重新整理，剛剛寫的內容跟測驗進度也都還在，不用重新填寫。")
    add_bullet("只需要電腦裡面有本地的 AI 模型，程式一開就能直接連線使用，輕巧又快速。")
    add_bullet("AI 講話有時會帶多餘的廢詞或格式亂掉，系統會自己把重點挑出來，確認程式可以正常使用。")
    add_bullet("以防使用時發生故障，系統會自動切換成「預設範例」，讓其他人可以知道在做甚麼。")

    # 四、怎麼測
    add_heading("四、怎麼測")
    add_bullet("用預設的教育文章測試，AI 不僅能夠 100% 抓出文章重點，出的 3 題測驗也都精準打中核心概念，解析非常清楚。")
    add_bullet("測試全對（會跳出慶祝特效）、答對一半或沒寫完等狀況，系統都能瞬間算出分數，並清楚標出每題對錯與詳細解析。")

    # 五、下一步
    add_heading("五、下一步")
    add_bullet("可以上傳整份檔案，不需要像現在一樣一個字一個字慢慢打。")
    add_bullet("製作可以隨身攜帶的記憶卡，不需要網頁也可以複習。")
    add_bullet("針對手機、平板以及畫面較小的裝置改善網頁的顯示模式。")

    # 儲存 docx
    doc.save(docx_path)
    print(f"Word 報告已儲存: {docx_path}")

    # 同時產生高質感、支援列印轉 PDF 的 HTML 報告
    html_content = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>AI 課堂摘要與互動測驗小助手 - 專題報告書</title>
    <style>
        @page {
            size: A4;
            margin: 2.2cm 2.5cm;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Microsoft JhengHei", "PingFang TC", "Noto Sans TC", sans-serif;
            color: #1F2937;
            line-height: 1.7;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #F9FAFB;
        }
        .page {
            background: #FFFFFF;
            padding: 50px 60px;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        h1 {
            color: #1E3A8A;
            text-align: center;
            font-size: 24pt;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }
        .author {
            text-align: center;
            color: #4B5563;
            font-size: 13pt;
            font-weight: 600;
            margin-bottom: 35px;
        }
        h2 {
            color: #2563EB;
            font-size: 15pt;
            margin-top: 26px;
            margin-bottom: 12px;
            border-bottom: 2px solid #EFF6FF;
            padding-bottom: 5px;
        }
        p {
            font-size: 11.5pt;
            margin-bottom: 10px;
            color: #374151;
            text-align: justify;
        }
        ul {
            list-style: none;
            padding-left: 5px;
            margin-top: 8px;
            margin-bottom: 14px;
        }
        li {
            font-size: 11.5pt;
            margin-bottom: 10px;
            color: #374151;
            position: relative;
            padding-left: 24px;
            text-align: justify;
        }
        li::before {
            content: "●";
            color: #2563EB;
            font-size: 9pt;
            position: absolute;
            left: 4px;
            top: 1px;
        }
        .print-btn {
            display: block;
            margin: 0 auto 25px auto;
            padding: 10px 24px;
            background-color: #2563EB;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
        }
        @media print {
            body {
                background: none;
                padding: 0;
            }
            .page {
                box-shadow: none;
                padding: 0;
            }
            .print-btn {
                display: none;
            }
        }
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">🖨️ 列印或另存為 PDF (Print to PDF)</button>
    <div class="page">
        <h1>AI 課堂摘要與互動測驗小助手</h1>
        <div class="author">411587035 教行一 楊皓翔</div>

        <h2>一、做什麼</h2>
        <p>動機：現在學生在面對厚重的教科書和課堂筆記時，會出現花很多時間一直重讀，考試卻記不住的困難，所以利用這次機會做一個可以快速複習的工具。</p>
        <ul>
            <li>條列 3-5 點核心知識，快速過濾冗言贅字，在 30 秒內建立最基礎的認識。</li>
            <li>生成 3 題四選一理解型測驗題（包含題目、4 個選項、標準答案與解析）。</li>
            <li>提供單選按鈕作答介面，提交後即時統計得分、標記正誤，並展開詳解，引導學生進行主動提取與錯題強化。</li>
        </ul>

        <h2>二、給誰用</h2>
        <ul>
            <li><b>大學和高中職學生</b>：面對醫學、法律、工程或人文期中期末考量的學生，能在課前預習抓重點、課後 3 分鐘快速檢測理解程度。</li>
            <li><b>自學與證照考生</b>：國家考試、證照考或公職考生，快速吸收繁複法規、技術文獻，透過自測加深記憶。</li>
        </ul>

        <h2>三、怎麼做</h2>
        <ul>
            <li>畫面好操作，即使不小心按到重新整理，剛剛寫的內容跟測驗進度也都還在，不用重新填寫。</li>
            <li>只需要電腦裡面有本地的 AI 模型，程式一開就能直接連線使用，輕巧又快速。</li>
            <li>AI 講話有時會帶多餘的廢詞或格式亂掉，系統會自己把重點挑出來，確認程式可以正常使用。</li>
            <li>以防使用時發生故障，系統會自動切換成「預設範例」，讓其他人可以知道在做甚麼。</li>
        </ul>

        <h2>四、怎麼測</h2>
        <ul>
            <li>用預設的教育文章測試，AI 不僅能夠 100% 抓出文章重點，出的 3 題測驗也都精準打中核心概念，解析非常清楚。</li>
            <li>測試全對（會跳出慶祝特效）、答對一半或沒寫完等狀況，系統都能瞬間算出分數，並清楚標出每題對錯與詳細解析。</li>
        </ul>

        <h2>五、下一步</h2>
        <ul>
            <li>可以上傳整份檔案，不需要像現在一樣一個字一個字慢慢打。</li>
            <li>製作可以隨身攜帶的記憶卡，不需要網頁也可以複習。</li>
            <li>針對手機、平板以及畫面較小的裝置改善網頁的顯示模式。</li>
        </ul>
    </div>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML 報告已儲存: {html_path}")

if __name__ == "__main__":
    base_dir = r"c:\Users\yangh\OneDrive\Desktop\ai-study-assistant"
    docx_file = os.path.join(base_dir, "專題報告_AI課堂摘要與互動測驗小助手.docx")
    html_file = os.path.join(base_dir, "專題報告_AI課堂摘要與互動測驗小助手.html")
    create_styled_report(docx_file, html_file)
