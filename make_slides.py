import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]

# 配色
BLUE_DARK  = RGBColor(30,  58, 138)   # 深藍
BLUE_MID   = RGBColor(37,  99, 235)   # 亮藍
GREEN      = RGBColor(16, 185, 129)   # 翠綠
ORANGE     = RGBColor(234, 88,  12)   # 橘
WHITE      = RGBColor(255, 255, 255)
GRAY_DARK  = RGBColor(31,  41,  55)
GRAY_MID   = RGBColor(107, 114, 128)
BG         = RGBColor(241, 245, 249)  # 淡藍灰背景

def bg(slide, color=BG):
    """整頁底色"""
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0,
                               prs.slide_width, prs.slide_height)
    s.fill.solid(); s.fill.fore_color.rgb = color
    s.line.fill.background()

def rect(slide, l, t, w, h, fill, line_color=None, line_w=1.5):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line_color:
        s.line.color.rgb = line_color; s.line.width = Pt(line_w)
    else:
        s.line.fill.background()
    return s

def tb(slide, text, l, t, w, h,
       size=14, bold=False, color=GRAY_DARK, align=PP_ALIGN.LEFT,
       wrap=True, italic=False):
    box = slide.shapes.add_textbox(l, t, w, h)
    box.text_frame.word_wrap = wrap
    p   = box.text_frame.paragraphs[0]
    p.alignment = align
    run = p.add_run(); run.text = text
    run.font.name   = "微軟正黑體"
    run.font.size   = Pt(size)
    run.font.bold   = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return box

def card(slide, l, t, w, h, icon, title, bullets,
         icon_color=BLUE_MID, title_color=BLUE_DARK):
    rect(slide, l, t, w, h, WHITE, RGBColor(209,213,219))
    # Icon + 標題
    tb(slide, f"{icon}  {title}", l+Inches(0.2), t+Inches(0.15),
       w-Inches(0.4), Inches(0.55), size=14, bold=True, color=icon_color)
    # 分隔線 (細矩形)
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        l+Inches(0.2), t+Inches(0.7), w-Inches(0.4), Pt(1.5))
    s.fill.solid(); s.fill.fore_color.rgb = RGBColor(209,213,219)
    s.line.fill.background()
    # 條列
    box = slide.shapes.add_textbox(l+Inches(0.2), t+Inches(0.75),
                                   w-Inches(0.4), h-Inches(0.9))
    box.text_frame.word_wrap = True
    for i, b in enumerate(bullets):
        p = box.text_frame.paragraphs[0] if i==0 \
            else box.text_frame.add_paragraph()
        p.space_after = Pt(5)
        run = p.add_run()
        run.text = f"• {b}"
        run.font.name  = "微軟正黑體"
        run.font.size  = Pt(11.5)
        run.font.color.rgb = GRAY_DARK

