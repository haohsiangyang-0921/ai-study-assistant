import os
import re
import json
import requests
import streamlit as st

# ==============================================================================
# 頁面配置與自訂樣式
# ==============================================================================
st.set_page_config(
    page_title="AI 課堂摘要與互動測驗小助手 (本地模型版)",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 現代化學生友善 UI 樣式
st.markdown("""
<style>
    /* 全域文字與字型調整 */
    .main-header {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 50%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.3rem !important;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #4B5563;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 0.3rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .badge-local {
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
    }
    .badge-demo {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FCD34D;
    }
    .badge-cloud {
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
    }
    .privacy-notice {
        background-color: #F0FDF4;
        border-left: 4px solid #10B981;
        padding: 0.85rem 1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.92rem;
        color: #065F46;
        margin-bottom: 1.2rem;
    }
    .summary-item {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 0.85rem 1.1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.75rem;
        font-size: 1rem;
        color: #1F2937;
        line-height: 1.6;
    }
    .quiz-card {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
    }
    .explanation-box {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 0.85rem;
        margin-top: 0.75rem;
        color: #1E40AF;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 範例文章與 Demo 模式資料
# ==============================================================================
SAMPLE_ARTICLE = """【主動回想與間隔重複的記憶機制】
在認知心理學中，傳統的「重複閱讀」（Passive Rereading）被證實是最耗時且效率最低的學習方法之一。學生反覆瀏覽劃滿螢光筆的課文時，常會產生一種「我已經學會了」的認知錯覺（Fluency Illusion），然而這僅僅是視覺上的熟悉感，並非真正的長期記憶編碼。

相較之下，「主動回想」（Active Recall）要求大腦在沒有提示的情況下，主動提取儲存在突觸網絡中的知識。根據「測試效應」（Testing Effect）研究，每次提取記憶的過程，大腦的神經迴路都會進行重新強化與重構，從而大幅延緩遺忘速度。

此外，結合德國心理學家艾賓浩斯提出的「遺忘曲線」，最佳的記憶鞏固策略是「間隔重複」（Spaced Repetition）。當大腦即將遺忘某個知識點的臨界點進行主動測驗與複習，大腦會釋放更多神經傳導物質，使該記憶節點由工作記憶轉化為穩固的長期記憶（Long-term Memory）。

因此，現代教育建議學生：停止被動抄寫與劃重點，改為「讀完一個段落立刻自我提問，並在一天、三天與一週後進行間隔小測驗」。"""

DEMO_RESULT = {
    "summary": [
        "**被動重讀的認知錯覺**：反覆瀏覽課文僅產生表面熟悉感（Fluency Illusion），缺乏深層神經編碼，學習成效低。",
        "**主動回想（Active Recall）**：透過在無提示下主動提取記憶，促使神經迴路重新構建與強化，顯著延緩遺忘。",
        "**測試效應（Testing Effect）**：測驗不只是能力評量工具，更是促使大腦深度記憶編碼的高效學習手段。",
        "**間隔重複（Spaced Repetition）**：根據艾賓浩斯遺忘曲線，在即將遺忘的臨界點進行自我檢測，能最高效率地將資訊固化為長期記憶。"
    ],
    "quiz": [
        {
            "id": 1,
            "question": "根據文章，為什麼傳統的反覆劃重點與閱讀效果有限？",
            "options": [
                "A. 會使學生產生「我已經學會」的認知錯覺（Fluency Illusion）",
                "B. 會過度消耗大腦的長期記憶空間",
                "C. 容易造成艾賓浩斯遺忘曲線的逆轉",
                "D. 因為大腦無法接收超過兩種顏色的螢光筆標記"
            ],
            "answer": "A",
            "explanation": "文章明確指出，重複瀏覽劃線文章只會帶來視覺上的熟悉感，讓人誤以為已經掌握（認知錯覺），但並未完成深層記憶編碼。"
        },
        {
            "id": 2,
            "question": "何謂「測試效應」（Testing Effect）在認知學習上的真正意義？",
            "options": [
                "A. 僅用於期末對學生進行排名與能力篩選",
                "B. 記憶提取的過程本身就是一種重構與強化神經迴路的有效學習手段",
                "C. 能夠證明不需睡眠也能維持長期記憶",
                "D. 減少大腦突觸數量以避免神經元疲乏"
            ],
            "answer": "B",
            "explanation": "測試效應證明：每次主動提取記憶時，大腦神經網絡都會重新強化與重組，使測驗成為記憶編碼強化的過程，而不只是評分工具。"
        },
        {
            "id": 3,
            "question": "結合艾賓浩斯遺忘曲線，何時進行「間隔重複」複習的效益最高？",
            "options": [
                "A. 剛讀完課文的當下一秒內不間斷重複十次",
                "B. 在大腦即將遺忘某知識點的臨界點進行主動測驗",
                "C. 等到一個月後的期末考前一天通宵複習",
                "D. 只有在心情完全放鬆且睡著的時候"
            ],
            "answer": "B",
            "explanation": "文章指出，最佳策略是在大腦即將遺忘的臨界點進行主動回想與測驗，此時神經傳導物質最能促成工作記憶轉移為穩固的長期記憶。"
        }
    ]
}

# ==============================================================================
# 工具函式：本地模型通訊與 JSON 容錯解析
# ==============================================================================
def get_local_models(base_url: str):
    """自本機模型伺服器（Ollama 或 LM Studio）查詢已下載或載入的模型清單"""
    models = []
    clean_base = base_url.strip().rstrip("/")
    root_url = clean_base.replace("/v1", "")

    # 1. 嘗試 Ollama 原生 API: http://localhost:11434/api/tags
    try:
        resp = requests.get(f"{root_url}/api/tags", timeout=1.5)
        if resp.status_code == 200:
            data = resp.json()
            models = [m.get("name") for m in data.get("models", []) if m.get("name")]
            if models:
                return models
    except Exception:
        pass

    # 2. 嘗試 OpenAI 相容格式: http://localhost:11434/v1/models 或 LM Studio http://localhost:1234/v1/models
    try:
        v1_url = clean_base if clean_base.endswith("/v1") else f"{clean_base}/v1"
        resp = requests.get(f"{v1_url}/models", timeout=1.5)
        if resp.status_code == 200:
            data = resp.json()
            models = [m.get("id") for m in data.get("data", []) if m.get("id")]
            if models:
                return models
    except Exception:
        pass

    return models

def extract_json_response(raw_text: str):
    """增強型 JSON 提取器：支援本地模型常見的 Markdown 包裹與前後多餘說明字元"""
    raw_text = raw_text.strip()
    
    # 1. 直接解析
    try:
        return json.loads(raw_text)
    except Exception:
        pass

    # 2. 擷取 ```json ... ``` 程式碼區塊
    if "```" in raw_text:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except Exception:
                pass

    # 3. 尋找最外層的 { 與 }
    first_brace = raw_text.find("{")
    last_brace = raw_text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        try:
            return json.loads(raw_text[first_brace:last_brace+1])
        except Exception:
            pass

    return None

def call_llm(base_url: str, model_name: str, api_key: str, text: str):
    """統一呼叫 OpenAI 相容端點（支援 Ollama、LM Studio 與雲端 API）"""
    system_prompt = """你是一位專業的教育心理學家與頂尖教學助教。
請針對使用者提供的學習材料，完成以下兩項任務：
1. 整理出 3 至 5 個關鍵核心重點（請使用繁體中文），每個重點附帶標題與簡短說明。
2. 設計 3 題高質量的單選測驗題（每題有 A, B, C, D 四個選項、標記正確答案如 "A"、以及詳細解析），檢驗學生是否真正理解核心概念（而非死背）。

請務必嚴格以標準 JSON 格式回傳，且不要包含多餘廢話，格式範例如下：
{
  "summary": [
    "**重點標題**：重點詳細說明...",
    "**重點標題**：重點詳細說明..."
  ],
  "quiz": [
    {
      "id": 1,
      "question": "題目敘述...",
      "options": ["A. 選項一", "B. 選項二", "C. 選項三", "D. 選項四"],
      "answer": "A",
      "explanation": "針對正確答案與錯誤選項的解析..."
    }
  ]
}"""

    clean_base = base_url.strip().rstrip("/")
    endpoint = f"{clean_base}/chat/completions" if clean_base.endswith("/v1") else f"{clean_base}/v1/chat/completions"

    headers = {
        "Content-Type": "application/json"
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"學習材料內容如下：\n\n{text}"}
        ],
        "temperature": 0.3,
        "stream": False
    }

    response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    resp_data = response.json()
    
    # 取得回傳文字
    content = resp_data["choices"][0]["message"]["content"]
    parsed = extract_json_response(content)
    if not parsed or "summary" not in parsed or "quiz" not in parsed:
        raise ValueError("本地模型回傳內容未能成功解析為所需的 JSON 格式。")
    return parsed

# ==============================================================================
# 狀態初始化與回呼函式 (Session State & Callbacks)
# ==============================================================================
if "article_input" not in st.session_state:
    st.session_state["article_input"] = ""
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = {}
if "quiz_submitted" not in st.session_state:
    st.session_state["quiz_submitted"] = False
if "detected_models" not in st.session_state:
    st.session_state["detected_models"] = []

def load_sample_article():
    """載入範例文章並重置先前的測驗狀態"""
    st.session_state["article_input"] = SAMPLE_ARTICLE
    st.session_state["analysis_result"] = None
    st.session_state["quiz_submitted"] = False
    st.session_state["user_answers"] = {}

def clear_article_input():
    """清空輸入區文字與分析結果"""
    st.session_state["article_input"] = ""
    st.session_state["analysis_result"] = None
    st.session_state["quiz_submitted"] = False
    st.session_state["user_answers"] = {}

# ==============================================================================
# 側邊欄：AI 模型與服務設定 (支援本機 Ollama / LM Studio)
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ AI 模型核心設定")
    
    # 模式選擇
    backend_mode = st.radio(
        "選擇 AI 運算方式",
        [
            "🏠 本地模型 (Ollama / LM Studio)",
            "☁️ 雲端 API (OpenAI 相容)",
            "🟡 演示模式 (Demo Mode)"
        ],
        index=0,
        help="推薦使用本地模型：完全免費、資料不出電腦、保護隱私且無額外 API 限制。"
    )

    base_url = "http://localhost:11434/v1"
    model_name = "llama3.2"
    api_key = "local-key"
    is_demo = False

    if backend_mode == "🏠 本地模型 (Ollama / LM Studio)":
        st.markdown('<span class="badge badge-local">🏠 本地模型模式</span>', unsafe_allow_html=True)
        
        server_preset = st.selectbox(
            "本地服務捷徑",
            [
                "Ollama (預設 http://localhost:11434/v1)",
                "LM Studio (預設 http://localhost:1234/v1)",
                "自訂本地伺服器網址"
            ]
        )
        
        if "Ollama" in server_preset:
            default_url = "http://localhost:11434/v1"
        elif "LM Studio" in server_preset:
            default_url = "http://localhost:1234/v1"
        else:
            default_url = "http://localhost:8000/v1"

        base_url = st.text_input("本地 API 伺服器網址", value=default_url)

        # 偵測本地模型按鈕
        col_detect, _ = st.columns([2, 1])
        with col_detect:
            if st.button("🔄 偵測本機已下載模型"):
                with st.spinner("正在探測本機 AI 服務..."):
                    found = get_local_models(base_url)
                    st.session_state["detected_models"] = found
                    if found:
                        st.success(f"已偵測到 {len(found)} 個本地模型！")
                    else:
                        st.warning("未偵測到運作中的本地服務。請確認已執行 `ollama run ...` 或啟動 LM Studio。")

        # 模型名稱選擇 / 輸入
        detected = st.session_state.get("detected_models", [])
        if detected:
            model_name = st.selectbox("選擇本地模型", detected, index=0)
        else:
            common_models = ["llama3.2", "llama3", "qwen2.5", "gemma2", "mistral", "taide", "自訂輸入"]
            chosen = st.selectbox("指定模型名稱", common_models, index=0)
            if chosen == "自訂輸入":
                model_name = st.text_input("輸入本機模型名稱 (如 llama3.2:1b)", value="llama3.2")
            else:
                model_name = chosen

        st.caption("💡 免費離線運算，無需任何 API Key。")

    elif backend_mode == "☁️ 雲端 API (OpenAI 相容)":
        st.markdown('<span class="badge badge-cloud">☁️ 雲端 API 模式</span>', unsafe_allow_html=True)
        env_key = os.getenv("OPENAI_API_KEY", "").strip()
        user_key = st.text_input("API Key (密碼遮罩)", value=env_key, type="password")
        api_key = user_key
        base_url = st.text_input("API 網址 (Base URL)", value="https://api.openai.com/v1")
        model_name = st.selectbox("選擇模型", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)
        
        if not api_key:
            st.warning("未輸入 API Key，送出時將自動降級為 Demo 備用模式。")

    else:
        # 強制 Demo 模式
        st.markdown('<span class="badge badge-demo">🟡 演示模式 (Demo Mode)</span>', unsafe_allow_html=True)
        st.info("💡 演示模式已啟動，不消耗本機算力或 API，保證 90 秒順暢展示！")
        is_demo = True

    st.markdown("---")
    st.markdown("### 🎯 核心學習功能")
    st.markdown("""
    1. **重點萃取**：過濾冗贅資訊，提煉核心概念。
    2. **互動測驗**：基於認知科學測試效應，自動生成隨堂三題。
    3. **即時解析**：提交後立即批改並呈現完整題解。
    """)
    st.markdown("---")
    st.caption("Designed for Students | 本地離線隱私保障")

# ==============================================================================
# 主畫面標題與隱私提示
# ==============================================================================
st.markdown('<div class="main-header">🎓 AI 課堂摘要與互動測驗小助手</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">專為學生打造的高效學習利器 —— 結合認知心理學「主動回想」機制，快速提煉重點與自我檢測！</div>', unsafe_allow_html=True)

if backend_mode == "🏠 本地模型 (Ollama / LM Studio)":
    st.markdown("""
    <div class="privacy-notice">
        🔒 <b>本地模型離線保護已啟用</b>：所有的文章、教科書章節與筆記內容，均<b>直接在您的個人電腦內執行 AI 運算</b>，零資料外傳、零 API 費用，兼顧隱私與學習效率！
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 區塊 1：教材與筆記輸入區
# ==============================================================================
st.markdown("### 📝 第一步：輸入或載入閱讀材料")

# 操作按鈕列
col_btn1, col_btn2, _ = st.columns([1.5, 1, 4])
with col_btn1:
    st.button("📚 載入範例文章", use_container_width=True, on_click=load_sample_article)

with col_btn2:
    st.button("🧹 清空內容", use_container_width=True, on_click=clear_article_input)

# 文字輸入框（直接綁定 key="article_input"，即時同步狀態）
st.text_area(
    "請在下方貼上課堂筆記、教科書章節或論文內容：",
    height=200,
    placeholder="在此貼上任何長篇教材或點擊上方「載入範例文章」開始體驗...",
    key="article_input"
)

# 開始分析按鈕
start_analysis = st.button("🚀 開始由本地 AI 分析並生成隨堂測驗", type="primary", use_container_width=True)

if start_analysis:
    current_text = st.session_state.get("article_input", "").strip()
    if not current_text:
        st.warning("⚠️ 請先輸入文章內容，或點擊「載入範例文章」！")
    else:
        with st.spinner(f"🤖 本地 AI ({model_name}) 正在精讀文章、萃取重點並出題中..."):
            if is_demo:
                result = DEMO_RESULT
            else:
                try:
                    result = call_llm(base_url, model_name, api_key, current_text)
                except Exception as e:
                    st.warning(f"⚠️ 連線至本地模型伺服器時發生問題（{str(e)}）。\n\n系統已自動切換為 Demo 模式呈現優質分析，確保您的展示順暢不中斷！")
                    result = DEMO_RESULT
                    
            st.session_state["analysis_result"] = result
            st.session_state["quiz_submitted"] = False
            st.session_state["user_answers"] = {}
        st.success("✨ 分析完成！已為您提煉核心摘要並出好隨堂複習題。")

# ==============================================================================
# 區塊 2 & 3：生成成果展示 (核心摘要 + 互動測驗)
# ==============================================================================
if st.session_state.get("analysis_result"):
    res = st.session_state["analysis_result"]
    summary_list = res.get("summary", [])
    quiz_list = res.get("quiz", [])
    
    st.markdown("---")
    
    # 核心重點摘要
    st.markdown("### 💡 核心重點摘要 (Key Takeaways)")
    st.caption("AI 已經為您去蕪存菁，掌握以下核心概念即可掌握本章精髓：")
    
    for i, item in enumerate(summary_list, 1):
        st.markdown(f'<div class="summary-item"><b>重點 {i}</b> ｜ {item}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 互動式隨堂三題測驗
    st.markdown("### ✍️ 互動隨堂測驗 (3-Question Interactive Quiz)")
    st.caption("依據認知心理學的「主動回想」機制，測驗能大幅強化大腦突觸連結。請選出最適當的答案：")
    
    with st.form(key="quiz_form"):
        for q in quiz_list:
            q_id = q.get("id", 1)
            q_text = q.get("question", "")
            options = q.get("options", [])
            
            st.markdown(f"#### ❓ 第 {q_id} 題：{q_text}")
            
            # 單選按鈕
            selected_option = st.radio(
                label=f"請選擇第 {q_id} 題答案：",
                options=options,
                index=None,
                key=f"radio_q_{q_id}",
                label_visibility="collapsed"
            )
            st.session_state["user_answers"][q_id] = selected_option
            st.markdown("<br>", unsafe_allow_html=True)
            
        submit_quiz = st.form_submit_button("📝 提交答案並查看解析", type="primary", use_container_width=True)
        
    if submit_quiz:
        st.session_state["quiz_submitted"] = True

    # 顯示測驗批改結果與解析
    if st.session_state.get("quiz_submitted", False):
        st.markdown("### 📊 測驗成果與深度解析")
        
        correct_count = 0
        total_questions = len(quiz_list)
        
        for q in quiz_list:
            q_id = q.get("id", 1)
            correct_ans_letter = q.get("answer", "").strip().upper()
            user_choice = st.session_state["user_answers"].get(q_id)
            
            # 檢查使用者是否選取該字母 (例如 'A. ...' 開頭為 'A')
            is_correct = False
            if user_choice and user_choice.strip().startswith(correct_ans_letter):
                is_correct = True
                correct_count += 1
                
        # 成績反饋橫幅
        score_percent = int((correct_count / total_questions) * 100) if total_questions > 0 else 0
        if correct_count == total_questions:
            st.balloons()
            st.success(f"🎉 太棒了！全對！得分：{correct_count} / {total_questions} ({score_percent}分) —— 您已徹底掌握該教材的核心概念！")
        elif correct_count >= 1:
            st.info(f"👍 不錯的表現！得分：{correct_count} / {total_questions} ({score_percent}分) —— 請參照下方解析，針對錯題進行主動回想強化。")
        else:
            st.warning(f"💪 得分：{correct_count} / {total_questions} ({score_percent}分) —— 別灰心！「提取失敗」也是大腦重新鞏固記憶的關鍵過程，快看看解析吧！")
            
        # 逐題解析卡片
        for q in quiz_list:
            q_id = q.get("id", 1)
            q_text = q.get("question", "")
            correct_ans_letter = q.get("answer", "").strip().upper()
            user_choice = st.session_state["user_answers"].get(q_id, "未作答")
            explanation = q.get("explanation", "")
            
            is_correct = user_choice and user_choice.strip().startswith(correct_ans_letter)
            
            status_icon = "✅ 正確" if is_correct else "❌ 需複習"
            status_color = "#10B981" if is_correct else "#EF4444"
            
            with st.expander(f"第 {q_id} 題結果：{status_icon} ｜ {q_text}", expanded=True):
                st.markdown(f"**您的回答**：`{user_choice if user_choice else '未作答'}`")
                st.markdown(f"**標準答案**：`<span style='color:{status_color}; font-weight:bold;'>選項 {correct_ans_letter}</span>`", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="explanation-box">
                    💡 <b>深度題解與認知概念</b>：<br>
                    {explanation}
                </div>
                """, unsafe_allow_html=True)
