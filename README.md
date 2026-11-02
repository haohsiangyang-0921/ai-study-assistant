# 🎓 AI 課堂摘要與互動測驗小助手

> 專為學生打造的智慧學習夥伴 —— **已部署上雲端，任何裝置打開網址即可使用、無需安裝任何程式**；同時支援本地離線 AI 模型（Ollama / LM Studio）與免費雲端 API（Groq），快速提煉長文重點並自動生成隨堂測驗！

---

## 🌐 線上直接使用（免安裝、免終端機）

本專案已部署於 **Streamlit Community Cloud**：

1. 用瀏覽器前往 `https://share.streamlit.io/app`（部署者本人）或分享後的 `https://<app-name>.streamlit.app` 網址。
2. 手機、平板、其他電腦可直接開啟，**完全不需要安裝 Python 或任何程式**。
3. 預設為「🟡 演示模式」——打開即可用；想體驗真實 AI 分析，可在側邊欄選「☁️ 雲端 API」並輸入 Groq 的免費 API Key。

### 部署步驟（全程只用瀏覽器，共 5 分鐘）

1. 先確認專案已推送到 GitHub（本專案的 repo：`haohsiangyang-0921/ai-study-assistant`）。
2. 前往 [share.streamlit.io](https://share.streamlit.io)，用 GitHub 帳號登入（免費）。
3. 點擊 **「Create app」→「Deploy a public app from GitHub」**。
4. 選擇 repo `haohsiangyang-0921/ai-study-assistant`、branch `main`、Main file path 填 `app.py`。
5. 按下 **Deploy**，等 2~3 分鐘即取得永久公開網址。之後每次 `git push`，線上版本會自動更新。

（選填）若要讓所有人免輸入 Key 就能用雲端 AI：登入後進入該 App 的 **Settings → Secrets**，貼上：

```toml
GROQ_API_KEY = "gsk_你的金鑰"
```

> 💡 免費 API Key 可在 [console.groq.com](https://console.groq.com) 註冊即拿，Groq 是 OpenAI 相容端點，速度極快。

---

## 📌 專案亮點與目標

1. **本機隱私保護**：可選用本地模式，所有教材、課堂筆記與論文均在您的電腦本機離線運算，零個資與版權教材外傳風險。
2. **零 API 費用**：可調用本機 Ollama 或 LM Studio 模型（如 `llama3.2`, `qwen2.5`, `mistral` 等），或使用免費的 Groq 雲端 API，不需購買或綁定信用卡。
3. **主動回想與測試效應**：依據認知心理學原理，一鍵生成 **3~5 個核心要點** 與 **3 題四選一隨堂測驗**，附帶即時評分與深度題解。
4. **演示備用機制（Demo Mode）**：預設啟用，若本機尚未啟動模型或暫時沒有算力，系統會自動無縫切換為 Demo 模式，確保展示或離線測試順暢不中斷！

---

## 🛠️ 技術架構

- **前端與互動介面**：Streamlit
- **部署**：Streamlit Community Cloud（公開網址，任何裝置免安裝直開）
- **AI 運算後端**：
  - 🟡 **演示模式（預設）**：無需任何設定即可完整體驗
  - 🆓 **雲端 API**：Groq（免費）或 OpenAI 相容端點
  - 🏠 **本機本地模型**：Ollama（預設端點 `http://localhost:11434/v1`）或 LM Studio（`http://localhost:1234/v1`）
- **開發語言**：Python 3.10+

---

## 🚀 快速啟動指引

### 步驟 1：啟動您電腦上的本地模型（二選一）

#### 方案 A：使用 Ollama（推薦）
在電腦的終端機執行任一您已安裝的模型，例如：
```powershell
# 啟動 Llama 3.2
ollama run llama3.2

# 或啟動中文效果極佳的 Qwen 2.5
ollama run qwen2.5
```
*Ollama 啟動後會自動在背景監聽 `http://localhost:11434`。*

#### 方案 B：使用 LM Studio
1. 開啟 LM Studio 並載入您喜歡的模型。
2. 切換到 **Local Server** 頁籤，點擊 **Start Server**（預設連接埠為 1234）。

---

### 步驟 2：啟動 Web 應用程式

在專案目錄下執行：

```powershell
# 1. 進入專案目錄
cd ai-study-assistant

# 2. 安裝必要套件 (streamlit 與 requests)
pip install -r requirements.txt

# 3. 啟動 Streamlit 服務
streamlit run app.py
```

瀏覽器將自動開啟 `http://localhost:8501`。

---

## 🖥️ 介面操作指南

1. **側邊欄設定**：
   - 預設已選擇「🏠 本地模型 (Ollama / LM Studio)」。
   - 點擊「**🔄 偵測本機已下載模型**」按鈕，系統會自動探測並列出您電腦中已安裝的模型。
2. **載入教材**：
   - 點擊「**📚 載入範例文章**」或手動貼上課堂筆記、長篇文章。
3. **生成重點與測驗**：
   - 點擊「**🚀 開始由本地 AI 分析並生成隨堂測驗**」，本機模型將即時閱讀並完成結構化出題。
4. **互動答題與即時解析**：
   - 線上點選題目答案，按下「**📝 提交答案並查看解析**」，即時取得分數、正誤判定與深度題解！

---

## 📁 檔案結構

```text
ai-study-assistant/
│
├── app.py              # Streamlit 主程式（本地模型連接、UI 互動、容錯解析與測驗邏輯）
├── requirements.txt    # 輕量相依套件 (streamlit, requests)
└── README.md           # 完整使用與本地模型配置說明文件
```
