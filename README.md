# 🎓 AI 課堂摘要與互動測驗小助手 (本地模型離線版)

> 專為學生打造的智慧學習夥伴 —— 支援**本機離線 AI 模型（Ollama / LM Studio）**，完全免費、資料不出電腦、零 API 金鑰洩漏風險，快速提煉長文重點並自動生成隨堂測驗！

---

## 📌 專案亮點與目標

1. **本機隱私保護**：所有教材、課堂筆記與論文均在您的電腦本機離線運算，零個資與版權教材外傳風險。
2. **零 API 費用**：直接調用本機 Ollama 或 LM Studio 模型（如 `llama3.2`, `qwen2.5`, `mistral`, `gemma2`, `taide` 等），不需購買或綁定信用卡。
3. **主動回想與測試效應**：依據認知心理學原理，一鍵生成 **3~5 個核心要點** 與 **3 題四選一隨堂測驗**，附帶即時評分與深度題解。
4. **演示備用機制（Demo Mode）**：若本機尚未啟動模型或暫時沒有算力，系統會自動無縫切換為 Demo 模式，確保展示或離線測試順暢不中斷！

---

## 🛠️ 技術架構

- **前端與互動介面**：Streamlit
- **AI 運算後端**：
  - 🏠 **本機本地模型**：Ollama（預設端點 `http://localhost:11434/v1`）或 LM Studio（`http://localhost:1234/v1`）
  - ☁️ **雲端 API 備用**：支援 OpenAI 相容端點（選填）
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
