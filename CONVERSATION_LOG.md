# 📋 專案開發與對話歷程紀錄 (Development & Conversation Log)

本文件完整記錄「AI 課堂摘要與互動測驗小助手」從需求發想、架構設計、本機模型遷移、除錯修復至發布的完整開發軌跡。

---

## 📌 階段一：專案需求分析與第一版原型建立

### 1. 使用者需求
- **目標受眾**：學生（解決長篇教材「抓不到重點」與「缺乏複習題目」的痛點）。
- **核心功能**：
  - 長文字輸入區（`st.text_area`）與「載入範例文章」快捷鍵。
  - AI 萃取 3~5 點條列式核心精髓。
  - 互動式 3 題單選測驗（含 4 個選項、作答後即時評分與詳解）。
- **架構與安全性要求**：
  - Streamlit Web 應用程式（`app.py`）。
  - API 金鑰安全管理（禁止 Hardcode，使用環境變數）。
  - 90 秒評審展示專用免金鑰「Demo 模式」。

### 2. 開發實作成果
- 建立專案目錄 `ai-study-assistant/`。
- 開發 `app.py`，設計現代化卡片式學生友善 UI。
- 設計高品質教育心理學示範文章（主題：主動回想與艾賓浩斯遺忘曲線）及預設 Demo 題庫。
- 撰寫 `requirements.txt` 與完整 `README.md`。

---

## 📌 階段二：全面改用本機本地模型 (Local LLM Migration)

### 1. 使用者需求
- 捨棄雲端 API，全面改用使用者電腦本機已安裝的本地模型（例如 Ollama / LM Studio）。

### 2. 架構調整與升級
- **支援本地推論**：
  - 預設對接本機 Ollama 服務端點（`http://localhost:11434/v1`）與 LM Studio（`http://localhost:1234/v1`）。
  - 支援使用者自訂本地端點與指定模型（如 `llama3.2`, `qwen2.5`, `gemma2`, `taide` 等）。
- **優勢**：
  - 🔒 **100% 離線隱私保護**：教材與筆記資料不離開使用者本機電腦。
  - 💰 **零 API 費用**：完全免費，不需 API Key。
- **功能強化**：
  - 加入「🔄 偵測本機已下載模型」按鈕，主動探測本機 AI 伺服器並載入可用模型清單。
  - 實作增強型 JSON 容錯解析器，自動過濾本地模型常輸出的 Markdown ````json 標記與前後非結構化贅字。
  - 保持 Demo Mode 作為本地伺服器未啟動時的防禦性降級機制。

---

## 📌 階段三：路徑問題排查與終端機指引

### 1. 使用者反饋問題
- 使用者在 PowerShell 執行 `cd ai-study-assistant` 與 `streamlit run app.py` 時出現：
  - `找不到 'C:\Users\yangh\ai-study-assistant' 路徑`
  - `File does not exist: app.py`

### 2. 問題診斷與解決方案
- **原因**：PowerShell 預設開啟於使用者家目錄 `C:\Users\yangh`，而專案位於桌面目錄 `C:\Users\yangh\OneDrive\Desktop\ai-study-assistant`。
- **指引**：提供精確的絕對路徑切換指令：
  ```powershell
  cd "C:\Users\yangh\OneDrive\Desktop\ai-study-assistant"
  streamlit run app.py
  ```

---

## 📌 階段四：互動狀態快取修復與介面文字微調

### 1. 使用者反饋問題
- 點擊「載入範例文章」按鈕後，文字框未正確帶入文章，仍提示「請先輸入文章內容」。
- 希望將按鈕後方的「（教育心理學）」五個字刪除。

### 2. 技術診斷與修復
- **狀態競爭問題**：Streamlit 元件的 `key` 快取權重高於 `value` 參數，導致點擊按鈕重繪時被先前的空字串覆蓋。
- **解決方法**：重構為 Streamlit 標準的 `on_click` 回呼機制（`load_sample_article` 與 `clear_article_input`），直接對 `st.session_state["article_input"]` 進行寫入與雙向綁定。
- **文字調整**：按鈕簡化為「📚 載入範例文章」，並同步清理內文標題贅字。

---

## 📌 階段五：版本控制與開源發布

- 初始化 Git 儲存庫並配置 `.gitignore`。
- 生成專案開發歷程紀錄文件（本文件）。
- 提交所有核心程式碼與文檔，準備推送至 GitHub。