def tag(slide, text, l, t, fill=BLUE_MID):
    w = Inches(1.9); h = Inches(0.35)
    rect(slide, l, t, w, h, fill)
    tb(slide, text, l, t, w, h, size=11, bold=True, color=WHITE,
       align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────────────────
# Slide 1 ▸ 封面
# ─────────────────────────────────────────────────────────────────────────────
s1 = prs.slides.add_slide(BLANK)
bg(s1, RGBColor(30, 58, 138))          # 深藍底

# 左側白色大卡
rect(s1, Inches(0.6), Inches(0.9), Inches(7.5), Inches(5.7),
     WHITE, line_color=None)

tb(s1, "🎓  AI 課堂摘要\n        與互動測驗小助手",
   Inches(0.9), Inches(1.2), Inches(7.0), Inches(2.2),
   size=30, bold=True, color=BLUE_DARK)

tb(s1, "「讀完課文，卻不記得任何重點？」\n用 AI 幫你一鍵整理重點＋出 3 題考你！",
   Inches(0.9), Inches(3.4), Inches(7.0), Inches(1.2),
   size=14, color=GRAY_DARK)

tb(s1, "411587035｜教行一｜楊皓翔",
   Inches(0.9), Inches(5.6), Inches(7.0), Inches(0.5),
   size=12, color=GRAY_MID)

# 右側三個彩色標籤
for i,(emoji,txt,col) in enumerate([
    ("📝","一鍵萃取重點", BLUE_MID),
    ("✍️","自動出題測驗", GREEN),
    ("🔒","免費離線運算", ORANGE),
]):
    ly = Inches(1.6) + i*Inches(1.5)
    rect(s1, Inches(8.8), ly, Inches(3.8), Inches(1.1), col)
    tb(s1, emoji, Inches(8.9), ly+Inches(0.12), Inches(0.6), Inches(0.8),
       size=22, color=WHITE)
    tb(s1, txt,   Inches(9.5), ly+Inches(0.28), Inches(3.0), Inches(0.6),
       size=15, bold=True, color=WHITE)

tb(s1, "90 秒展示用投影片", Inches(8.8), Inches(6.4), Inches(3.8), Inches(0.5),
   size=11, color=RGBColor(147,197,253), align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────────────────
# Slide 2 ▸ 一個畫面說清楚
# ─────────────────────────────────────────────────────────────────────────────
s2 = prs.slides.add_slide(BLANK); bg(s2)

rect(s2, 0, 0, prs.slide_width, Inches(1.3), BLUE_DARK)
tb(s2, "這個工具到底是什麼？",
   Inches(0.5), Inches(0.2), Inches(10), Inches(0.9),
   size=26, bold=True, color=WHITE)
tb(s2, "⏱ 0:00 ~ 0:20",
   Inches(11.0), Inches(0.35), Inches(2.0), Inches(0.5),
   size=12, color=RGBColor(147,197,253))

# 大說明框
rect(s2, Inches(0.5), Inches(1.5), Inches(12.3), Inches(1.2),
     RGBColor(239,246,255), RGBColor(191,219,254))
tb(s2,
   "😫  學生的困境：讀了好幾頁課本，劃滿螢光筆，但合上書就忘了⋯⋯"
   "  原因：「看過」不等於「記住」，大腦需要主動思考才能真正學進去！",
   Inches(0.7), Inches(1.6), Inches(11.9), Inches(1.0),
   size=13, color=BLUE_DARK)

# 三大功能卡
card(s2, Inches(0.5), Inches(2.9), Inches(3.85), Inches(3.8),
     "📝", "一鍵整理重點",
     ["貼上任何課文，直接按一個按鈕。",
      "AI 幫你整理成 3~5 點，清清楚楚。",
      "不再瞎猜「這段到底重不重要」。"],
     BLUE_MID, BLUE_DARK)

card(s2, Inches(4.74), Inches(2.9), Inches(3.85), Inches(3.8),
     "✍️", "自動出 3 題測驗",
     ["讀完馬上就有題目可以做。",
      "每題都有 4 個選項，附上解析。",
      "考你「有沒有真的懂」，不是死背。"],
     GREEN, RGBColor(4,120,87))

card(s2, Inches(8.98), Inches(2.9), Inches(3.85), Inches(3.8),
     "🔒", "完全免費離線",
     ["用你電腦裡已裝好的 AI 模型。",
      "不需要網路，不需要付錢。",
      "課本筆記不會跑到外面的伺服器。"],
     ORANGE, RGBColor(154,52,18))

# ─────────────────────────────────────────────────────────────────────────────
# Slide 3 ▸ 怎麼用（步驟說明）
# ─────────────────────────────────────────────────────────────────────────────
s3 = prs.slides.add_slide(BLANK); bg(s3)

rect(s3, 0, 0, prs.slide_width, Inches(1.3), GREEN)
tb(s3, "怎麼用？三步驟就完成！",
   Inches(0.5), Inches(0.2), Inches(10), Inches(0.9),
   size=26, bold=True, color=WHITE)
tb(s3, "⏱ 0:20 ~ 1:00（現場操作）",
   Inches(10.2), Inches(0.35), Inches(3.0), Inches(0.5),
   size=12, color=RGBColor(209,250,229))

# 步驟一
rect(s3, Inches(0.4), Inches(1.4), Inches(3.9), Inches(5.5),
     RGBColor(239,246,255), RGBColor(191,219,254))
tb(s3, "Step 1", Inches(0.6), Inches(1.5), Inches(1.2), Inches(0.4),
   size=11, bold=True, color=WHITE)
rect(s3, Inches(0.6), Inches(1.55), Inches(1.1), Inches(0.35), BLUE_MID)
tb(s3, "Step 1", Inches(0.6), Inches(1.55), Inches(1.1), Inches(0.35),
   size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
tb(s3, "貼上課文", Inches(0.6), Inches(2.0), Inches(3.5), Inches(0.55),
   size=18, bold=True, color=BLUE_DARK)
tb(s3,
   "📋  點「載入範例文章」\n     或自己貼上任何課文、筆記。\n\n"
   "→ 底下的大方框會出現文字\n   就代表準備好了！",
   Inches(0.6), Inches(2.65), Inches(3.5), Inches(3.7),
   size=12.5, color=GRAY_DARK)

# 步驟二
rect(s3, Inches(4.7), Inches(1.4), Inches(3.9), Inches(5.5),
     RGBColor(240,253,244), RGBColor(167,243,208))
rect(s3, Inches(4.9), Inches(1.55), Inches(1.1), Inches(0.35), GREEN)
tb(s3, "Step 2", Inches(4.9), Inches(1.55), Inches(1.1), Inches(0.35),
   size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
tb(s3, "按一下按鈕", Inches(4.9), Inches(2.0), Inches(3.5), Inches(0.55),
   size=18, bold=True, color=RGBColor(4,120,87))
tb(s3,
   "🚀  點「開始分析並生成測驗」\n\n"
   "→ 等幾秒鐘，AI 就會：\n\n"
   "   ① 整理出 3~5 個核心重點\n"
   "   ② 自動出好 3 題考題",
   Inches(4.9), Inches(2.65), Inches(3.5), Inches(3.7),
   size=12.5, color=GRAY_DARK)

# 步驟三
rect(s3, Inches(9.0), Inches(1.4), Inches(3.9), Inches(5.5),
     RGBColor(255,247,237), RGBColor(253,186,116))
rect(s3, Inches(9.2), Inches(1.55), Inches(1.1), Inches(0.35), ORANGE)
tb(s3, "Step 3", Inches(9.2), Inches(1.55), Inches(1.1), Inches(0.35),
   size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
tb(s3, "作答＋看解析", Inches(9.2), Inches(2.0), Inches(3.5), Inches(0.55),
   size=18, bold=True, color=ORANGE)
tb(s3,
   "✍️  點選 3 題的答案\n     然後按「提交答案」\n\n"
   "→ 系統馬上告訴你：\n\n"
   "   ✅ 哪題答對？\n"
   "   ❌ 哪題答錯？為什麼錯？",
   Inches(9.2), Inches(2.65), Inches(3.5), Inches(3.7),
   size=12.5, color=GRAY_DARK)

# ─────────────────────────────────────────────────────────────────────────────
# Slide 4 ▸ 背後怎麼做到的（技術白話版）
# ─────────────────────────────────────────────────────────────────────────────
s4 = prs.slides.add_slide(BLANK); bg(s4)

rect(s4, 0, 0, prs.slide_width, Inches(1.3), ORANGE)
tb(s4, "背後怎麼做到的？（白話技術說明）",
   Inches(0.5), Inches(0.2), Inches(10), Inches(0.9),
   size=26, bold=True, color=WHITE)
tb(s4, "⏱ 1:00 ~ 1:20",
   Inches(11.0), Inches(0.35), Inches(2.0), Inches(0.5),
   size=12, color=RGBColor(254,215,170))

bullets_tech = [
    ("🖥️",  "網頁介面",
     "用 Python 的 Streamlit 做的，\n就像在填表單一樣直觀。\n不怕按錯——重新整理也不會消失！"),
    ("🤖",  "AI 在自己電腦跑",
     "叫 Ollama 或 LM Studio 幫忙，\n這些 AI 裝在你電腦裡。\n不用網路，不用付錢！"),
    ("🔧",  "AI 講話整理器",
     "AI 有時候說話會帶廢話，\n程式會自己把廢話過濾掉，\n只留下真正有用的重點和考題。"),
    ("🛡️",  "備用保護機制",
     "萬一 AI 沒開或網路斷線，\n系統自動切換到「展示模式」，\n90 秒演示一定順暢！"),
]

for i,(icon,title,body) in enumerate(bullets_tech):
    col_ = i % 2; row_ = i // 2
    lx = Inches(0.5) + col_ * Inches(6.5)
    ty = Inches(1.5) + row_ * Inches(2.8)
    rect(s4, lx, ty, Inches(6.1), Inches(2.5), WHITE,
         RGBColor(229,231,235))
    tb(s4, f"{icon}  {title}", lx+Inches(0.2), ty+Inches(0.15),
       Inches(5.7), Inches(0.5), size=15, bold=True, color=BLUE_DARK)
    tb(s4, body, lx+Inches(0.2), ty+Inches(0.68),
       Inches(5.7), Inches(1.7), size=12.5, color=GRAY_DARK)

# ─────────────────────────────────────────────────────────────────────────────
# Slide 5 ▸ 怎麼測試 & 結果
# ─────────────────────────────────────────────────────────────────────────────
s5 = prs.slides.add_slide(BLANK); bg(s5)

rect(s5, 0, 0, prs.slide_width, Inches(1.3), RGBColor(79,70,229))
tb(s5, "測試了什麼？結果怎樣？",
   Inches(0.5), Inches(0.2), Inches(10), Inches(0.9),
   size=26, bold=True, color=WHITE)
tb(s5, "⏱ 現場試給你看",
   Inches(11.0), Inches(0.35), Inches(2.0), Inches(0.5),
   size=12, color=RGBColor(199,210,254))

tests = [
    ("📖", "用內建的教育文章測",
     "AI 完整整理出 4 個重點，\n3 題考題全部切中核心，\n解析清楚到位。"),
    ("🎉", "故意全答對",
     "會跳出「慶祝氣球特效」！\n系統即時顯示「3/3 全對！」，\n並展開每題的詳細解說。"),
    ("❌", "故意把 AI 關掉再測",
     "系統偵測到 AI 沒有開，\n自動切到「預設展示模式」，\n不會當機、不會出現紅字錯誤。"),
    ("📱", "不同大小的瀏覽器視窗",
     "目前在電腦畫面表現最好，\n手機版是未來的改善目標（下一步）。"),
]

for i,(icon,title,body) in enumerate(tests):
    col_ = i % 2; row_ = i // 2
    lx = Inches(0.5) + col_ * Inches(6.5)
    ty = Inches(1.5) + row_ * Inches(2.8)
    fill_ = RGBColor(240,253,244) if i%2==0 else RGBColor(239,246,255)
    border_ = RGBColor(167,243,208) if i%2==0 else RGBColor(191,219,254)
    rect(s5, lx, ty, Inches(6.1), Inches(2.5), fill_, border_)
    tb(s5, f"{icon}  {title}", lx+Inches(0.2), ty+Inches(0.15),
       Inches(5.7), Inches(0.5), size=15, bold=True, color=BLUE_DARK)
    tb(s5, body, lx+Inches(0.2), ty+Inches(0.68),
       Inches(5.7), Inches(1.7), size=12.5, color=GRAY_DARK)

# ─────────────────────────────────────────────────────────────────────────────
# Slide 6 ▸ 下一步 & 結語
# ─────────────────────────────────────────────────────────────────────────────
s6 = prs.slides.add_slide(BLANK); bg(s6, RGBColor(30,58,138))

# 左半：下一步
rect(s6, Inches(0.4), Inches(0.8), Inches(6.3), Inches(6.2), WHITE)
tb(s6, "🚀  下一步想做什麼？",
   Inches(0.6), Inches(0.95), Inches(6.0), Inches(0.6),
   size=18, bold=True, color=BLUE_DARK)

nexts = [
    ("📎","上傳整份 PDF 或 Word",
     "不用再一字一字複製貼上"),
    ("📇","製作記憶卡",
     "手機也能隨時隨地刷題複習"),
    ("📱","手機 / 平板版面優化",
     "讓小螢幕也能完整使用"),
]
for i,(icon,t1,t2) in enumerate(nexts):
    ty = Inches(1.75) + i*Inches(1.7)
    rect(s6, Inches(0.6), ty, Inches(5.8), Inches(1.45),
         RGBColor(239,246,255), RGBColor(191,219,254))
    tb(s6, f"{icon}  {t1}", Inches(0.8), ty+Inches(0.12),
       Inches(5.4), Inches(0.5), size=14, bold=True, color=BLUE_DARK)
    tb(s6, t2, Inches(0.8), ty+Inches(0.65),
       Inches(5.4), Inches(0.6), size=12, color=GRAY_DARK)

# 右半：結語
rect(s6, Inches(7.1), Inches(0.8), Inches(5.8), Inches(6.2),
     RGBColor(37,99,235))

tb(s6, "感謝聆聽！",
   Inches(7.3), Inches(1.2), Inches(5.4), Inches(0.8),
   size=26, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

tb(s6,
   "讓每一次閱讀\n都真正學進大腦",
   Inches(7.3), Inches(2.1), Inches(5.4), Inches(1.2),
   size=18, color=RGBColor(191,219,254), align=PP_ALIGN.CENTER)

tb(s6,
   "411587035｜教行一｜楊皓翔\n\n"
   "github.com/haohsiangyang-0921/\nai-study-assistant",
   Inches(7.3), Inches(4.5), Inches(5.4), Inches(1.8),
   size=12, color=RGBColor(147,197,253), align=PP_ALIGN.CENTER)

# ─────────────────────────────────────────────────────────────────────────────
# 存檔
# ─────────────────────────────────────────────────────────────────────────────
out = r"c:\Users\yangh\OneDrive\Desktop\ai-study-assistant\專題簡報_AI課堂摘要與互動測驗小助手.pptx"
prs.save(out)
print(f"PPT 已儲存：{out}")
