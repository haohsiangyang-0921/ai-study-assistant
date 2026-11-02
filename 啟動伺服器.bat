@echo off
title AI 課堂摘要小助手

REM 切換到專案資料夾
cd /d "C:\Users\yangh\OneDrive\Desktop\ai-study-assistant"

REM 啟動 Streamlit，讓區域網路內所有裝置都能連線
REM   --server.address 0.0.0.0  → 讓其他裝置可以輸入 IP 連線
REM   --server.port 8501         → 連接埠 8501
REM   --server.headless true     → 不強制開瀏覽器（讓使用者自行開）

"C:\Users\yangh\AppData\Local\Programs\Python\Python312\python.exe" ^
    -m streamlit run app.py ^
    --server.address 0.0.0.0 ^
    --server.port 8501 ^
    --server.headless true
